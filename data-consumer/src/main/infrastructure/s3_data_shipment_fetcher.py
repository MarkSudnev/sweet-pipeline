import boto3

from src.main.domain.data_shipment import DataShipment
from src.main.domain.fetch_shipment import FetchShipment
from src.main.domain.shipment_metadata import ShipmentMetadata
from src.main.result import Result, Success, Unit


def S3DataShipmentFetcher(
  aws_access_key_id: str,
  aws_secret_access_key: str
) -> FetchShipment:

  s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
  )

  def _execute(metadata: ShipmentMetadata) -> Result[DataShipment]:
    
    return Success(Unit())

  return _execute
