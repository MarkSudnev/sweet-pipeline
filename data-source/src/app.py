
import json
import subprocess
import uuid
from datetime import datetime, UTC

from flask import Flask
from flask import Response
from flask import request

app = Flask(__name__)

@app.route("/api/v1/data", methods=["GET"])
def data():
    query = request.args.get("q")
    if not query:
        return Response("No query found", status=400)
    result = subprocess.run(
        [f"/opt/llama2.c/run /opt/llama2.c/stories15M.bin -z /opt/llama2.c/tokenizer.bin -n 256 -i \"{query}\""],
        capture_output=True,
        shell=True,
        text=True
    )
    if not result.stdout and result.stderr:
        return Response(result.stderr, status=500)
    response_body = json.dumps({
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "query": query,
        "response": f"{result.stdout}"
    })
    return Response(response_body, status=200, content_type="application/json")
