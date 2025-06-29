from typing import Callable

from domain.file_location import FileLocation
from result import Result

ExtractFileLocation = Callable[[str], Result[FileLocation]]
