import boto3
from moto import mock_aws

from src.main.domain.data_consumer import DataConsumer
from src.tests import read_resource, prepare_bucket


class TestApplication:
  bucket_name = "test-bucket"

  @mock_aws
  def test_app(self):
    prepare_bucket(self.bucket_name)

    message: str = read_resource("message_example.json")
    data_consumer = DataConsumer()

    data_consumer(message)

    self.__assert_bucket_contains("sweet-94c13f58-73cf-4ad4-9afa-3823dcada72f.json")

  def __assert_bucket_contains(self, filename: str):
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=self.bucket_name)
    assert "Contents" in response.keys()
