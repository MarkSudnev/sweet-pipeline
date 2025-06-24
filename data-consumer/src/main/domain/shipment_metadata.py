from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class ShipmentMetadata:
  filepath: str
  size: int
  type: str
