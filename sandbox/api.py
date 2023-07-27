import os
import sys
import subprocess
from flask_cors import CORS
from flask import Flask, request

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
        }
    )

    extra = ""
    try:
        stdout, stderr = proc.communicate(code, timeout=2)
    except subprocess.TimeoutExpired:
        extra = "process timed out"
        proc.kill()
        stdout, stderr = proc.communicate()
    return f"{stdout.decode()}\n{stderr.decode()}\n{extra}"
