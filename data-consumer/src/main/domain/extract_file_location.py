from typing import Callable

from src.main.domain.file_location import FileLocation
from src.main.result import Result

ExtractFileLocation = Callable[[str], Result[FileLocation]]
