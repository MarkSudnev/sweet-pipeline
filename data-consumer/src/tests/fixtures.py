from pathlib import Path
from typing import List

from src.main.domain.data_shipment import DataShipment
from src.main.domain.fetch_shipment import FetchShipment
from src.main.domain.parse_shipment_metadata import ParseShipmentMetadata
from src.main.domain.shipment_metadata import ShipmentMetadata
from src.main.domain.store_shipment import StoreShipment
from src.main.result import Result, Success, Unit

test_data_shipment = DataShipment(
  metadata=ShipmentMetadata("bucket/key.json", 1024, "type"),
  location=Path("/alpha/beta.json")
)


class DummyShipmentParser(ParseShipmentMetadata):

  def __init__(self):
    self.__is_called = False

  @property
  def is_called(self) -> bool:
    return self.__is_called

  def __call__(self, message: str) -> Result[List[ShipmentMetadata]]:
    self.__is_called = True
    return Success([ShipmentMetadata("", 1024, "plain/text")])


class DummyShipmentFetcher(FetchShipment):

  def __init__(self):
    self.__call_count = 0

  @property
  def is_called(self) -> bool:
    return self.__call_count > 0

  @property
  def call_count(self) -> int:
    return self.__call_count

  def __call__(self, metadata: ShipmentMetadata) -> Result[DataShipment]:
    self.__call_count += 1
    return Success(test_data_shipment)


class DummyShipmentStorage(StoreShipment):

  def __init__(self):
    self.__call_count = 0

  @property
  def is_called(self) -> bool:
    return self.__call_count > 0

  @property
  def call_count(self) -> int:
    return self.__call_count

  def __call__(self, metadata: DataShipment) -> Result[Result.Unit]:
    self.__call_count += 1
    return Success(Unit())
