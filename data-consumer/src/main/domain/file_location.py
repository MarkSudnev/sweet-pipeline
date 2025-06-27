from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class FileLocation:
  uri: str
