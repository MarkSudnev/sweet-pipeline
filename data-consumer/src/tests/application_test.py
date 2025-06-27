from pathlib import Path

import boto3
from moto import mock_aws

from src.main.domain.data_consumer import DataConsumer
from src.main.infrastructure.json_file_location_extractor import \
  JsonFileLocationExtractor
from src.main.infrastructure.postgres_shipment_storage import PostgresShipmentStorage
from src.main.infrastructure.s3_data_shipment_fetcher import S3DataShipmentFetcher
from src.main.result import Result
from src.tests import read_resource, prepare_bucket, get_resource
from src.tests.fixtures import DummyPostgresStatementExecutor


class TestApplication:
  bucket_name = "sweet-bucket"

  @mock_aws
  def test_app(self):
    prepare_bucket(
      bucket_name=self.bucket_name,
      content={"sweet-94c13f58-73cf-4ad4-9afa-3823dcada72f.json": read_resource("alpha-shipment-example.json").encode("utf-8")})

    message: str = read_resource("message_example.json")
    executor = DummyPostgresStatementExecutor()
    data_consumer = DataConsumer(
      extract_file_location=JsonFileLocationExtractor(),
      fetch_shipment=S3DataShipmentFetcher(
        aws_access_key_id="aaa",
        aws_secret_access_key="bbb",
        store_path=Path(get_resource("store"))
      ),
      store_shipment=PostgresShipmentStorage(executor)
    )

    result: Result[Result.Unit] = data_consumer(message)
    if not result.is_successful():
      print(result.error)
    assert result.is_successful() is True
    assert executor.call_count > 0

