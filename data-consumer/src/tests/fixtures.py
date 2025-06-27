from pathlib import Path
from typing import List

from src.main.domain.data_shipment import DataShipment
from src.main.domain.extract_file_location import ExtractFileLocation
from src.main.domain.fetch_shipment import FetchShipment, FileLocation
from src.main.domain.store_shipment import StoreShipment
from src.main.infrastructure.postgres_shipment_storage import PostgresStatementExecutor
from src.main.result import Result, Success, Unit

test_data_shipment = DataShipment(
  location=Path("/alpha/beta.json")
)


class DummyShipmentParser(ExtractFileLocation):

  def __init__(self):
    self.__is_called = False

  @property
  def is_called(self) -> bool:
    return self.__is_called

  def __call__(self, message: str) -> Result[FileLocation]:
    self.__is_called = True
    return Success(FileLocation("alpha/beta.json"))


class DummyShipmentFetcher(FetchShipment):

  def __init__(self):
    self.__call_count = 0

  @property
  def is_called(self) -> bool:
    return self.__call_count > 0

  @property
  def call_count(self) -> int:
    return self.__call_count

  def __call__(self, file_location: FileLocation) -> Result[DataShipment]:
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

  def __call__(self, shipment: DataShipment) -> Result[Result.Unit]:
    self.__call_count += 1
    return Success(Unit())


class DummyPostgresStatementExecutor(PostgresStatementExecutor):

  def __init__(self):
    self.__statements: List[str] = []

  @property
  def call_count(self) -> int:
    return len(self.__statements)

  @property
  def statements(self) -> List[str]:
    return self.__statements

  def __call__(self, statement: str):
    self.__statements.append(statement)
