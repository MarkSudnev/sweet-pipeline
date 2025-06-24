from typing import List

from src.main.domain.data_consumer import DataConsumer
from src.main.domain.fetch_shipment import FetchShipment
from src.main.domain.parse_shipment_metadata import ParseShipmentMetadata
from src.main.domain.shipment_metadata import ShipmentMetadata
from src.main.result import Success, Unit, Result, Failure


class TestDataConsumer:

  def test_call_collaborators(self):
    shipment_parser = DummyShipmentParser()
    shipment_fetcher = DummyShipmentFetcher()
    data_consumer = DataConsumer(
      parse_shipment_metadata=shipment_parser,
      fetch_shipment=shipment_fetcher
    )
    result: Result[Result.Unit] = data_consumer("message string")

    assert result.is_successful() is True
    assert shipment_parser.is_called is True
    assert shipment_fetcher.is_called is True

  def test_return_failure_when_shipment_parser_is_failed(self):
    error_message = "Unable to parse shipment metadata"
    shipment_parser: ParseShipmentMetadata = lambda _: Failure(error_message)
    shipment_fetcher: FetchShipment = lambda _: Success(Unit())

    data_consumer = DataConsumer(
      parse_shipment_metadata=shipment_parser,
      fetch_shipment=shipment_fetcher
    )

    result: Result[Result.Unit] = data_consumer("message string")

    assert result.is_successful() is False
    assert result.error == error_message

  def test_return_failure_when_shipment_fetcher_is_failed(self):
    error_message = "Unable to fetch shipment"
    metadata = ShipmentMetadata("alpha/beta.json", 1024, "application/json")
    shipment_parser: ParseShipmentMetadata = lambda _: Success([metadata])
    shipment_fetcher: FetchShipment = lambda _: Failure(error_message)

    data_consumer = DataConsumer(
      parse_shipment_metadata=shipment_parser,
      fetch_shipment=shipment_fetcher
    )

    result: Result[Result.Unit] = data_consumer("message string")

    assert result.is_successful() is False
    assert result.error == error_message

  def test_call_fetcher_for_each_shipment(self):
    metadata = ShipmentMetadata("alpha/beta.json", 1024, "application/json")
    shipment_parser: ParseShipmentMetadata = lambda _: Success([metadata, metadata])
    shipment_fetcher = DummyShipmentFetcher()

    data_consumer = DataConsumer(
      parse_shipment_metadata=shipment_parser,
      fetch_shipment=shipment_fetcher
    )

    result: Result[Result.Unit] = data_consumer("message string")

    assert result.is_successful() is True
    assert shipment_fetcher.call_count == 2

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
    self.__is_called = False
    self.__call_count = 0

  @property
  def is_called(self) -> bool:
    return self.__is_called

  @property
  def call_count(self) -> int:
    return self.__call_count

  def __call__(self, metadata: ShipmentMetadata) -> Result[Result.Unit]:
    self.__is_called = True
    self.__call_count += 1
    return Success(Unit())
