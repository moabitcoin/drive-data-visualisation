import io
import os
import sys
import json
from pathlib import Path

from flask import Flask, send_file, render_template, jsonify, abort

host, port = "0.0.0.0", 5000
db = json.load(Path(os.getenv("BLOCKAGES_DEMO_DB")).open())

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("map.html", token=os.getenv("MAPBOX_ACCESS_TOKEN"))


@app.route("/total")
def total():
    return jsonify(len(db))


@app.route("/location/<int:gid>")
def location(gid):
    return jsonify(db[gid]["location"])


@app.route("/frame/<int:gid>")
def frame(gid):
    return send_jpg(db[gid]["path"])


def send_jpg(path):
    return send_file(path, mimetype="image/jpeg")


@app.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = "*"
    return response


app.run(host=host, port=port, threaded=False)
