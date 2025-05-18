import logging
import uuid
from datetime import datetime

from airflow.decorators import dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.http.hooks.http import HttpHook
from requests import Response

_logger = logging.getLogger(__name__)

bucket_name = "sweet-bucket"
aws_region = "us-east-1"


@dag(
    dag_id="alpha_dag",
    dag_display_name="Fetch Data",
    start_date=datetime(2020, 1, 1),
    schedule="*/2 * * * *",
    max_active_runs=1,
    catchup=False
)
def alpha_dag():
    @task(task_id="fetch_data")
    def fetch_data():
        http_hook: HttpHook = HttpHook(http_conn_id="ALPHA", method="GET")
        s3_hook: S3Hook = S3Hook()
        response: Response = http_hook.run(endpoint="/api/v1/data?", data={"q": "if you want to be okay"})
        _logger.info(f"response: {response.status_code}")
        if response.status_code == 200:
            data: str = response.text
            s3_hook.load_string(
                string_data=data,
                bucket_name=bucket_name,
                key=f"sweet-{uuid.uuid4()}.json"
            )
        else:
            _logger.error(f"Error happened: {response.content}")

    fetch_data()


alpha_dag()
