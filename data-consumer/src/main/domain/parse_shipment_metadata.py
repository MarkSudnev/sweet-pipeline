from typing import Callable

from src.main.domain.shipment_metadata import ShipmentMetadata
from src.main.result import Result

ParseShipmentMetadata = Callable[[str], Result[ShipmentMetadata]]
