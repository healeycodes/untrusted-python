import subprocess
from flask import Flask, request

app = Flask(__name__)


@app.route("/api/exec", methods=['POST'])
def exec():
    code = request.get_json()['code']
    proc = subprocess.Popen(["ls -a"])
    try:
        out, err = proc.communicate(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
    return f'''
(stdout)
{out}
(stderr)
{err}
(code)
{code}
'''
