from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class ShipMetadata:
  filepath: str
  size: int
  type: str
