from flask import Flask, request

app = Flask(__name__)


@app.route("/api/exec", methods=['POST'])
def hello_world():
    return str(request.json())
