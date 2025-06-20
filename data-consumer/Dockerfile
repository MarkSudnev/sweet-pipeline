FROM debian:bookworm-slim

USER root

RUN apt update
RUN apt install -y curl ca-certificates python3

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH=/root/.local/bin:${PATH}
ENV APP_FOLDER=/opt/consumer

RUN mkdir -p $APP_FOLDER
COPY src ${APP_FOLDER}/src
COPY requirements.txt ${APP_FOLDER}/requirements.txt
WORKDIR $APP_FOLDER

RUN uv venv
RUN uv pip install -r requirements.txt

CMD ["/opt/consumer/.venv/bin/python", "src/main/main.py"]
