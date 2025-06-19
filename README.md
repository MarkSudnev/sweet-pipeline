# sweet-pipeline

### data-source  
Generates data by query


## TODO
Add Kafka event publishing to minio
[minio-kafka manual](https://min.io/docs/minio/linux/administration/monitoring/publish-events-to-kafka.html)

#### Debug commands
```bash
./bin/kafka-topics.sh --bootstrap-server=localhost:9092 --list
./bin/kafka-console-consumer.sh --bootstrap-server=localhost:9092 --topic=sweet --from-beginning
```
