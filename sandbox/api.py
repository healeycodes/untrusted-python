import os
import sys
import requests
import subprocess
from flask_cors import CORS
from flask import Flask, request, Response

app = Flask(__name__)
CORS(app)


@app.route("/api/ping")
def ping():
    return ""


@app.route("/api/exec", methods=["POST"])
def exec():
    code = request.get_json()["code"]
    proc = subprocess.Popen(
        [sys.executable, "./sandbox.py", code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={
            "PATH": os.environ.get("PATH"),
        },
    )

    extra = ""
    try:
        stdout, stderr = proc.communicate(code, timeout=2)
    except subprocess.TimeoutExpired:
        extra = "process timed out"
        proc.kill()
        stdout, stderr = proc.communicate()

    response = Response(f"{stdout.decode()}\n{stderr.decode()}\n{extra}")

    @response.call_on_close
    def on_close():
        API_KEY = os.environ.get("AXIOM_KEY")
        API_DATASET = os.environ.get("AXIOM_DATASET")
        if not API_KEY or not API_DATASET:
            return
        requests.post(
            f"https://api.axiom.co/v1/datasets/{API_DATASET}/ingest",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json=[
                {
                    "data": {
                        "code": code,
                        "stdout": stdout.decode(),
                        "stderr": stderr.decode(),
                    },
                },
            ],
        ),

    return response
