from typing import Callable

from src.main.domain.fetch_shipment import FetchShipment
from src.main.domain.parse_shipment_metadata import ParseShipmentMetadata
from src.main.result import Result, Failure


def DataConsumer(
  parse_shipment_metadata: ParseShipmentMetadata,
  fetch_shipment: FetchShipment
) -> Callable[[str], Result[Result.Unit]]:

  def _execute(message: str) -> Result[Result.Unit]:
    shipment_metadata_result = parse_shipment_metadata(message)
    if not shipment_metadata_result.is_successful():
      return Failure(shipment_metadata_result.error)
    return fetch_shipment(shipment_metadata_result.value)

  return _execute
