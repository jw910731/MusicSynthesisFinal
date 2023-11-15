from flask import Flask, send_from_directory

app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory('../../web/build', "index.html")


@app.route("/<path:path>")
def base(path):
    return send_from_directory('../../web/build', path)
