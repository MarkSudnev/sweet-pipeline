import os
from typing import Dict

import boto3


def read_resource(filename: str) -> str:
  folder, _ = os.path.split(__file__)
  resource_filename: str = os.path.join(folder, "resources", filename)
  with open(resource_filename, "r") as resource_file:
    return resource_file.read()


def prepare_bucket(bucket_name: str, content: Dict[str, bytes] = None) -> None:
  s3 = boto3.client("s3")
  s3.create_bucket(Bucket=bucket_name)
  if content:
    for key, value in content.items():
      s3.put_object(Bucket=bucket_name, Key=key, Body=value)
