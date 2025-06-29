import json
from typing import Dict, Any

from domain.extract_file_location import ExtractFileLocation
from domain.file_location import FileLocation
from result import Result, Failure


def JsonFileLocationExtractor() -> ExtractFileLocation:

  def _execute(message: str) -> Result[FileLocation]:
    result: Result[Dict[str, Any]] = Result.from_function(lambda : json.loads(message))
    if not result.is_successful():
      return Failure(result.error)
    return Result.from_function(lambda : FileLocation(result.value["Key"]))

  return _execute
