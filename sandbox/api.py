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
        AXIOM_KEY = os.environ.get("AXIOM_KEY")
        AXIOM_DATASET = os.environ.get("AXIOM_DATASET")
        if not AXIOM_KEY or not AXIOM_DATASET:
            print('missing logging env vars')
            return
        requests.post(
            f"https://api.axiom.co/v1/datasets/{AXIOM_DATASET}/ingest",
            headers={
                "Authorization": f"Bearer {AXIOM_KEY}",
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
