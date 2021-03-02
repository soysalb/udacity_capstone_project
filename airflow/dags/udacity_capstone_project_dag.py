from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (PostgresOperator, StageToRedshiftOperator, LoadFactOperator, LoadDimensionOperator,
                               DataQualityOperator)
from helpers import SqlQueries

# Default arguments for DAG
default_args = {
    'owner': 'udacity_data_engineering_nanodegree',
    'start_date': datetime(2020, 3, 1),
    'depends_on_past': False,
    'email_on_retry': True
}

# Definition of DAG
dag = DAG('udacity_capstone_project',
          default_args=default_args,
          description='Udacity Data Engineering Nanodegree Capstone Project',
          schedule_interval='@once',
          max_active_runs=1
          )

# start_operator Task by using DummyOperator
start_operator = DummyOperator(task_id='Begin_execution', dag=dag)

# create_all_tables Task by using PostgresOperator
create_all_tables = PostgresOperator(
    task_id="create_all_tables",
    dag=dag,
    postgres_conn_id="redshift",
    sql="create_all_tables.sql"
)

# stage_exchanges_to_redshift Task by using StageToRedshiftOperator
stage_exchanges_to_redshift = StageToRedshiftOperator(
    task_id='stage_exchanges_to_redshift',
    dag=dag,
    table="staging_exchanges",
    s3_bucket='udacity-capstone-bucket-berna',
    s3_key='staging_exchanges',
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    provide_context=True
)

# stage_tickers_to_redshift Task by using StageToRedshiftOperator
stage_tickers_to_redshift = StageToRedshiftOperator(
    task_id='stage_tickers_to_redshift',
    dag=dag,
    table="staging_tickers",
    s3_bucket='udacity-capstone-bucket-berna',
    s3_key='staging_tickers',
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    file_type='csv',
    provide_context=True
)

# load_tickers_table Task by using LoadFactOperator
load_tickers_table = LoadFactOperator(
    task_id='load_tickers_table',
    dag=dag,
    table='tickers',
    sql=SqlQueries.tickers_table_insert,
    redshift_conn_id='redshift',
    provide_context=True
)

# load_markets_dimension_table Task by using LoadDimensionOperator
load_markets_dimension_table = LoadDimensionOperator(
    task_id='load_markets_dimension_table',
    dag=dag,
    table='markets',
    sql=SqlQueries.markets_table_insert,
    redshift_conn_id='redshift',
    provide_context=True
)

# load_exchanges_dimension_table Task by using LoadDimensionOperator
load_exchanges_dimension_table = LoadDimensionOperator(
    task_id='load_exchanges_dimension_table',
    dag=dag,
    table='exchanges',
    sql=SqlQueries.recipes_table_insert,
    redshift_conn_id='redshift',
    provide_context=True
)

# load_time_dimension_table Task by using LoadDimensionOperator
load_time_dimension_table = LoadDimensionOperator(
    task_id='load_time_dimension_table',
    dag=dag,
    table='time',
    sql=SqlQueries.time_table_insert,
    redshift_conn_id='redshift',
    provide_context=True
)

# run_quality_checks_markets Task by using DataQualityOperator
run_quality_checks_markets = DataQualityOperator(
    task_id='run_quality_checks_markets',
    dag=dag,
    redshift_conn_id='redshift',
    query='select count(*) from markets where Symbol is null;',
    result=0,
    provide_context=True
)

# run_quality_checks_exchanges Task by using DataQualityOperator
run_quality_checks_exchanges = DataQualityOperator(
    task_id='run_quality_checks_exchanges',
    dag=dag,
    redshift_conn_id='redshift',
    query='select count(*) from exchanges where ExchangeKey is null;',
    result=0,
    provide_context=True
)

# end_operator Task by using DummyOperator
end_operator = DummyOperator(task_id='End_execution', dag=dag)

# Dependicies of Tasks
start_operator >> create_all_tables >> [stage_exchanges_to_redshift, stage_tickers_to_redshift] >> load_tickers_table
load_tickers_table >> [load_markets_dimension_table, load_time_dimension_table, load_exchanges_dimension_table] >> [
    run_quality_checks_markets, run_quality_checks_exchanges]
run_quality_checks_exchanges >> end_operator
