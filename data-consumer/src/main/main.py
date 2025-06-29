import logging
import os
import sys
import tempfile
from pathlib import Path

from kafka import KafkaConsumer

from domain.data_consumer import DataConsumer
from infrastructure.json_file_location_extractor import \
  JsonFileLocationExtractor
from infrastructure.postgres_client import PostgresCLient
from infrastructure.postgres_shipment_storage import PostgresShipmentStorage
from infrastructure.s3_data_shipment_fetcher import S3DataShipmentFetcher
from result import Result

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
  stream=sys.stdout
)


def main(
  kafka_brokers,
  kafka_topic,
  aws_access_key_id,
  aws_secret_access_key,
  aws_endpoint,
  pg_connection_string
):
  # executor = PostgresCLient(pg_connection_string)
  executor = PostgresCLient(pg_connection_string)
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
    data = message.value.decode("utf-8")
    logging.info(f"Message received: {data}")
    result: Result[Result.Unit] = data_consumer(data)
    if not result.is_successful():
      logging.error(f"Consumption failed: {result.error}")


#   try_number = 1
#   consumer: KafkaConsumer = ...
#   while try_number < 20:
#     try:
#       logging.info(f"Trying to connect to Kafka: {try_number}/5")
#       consumer = KafkaConsumer(
#         kafka_topic,
#         group_id=None,
#         bootstrap_servers=kafka_brokers,
#         auto_offset_reset='earliest'
#       )
#       break
#     except NoBrokersAvailable as e:
#       if try_number < 5:
#         logging.warning("Failed to connect to Kafka")
#       else:
#         raise e
#     try_number += 1
#     time.sleep(5)
#
#   while True:
#     response = consumer.poll(timeout_ms=1000)
#     if response is None:
#       continue
#     messages = flat_messages(response.values())
#     keys = [m.value for m in messages]
#     for k in keys:
#       logging.info(f"Message received: {k.decode('utf-8')}")
#
#
# def flat_messages(messages: List[List[Any]]) -> List:
#   out_messages = []
#   for message in messages:
#     out_messages.extend(message)
#   return out_messages


if __name__ == "__main__":
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

"""
raise Errors.NoBrokersAvailable()
kafka.errors.NoBrokersAvailable: NoBrokersAvailable
"""
