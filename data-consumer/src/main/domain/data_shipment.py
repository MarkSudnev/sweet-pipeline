from dataclasses import dataclass
from pathlib import Path

from src.main.domain.shipment_metadata import ShipmentMetadata


@dataclass(frozen=True, eq=True)
class DataShipment:
  metadata: ShipmentMetadata
  location: Path
