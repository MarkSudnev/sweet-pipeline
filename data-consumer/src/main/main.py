import json
import logging
import os
import sys
import tempfile
from pathlib import Path
from typing import List, Dict, Any

from kafka import KafkaConsumer
from prometheus_client import start_http_server, Counter

from domain.data_consumer import DataConsumer
from infrastructure.json_file_location_extractor import \
  JsonFileLocationExtractor
from infrastructure.postgres_client import PostgresClient
from infrastructure.postgres_shipment_storage import PostgresShipmentStorage
from infrastructure.s3_data_shipment_fetcher import S3DataShipmentFetcher
from result import Result

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
  stream=sys.stdout
)

counter = Counter("messages_consumed", "Messages Consumed")


def main(
  kafka_brokers: List[str],
  kafka_topic: str,
  aws_access_key_id: str,
  aws_secret_access_key: str,
  aws_endpoint: str,
  pg_connection_string: str
):
  executor = PostgresClient(pg_connection_string)
  data_consumer = DataConsumer(
    extract_file_location=JsonFileLocationExtractor(),
    fetch_shipment=S3DataShipmentFetcher(
      aws_access_key_id=aws_access_key_id,
      aws_secret_access_key=aws_secret_access_key,
      endpoint_url=aws_endpoint,
      store_path=Path(tempfile.gettempdir()).joinpath("data-consumer")
    ),
    store_shipment=PostgresShipmentStorage(executor)
  )

  kafka_consumer = KafkaConsumer(
    kafka_topic,
    bootstrap_servers=kafka_brokers,
    auto_offset_reset="earliest"
  )

  for message in kafka_consumer:
    data: str = message.value.decode("utf-8")
    data_obj: Dict[str, Any] = json.loads(data)
    logging.info(f"Message received: {data_obj['Key']}")
    result: Result[Result.Unit] = data_consumer(data)
    counter.inc()
    if not result.is_successful():
      logging.error(f"Consumption failed: {result.error}")


if __name__ == "__main__":
  _, thread = start_http_server(port=8099)
  brokers = os.environ["KAFKA_BROKERS"].split(",")
  topic = os.environ["KAFKA_TOPIC"]
  aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"]
  aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"]
  aws_endpoint = os.environ["AWS_ENDPOINT"]
  pg_connection_string = os.environ["POSTGRES_CONNECTION_STRING"]
  main(
    brokers,
    topic,
    aws_access_key_id,
    aws_secret_access_key,
    aws_endpoint,
    pg_connection_string
  )
  thread.join()
