from moto import mock_aws

from src.main.domain.data_shipment import DataShipment
from src.main.domain.shipment_metadata import ShipmentMetadata
from src.main.infrastructure.s3_data_shipment_fetcher import S3DataShipmentFetcher
from src.main.result import Result
from src.tests import prepare_bucket


class TestS3DataShipmentFetcher:

  @mock_aws
  def test_fetch_shipment_from_s3(self):
    prepare_bucket(
      bucket_name="alpha",
      content={"beta.json": "one-two".encode("utf8")}
    )
    metadata = ShipmentMetadata("alpha/beta.json", 1024, "type/type")
    fetcher = S3DataShipmentFetcher(
      aws_access_key_id="key",
      aws_secret_access_key="secret"
    )

    result: Result[DataShipment] = fetcher(metadata)

    assert result.is_successful() is True
