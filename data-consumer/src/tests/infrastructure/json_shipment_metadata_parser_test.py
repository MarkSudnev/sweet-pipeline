from src.main.domain.file_location import FileLocation
from src.main.infrastructure.json_file_location_extractor import \
  JsonFileLocationExtractor
from src.main.result import Result
from src.tests import read_resource


class TestJsonShipmentMetadataParser:

  def test_parser_parses_message_to_shipment_metadata(self):
    message = read_resource("message_example.json")
    parser = JsonFileLocationExtractor()

    result: Result[FileLocation] = parser(message)

    assert result.is_successful() is True
    assert result.value == FileLocation(
      uri="sweet-bucket/sweet-94c13f58-73cf-4ad4-9afa-3823dcada72f.json"
    )

  def test_parser_returns_failure_when_message_is_incorrect(self):
    message = """{"invalid": "json"}"""
    parser = JsonFileLocationExtractor()

    result: Result[FileLocation] = parser(message)

    assert result.is_successful() is False
    assert result.error is not None
