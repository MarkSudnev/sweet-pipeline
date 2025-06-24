from typing import Callable, List

from src.main.domain.shipment_metadata import ShipmentMetadata
from src.main.result import Result

ParseShipmentMetadata = Callable[[str], Result[List[ShipmentMetadata]]]
