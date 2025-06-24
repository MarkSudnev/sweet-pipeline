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
    shipment_parser: ParseShipmentMetadata = lambda _: Success(metadata)
    shipment_fetcher: FetchShipment = lambda _: Failure(error_message)

    data_consumer = DataConsumer(
      parse_shipment_metadata=shipment_parser,
      fetch_shipment=shipment_fetcher
    )

    result: Result[Result.Unit] = data_consumer("message string")

    assert result.is_successful() is False
    assert result.error == error_message

class DummyShipmentParser(ParseShipmentMetadata):

  def __init__(self):
    self.__is_called = False

  @property
  def is_called(self) -> bool:
    return self.__is_called

  def __call__(self, message: str) -> Result[ShipmentMetadata]:
    self.__is_called = True
    return Success(ShipmentMetadata("", 1024, "plain/text"))


class DummyShipmentFetcher(FetchShipment):

  def __init__(self):
    self.__is_called = False

  @property
  def is_called(self) -> bool:
    return self.__is_called

  def __call__(self, metadata: ShipmentMetadata) -> Result[Result.Unit]:
    self.__is_called = True
    return Success(Unit())
