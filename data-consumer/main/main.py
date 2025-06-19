from kafka import KafkaConsumer


def main():
  consumer = KafkaConsumer(
    'sweet',
    bootstrap_servers=['localhost:29092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True
  )
  print("Listening", consumer.topics())
  for message in consumer:
    if message:
      print(message.key.decode('utf-8'))


if __name__ == "__main__":
  main()
