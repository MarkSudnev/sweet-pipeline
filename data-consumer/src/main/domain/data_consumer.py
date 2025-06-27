from typing import Callable

from src.main.domain.data_shipment import DataShipment
from src.main.domain.extract_file_location import ExtractFileLocation
from src.main.domain.fetch_shipment import FetchShipment
from src.main.domain.file_location import FileLocation
from src.main.domain.store_shipment import StoreShipment
from src.main.result import Result, Failure, Success, Unit


def DataConsumer(
  extract_file_location: ExtractFileLocation,
  fetch_shipment: FetchShipment,
  store_shipment: StoreShipment
) -> Callable[[str], Result[Result.Unit]]:

  def _execute(message: str) -> Result[Result.Unit]:
    file_location_result: Result[FileLocation] = extract_file_location(message)
    if not file_location_result.is_successful():
      return Failure(file_location_result.error)

    shipment_result: Result[DataShipment] = fetch_shipment(file_location_result.value)
    if not shipment_result.is_successful():
      return Failure(shipment_result.error)

    result: Result[Result.Unit] = store_shipment(shipment_result.value)
    if not result.is_successful():
      return Failure(result.error)

    return Success(Unit())

  return _execute
