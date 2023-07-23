import subprocess
from flask import Flask, request

app = Flask(__name__)


def call_sandbox():
    pass


@app.route("/api/exec", methods=["POST"])
def exec():
    code = request.get_json()["code"]
    proc = subprocess.Popen(
        ["python", "./lib/sandbox.py", code],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        out, err = proc.communicate(code, timeout=2)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
    return f"{out.decode()}\n{err.decode()}"
