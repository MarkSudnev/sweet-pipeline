from typing import Callable, List

from src.main.domain.data_shipment import DataShipment
from src.main.domain.fetch_shipment import FetchShipment
from src.main.domain.parse_shipment_metadata import ParseShipmentMetadata
from src.main.domain.store_shipment import StoreShipment
from src.main.result import Result, Failure, Success, Unit


def DataConsumer(
  parse_shipment_metadata: ParseShipmentMetadata,
  fetch_shipment: FetchShipment,
  store_shipment: StoreShipment
) -> Callable[[str], Result[Result.Unit]]:

  def _execute(message: str) -> Result[Result.Unit]:
    shipment_metadata_result = parse_shipment_metadata(message)
    if not shipment_metadata_result.is_successful():
      return Failure(shipment_metadata_result.error)

    shipments: List[DataShipment] = []
    for metadata in shipment_metadata_result.value:
      result: Result[DataShipment] = fetch_shipment(metadata)
      if not result.is_successful():
        return Failure(result.error)
      shipments.append(result.value)

    for shipment in shipments:
      result: Result[Result.Unit] = store_shipment(shipment)
      if not result.is_successful():
        return Failure(result.error)

    return Success(Unit())

  return _execute
