import os
import subprocess
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/api/ping")
def ping():
    return ""


@app.route("/api/exec", methods=["POST"])
def exec():
    code = request.get_json()["code"]
    proc = subprocess.Popen(
        ["python3", "./sandbox.py", code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={
            "PATH": os.environ.get("PATH"),
        }
    )
    
    timeout = False
    try:
        out, err = proc.communicate(code, timeout=2)
    except subprocess.TimeoutExpired:
        timeout = True
        proc.kill()
        out, err = proc.communicate()
    return f"{out.decode()}\n{err.decode()}\n{'process timed out (you get ~2sec of wallclock time)' if timeout else ''}"
