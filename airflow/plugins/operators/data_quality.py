from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class DataQualityOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 query="",
                 result="",
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.query = query
        self.result = result

    def execute(self, context):
        self.log.info('Creating Postgres connection')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info("Checking Data Quality")
        num_of_records = redshift.get_records(self.query)
        if num_of_records[0][0] != self.result:
            raise Error("Data Quality Failed :(")
        else:
            self.log.info("Data Quality Passed :)")
