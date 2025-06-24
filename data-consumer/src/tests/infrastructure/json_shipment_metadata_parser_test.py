from typing import List

from src.main.domain.shipment_metadata import ShipmentMetadata
from src.main.infrastructure.json_shipment_metadata_parser import \
  JsonShipmentMetadataParser
from src.main.result import Result
from src.tests import read_resource


class TestJsonShipmentMetadataParser:

  def test_parser_parses_message_to_shipment_metadata(self):
    message = read_resource("message_example.json")
    parser = JsonShipmentMetadataParser()

    result: Result[List[ShipmentMetadata]] = parser(message)

    assert result.is_successful() is True
    assert result.value[0] == ShipmentMetadata(
      filepath="sweet-bucket/sweet-94c13f58-73cf-4ad4-9afa-3823dcada72f.json",
      size=865,
      type="binary/octet-stream"
    )

  def test_parser_returns_failure_when_message_is_incorrect(self):
    message = """{"invalid": "json"}"""
    parser = JsonShipmentMetadataParser()

    result: Result[List[ShipmentMetadata]] = parser(message)

    assert result.is_successful() is False
    assert result.error is not None
