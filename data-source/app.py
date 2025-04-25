
import json
from flask import Flask
from flask import request
from flask import Response

app = Flask(__name__)

@app.route("/data", methods=["GET"])
def data():
    query_parts = request.query_string.decode().split("&")
    q = list(filter(lambda a: a.startswith("q="), query_parts))
    if len(q) != 1:
        return Response(f"Wrong Request: {request.query_string}", status=400)
    _, query = q[0].split("=")
    return json.dumps({
        "query": query,
        "response": "some response data"
    })
