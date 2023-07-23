import subprocess
from flask import Flask, request

app = Flask(__name__)


def call_sandbox():
    pass


@app.route("/api/exec", methods=['POST'])
def exec():
    code = request.get_json()['code']
    proc = subprocess.Popen(["ls", "-a"])
    try:
        out, err = proc.communicate(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
    print(out, err)
    return f'''
(stdout)
{out}
(stderr)
{err}
'''
