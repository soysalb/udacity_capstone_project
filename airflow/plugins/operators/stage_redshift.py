from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class StageToRedshiftOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 table="",
                 s3_bucket="",
                 s3_key="",
                 redshift_conn_id="",
                 aws_credentials_id="",
                 file_type="parquet",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.file_type = file_type

    def execute(self, context):
        if self.file_type == "csv":
            sql_copy = """
            COPY {}
            FROM '{}'
            ACCESS_KEY_ID '{}'
            SECRET_ACCESS_KEY '{}'
            CSV
            dateformat 'auto'
            timeformat 'auto'
            IGNOREHEADER 1
            """
        else:
            sql_copy = """
            COPY {}
            FROM '{}'
            ACCESS_KEY_ID '{}'
            SECRET_ACCESS_KEY '{}'
            FORMAT AS PARQUET
            """

        self.log.info('Getting AWS credentials')
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()

        self.log.info('Creating Postgres connection')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info('Copying data')
        s3_path = "s3://{}/{}".format(self.s3_bucket, self.s3_key)
        sql = sql_copy.format(
            self.table,
            s3_path,
            credentials.access_key,
            credentials.secret_key
        )
        redshift.run(sql)
