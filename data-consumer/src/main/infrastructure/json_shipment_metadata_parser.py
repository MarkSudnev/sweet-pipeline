import json
from typing import Dict, Any, List

from src.main.domain.parse_shipment_metadata import ParseShipmentMetadata
from src.main.domain.shipment_metadata import ShipmentMetadata
from src.main.result import Result, Failure


def JsonShipmentMetadataParser() -> ParseShipmentMetadata:

  def __extract_metadata(message: Dict[str, Any]) -> List[ShipmentMetadata]:
    metadatas: List[ShipmentMetadata] = []
    for record in message["Records"]:
      filepath = f"{record["s3"]["bucket"]["name"]}/{record["s3"]["object"]["key"]}"
      metadata = ShipmentMetadata(
        filepath=filepath,
        size=record["s3"]["object"]["size"],
        type=record["s3"]["object"]["contentType"],
      )
      metadatas.append(metadata)
    return metadatas

  def _execute(message: str) -> Result[List[ShipmentMetadata]]:
    result: Result[Dict[str, Any]] = Result.from_function(lambda : json.loads(message))
    if not result.is_successful():
      return Failure(result.error)
    return Result.from_function(lambda : __extract_metadata(result.value))

  return _execute
