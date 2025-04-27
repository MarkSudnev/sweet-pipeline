
import json
import subprocess
from flask import Flask
from flask import request
from flask import Response

app = Flask(__name__)

@app.route("/data", methods=["GET"])
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
    response_body = json.dumps({"query": query, "response": f"{result.stdout} | {result.stderr}"})
    return Response(response_body, status=200, content_type="application/json")
