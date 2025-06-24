import os

import boto3


def read_resource(filename: str) -> str:
  folder, _ = os.path.split(__file__)
  resource_filename: str = os.path.join(folder, "resources", filename)
  with open(resource_filename, "r") as resource_file:
    return resource_file.read()


def prepare_bucket(bucket_name: str) -> None:
  s3 = boto3.client("s3")
  s3.create_bucket(Bucket=bucket_name)
