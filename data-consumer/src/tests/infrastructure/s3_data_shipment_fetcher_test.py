import tempfile
from pathlib import Path

from moto import mock_aws

from src.main.domain.data_shipment import DataShipment
from src.main.domain.file_location import FileLocation
from src.main.infrastructure.s3_data_shipment_fetcher import S3DataShipmentFetcher
from src.main.result import Result
from src.tests import prepare_bucket


class TestS3DataShipmentFetcher:

  temp_dir: Path = Path(tempfile.gettempdir()).joinpath("data-consumer")

  def teardown_method(self):
    if self.temp_dir.exists():
      for item in self.temp_dir.iterdir():
        if not item.is_dir():
          item.unlink()

  @mock_aws
  def test_fetch_shipment_from_s3(self):
    prepare_bucket(
      bucket_name="alpha",
      content={"beta/gamma.json": "one-two".encode("utf8")}
    )
    file_location = FileLocation("alpha/beta/gamma.json")

    fetcher = S3DataShipmentFetcher(aws_access_key_id="key",
                                    aws_secret_access_key="secret",
                                    store_path=self.temp_dir)

    result: Result[DataShipment] = fetcher(file_location)

    assert result.is_successful() is True
    assert result.value.location == self.temp_dir.joinpath("beta/gamma.json")

  @mock_aws
  def test_returns_failure_when_bucket_is_missing(self):
    prepare_bucket(
      bucket_name="alpha",
      content={"beta/gamma.json": "one-two".encode("utf8")}
    )
    file_location = FileLocation("missing-bucket/beta/gamma.json")

    fetcher = S3DataShipmentFetcher(aws_access_key_id="key",
                                    aws_secret_access_key="secret",
                                    store_path=self.temp_dir)

    result: Result[DataShipment] = fetcher(file_location)

    assert result.is_successful() is False

  @mock_aws
  def test_returns_failure_when_key_is_missing(self):
    prepare_bucket(
      bucket_name="alpha",
      content={"beta/gamma.json": "one-two".encode("utf8")}
    )
    file_location = FileLocation("not/existing/key.json")

    fetcher = S3DataShipmentFetcher(aws_access_key_id="key",
                                    aws_secret_access_key="secret",
                                    store_path=self.temp_dir)

    result: Result[DataShipment] = fetcher(file_location)

    assert result.is_successful() is False

  def test_returns_failure_when_s3_is_unavailable(self):
    file_location = FileLocation("not/existing/key.json")

    fetcher = S3DataShipmentFetcher(aws_access_key_id="key",
                                    aws_secret_access_key="secret",
                                    store_path=self.temp_dir)

    result: Result[DataShipment] = fetcher(file_location)

    assert result.is_successful() is False
