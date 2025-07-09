# Sweet Pipeline

![architecture](/docs/architecture.png)

Simple data pipeline. Pipeline is periodically triggered by Apache Airflow. Such architecture is quite flexible and allows us to add new data-sources and data-consumers quickly and easelly. Just add new DAG to Airflow and corresponding Data Consumer as well.

### Data Source
Simple FLask application uses simple AI-powered dummy text generator to produce response.

### Apache Airflow
Has one DAG which pulls data from **Data Source** every 2 minutes and stores the data to S3 storage.

### S3 Storage
Minio implementation. Stores input raw files pulled by **Apache Airflow**. Once new file is arrived S3 emit event with file's metadata to **a topic in Kafka Broker**. 

### Data Consumer  
A python application designed by Hexagon-like architecture. Listens **a topic in Kafka**. Once new event is received:  
- Extracts new file's location from metadata
- Pulls file from **S3**
- Extracts data from file
- Stores extracted data to storage (PostgreSQL)

## How to run
```bash
docker compose up -d
```
then open Grafana dashboard http://localhost:3000 Log in with admin/admin and observe `data-source` and `data-consumer` graphs




## TODO
- [x] enchance monitoring
- [ ] [data-consumer] fix missing topic failure
- [ ] CI/CD with gh-actions
- [ ] [data-source] improve logging
- [ ] [airflow] improve logging
