import os
from typing import Dict

import boto3


def read_resource(filename: str) -> str:
  resource_filename: str = get_resource(filename)
  with open(resource_filename, "r") as resource_file:
    return resource_file.read()


def get_resource(filename) -> str:
  folder, _ = os.path.split(__file__)
  return os.path.join(folder, "resources", filename)


def prepare_bucket(bucket_name: str, content: Dict[str, bytes] = None) -> None:
  s3 = boto3.client("s3")
  s3.create_bucket(Bucket=bucket_name)
  if content:
    for key, value in content.items():
      s3.put_object(Bucket=bucket_name, Key=key, Body=value)
