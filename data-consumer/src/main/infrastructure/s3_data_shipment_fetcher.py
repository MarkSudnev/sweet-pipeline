import os
from pathlib import Path
from typing import List, Dict

import boto3

from src.main.domain.data_shipment import DataShipment
from src.main.domain.fetch_shipment import FetchShipment
from src.main.domain.file_location import FileLocation
from src.main.result import Result, Success, Failure


def S3DataShipmentFetcher(
  aws_access_key_id: str,
  aws_secret_access_key: str,
  store_path: Path,
  endpoint_url=None
) -> FetchShipment:
  s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    endpoint_url=endpoint_url
  )

  def __prepare_directory(file: Path):
    if not file.parent.exists():
      file.parent.mkdir(parents=True, exist_ok=True)

  def _execute(file_location: FileLocation) -> Result[DataShipment]:
    path_components: List[str] = file_location.uri.split("/")
    bucket = path_components[0]
    key = "/".join(path_components[1:])
    local_path: str = os.sep.join(path_components[1:])
    result: Result[Dict] = Result.from_function(
      lambda: s3_client.get_object(Bucket=bucket, Key=key))
    if not result.is_successful():
      return Failure(result.error)
    content: bytes = result.value["Body"].read()
    location: Path = store_path.joinpath(local_path)
    __prepare_directory(location)
    location.write_bytes(content)
    return Success(DataShipment(location=location))

  return _execute
