import json
import subprocess
import time
import uuid
from datetime import datetime, UTC

from flask import Flask
from flask import Response
from flask import request
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Gauge

app = Flask(__name__)

inference_latency = Gauge(
    "inference_latency_seconds",
    "How long inference happens"
)

inference_size = Gauge(
    "inference_size_chars",
    "Characters count"
)


class Timer:

    def __init__(self):
        self.__started: float = 0.0
        self.__duration: float = 0.0

    @property
    def duration(self) -> float:
        return self.__duration

    def __enter__(self):
        self.__started = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__duration = time.perf_counter() - self.__started


@app.route("/api/v1/data", methods=["GET"])
def data():
    query = request.args.get("q")
    if not query:
        return Response("No query found", status=400)
    _timer = Timer()
    with _timer:
        result = subprocess.run(
            [f"/opt/llama2.c/run /opt/llama2.c/stories15M.bin -z /opt/llama2.c/tokenizer.bin -n 256 -i \"{query}\""],
            capture_output=True,
            shell=True,
            text=True
        )
    inference_latency.set(_timer.duration)
    if not result.stdout and result.stderr:
        return Response(result.stderr, status=500)
    body: str = result.stdout
    inference_size.set(len(body))
    response_body = json.dumps({
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "query": query,
        "response": f"{body}"
    })
    return Response(response_body, status=200, content_type="application/json")


@app.route("/ready", methods=["GET"])
def ready():
    return Response(status=200)


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
