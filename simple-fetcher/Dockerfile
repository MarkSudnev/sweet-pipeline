FROM debian:bookworm-slim

RUN apt update
RUN apt install -y curl jq

CMD ["sh", "-c", "curl -s http://data-source:8091/api/v1/data?q=hello | jq >> /opt/storage/out.json"]