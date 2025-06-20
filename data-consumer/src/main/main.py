import logging
import os
import sys
import time
from typing import Any, List

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
  stream=sys.stdout
)


def main(kafka_brokers, kafka_topic):
  try_number = 1
  consumer: KafkaConsumer = ...
  while try_number < 20:
    try:
      logging.info(f"Trying to connect to Kafka: {try_number}/5")
      consumer = KafkaConsumer(
        kafka_topic,
        group_id=None,
        bootstrap_servers=kafka_brokers,
        auto_offset_reset='earliest'
      )
      break
    except NoBrokersAvailable as e:
      if try_number < 5:
        logging.warning("Failed to connect to Kafka")
      else:
        raise e
    try_number += 1
    time.sleep(5)

  while True:
    response = consumer.poll(timeout_ms=1000)
    if response is None:
      continue
    messages = flat_messages(response.values())
    keys = [m.value for m in messages]
    for k in keys:
      logging.info(f"Message received: {k.decode('utf-8')}")


def flat_messages(messages: List[List[Any]]) -> List:
  out_messages = []
  for message in messages:
    out_messages.extend(message)
  return out_messages


if __name__ == "__main__":
  brokers = os.environ["KAFKA_BROKERS"].split(",")
  topic = os.environ["KAFKA_TOPIC"]
  main(brokers, topic)

"""
raise Errors.NoBrokersAvailable()
kafka.errors.NoBrokersAvailable: NoBrokersAvailable
"""
