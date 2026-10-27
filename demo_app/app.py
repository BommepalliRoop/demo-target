from flask import Flask, jsonify, request

from demo_app.importer import parse_import_payload
from demo_app.jobs import start_sync_job
from demo_app.utils import render_greeting

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/greet/<name>")
def greet(name):
    return render_greeting(name)


@app.route("/import", methods=["POST"])
def import_data():
    payload = parse_import_payload(request.get_data(as_text=True))
    return jsonify(imported=len(payload))


@app.route("/sync", methods=["POST"])
def sync():
    start_sync_job(request.get_json()["url"])
    return jsonify(started=True), 202
