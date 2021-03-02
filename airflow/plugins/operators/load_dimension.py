from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class LoadDimensionOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 table="",
                 sql="",
                 redshift_conn_id="",
                 *args, **kwargs):
        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.sql = sql
        self.redshift_conn_id = redshift_conn_id

    def execute(self, context):
        self.log.info('Creating Postgres connection')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info('Inserting data')
        sql_insert = f"insert into {self.table} {self.sql};"
        redshift.run(sql_insert)
