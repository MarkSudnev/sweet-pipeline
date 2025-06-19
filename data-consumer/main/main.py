from kafka import KafkaConsumer

def main():
  consumer = KafkaConsumer('sweet', bootstrap_servers=['localhost:9092'])
  for message in consumer:
    print(message)

if __name__ == "__main__":
  main()
