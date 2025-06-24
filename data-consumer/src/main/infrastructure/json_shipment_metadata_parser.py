import json
from typing import Dict, Any

from src.main.domain.parse_shipment_metadata import ParseShipmentMetadata
from src.main.domain.shipment_metadata import ShipmentMetadata
from src.main.result import Result, Success, Failure


def JsonShipmentMetadataParser() -> ParseShipmentMetadata:

  def __extract_metadata(message: Dict[str, Any]) -> ShipmentMetadata:
    filepath = f"{message["Records"][0]["s3"]["bucket"]["name"]}/{message["Records"][0]["s3"]["object"]["key"]}"
    return ShipmentMetadata(
      filepath=filepath,
      size=message["Records"][0]["s3"]["object"]["size"],
      type=message["Records"][0]["s3"]["object"]["contentType"],
    )

  def _execute(message: str) -> Result[ShipmentMetadata]:
    result: Result[Dict[str, Any]] = Result.from_function(lambda : json.loads(message))
    if not result.is_successful():
      return Failure(result.error)
    return Result.from_function(lambda : __extract_metadata(result.value))

  return _execute
