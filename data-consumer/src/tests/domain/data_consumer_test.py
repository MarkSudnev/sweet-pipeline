from src.main.domain.data_consumer import DataConsumer
from src.main.domain.extract_file_location import ExtractFileLocation
from src.main.domain.fetch_shipment import FetchShipment
from src.main.domain.file_location import FileLocation
from src.main.domain.store_shipment import StoreShipment
from src.main.result import Success, Unit, Result, Failure
from src.tests.fixtures import DummyShipmentParser, DummyShipmentFetcher, \
  DummyShipmentStorage, test_data_shipment


class TestDataConsumer:

  def test_call_collaborators(self):
    shipment_parser = DummyShipmentParser()
    shipment_fetcher = DummyShipmentFetcher()
    shipment_storage = DummyShipmentStorage()
    data_consumer = DataConsumer(
      extract_file_location=shipment_parser,
      fetch_shipment=shipment_fetcher,
      store_shipment=shipment_storage
    )
    result: Result[Result.Unit] = data_consumer("message string")

    assert result.is_successful() is True
    assert shipment_parser.is_called is True
    assert shipment_fetcher.is_called is True
    assert shipment_storage.is_called is True

  def test_return_failure_when_shipment_parser_is_failed(self):
    error_message = "Unable to parse shipment metadata"
    shipment_parser: ExtractFileLocation = lambda _: Failure(error_message)
    shipment_fetcher: FetchShipment = lambda _: Success(test_data_shipment)
    shipment_storage: StoreShipment = lambda _: Success(Unit())

    data_consumer = DataConsumer(
      extract_file_location=shipment_parser,
      fetch_shipment=shipment_fetcher,
      store_shipment=shipment_storage
    )

    result: Result[Result.Unit] = data_consumer("message string")

    assert result.is_successful() is False
    assert result.error == error_message

  def test_return_failure_when_shipment_fetcher_is_failed(self):
    error_message = "Unable to fetch shipment"
    file_location = FileLocation("alpha/beta.json")
    shipment_parser: ExtractFileLocation = lambda _: Success([file_location])
    shipment_fetcher: FetchShipment = lambda _: Failure(error_message)
    shipment_storage: StoreShipment = lambda _: Success(Unit())

    data_consumer = DataConsumer(
      extract_file_location=shipment_parser,
      fetch_shipment=shipment_fetcher,
      store_shipment=shipment_storage
    )

    result: Result[Result.Unit] = data_consumer("message string")

    assert result.is_successful() is False
    assert result.error == error_message

  def test_return_failure_when_failed_to_store_shipment(self):
    error_message = "Unable to store shipment"
    file_location = FileLocation("alpha/beta.json")
    shipment_parser: ExtractFileLocation = lambda _: Success([file_location])
    shipment_fetcher: FetchShipment = lambda _: Success(test_data_shipment)
    shipment_storage: StoreShipment = lambda _: Failure(error_message)

    data_consumer = DataConsumer(
      extract_file_location=shipment_parser,
      fetch_shipment=shipment_fetcher,
      store_shipment=shipment_storage
    )

    result: Result[Result.Unit] = data_consumer("message string")

    assert result.is_successful() is False
    assert result.error == error_message
