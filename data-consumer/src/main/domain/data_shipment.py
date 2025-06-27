from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, eq=True)
class DataShipment:
  location: Path
