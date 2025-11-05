#!/usr/bin/env python3
# main.py
import os
from flask import Flask, jsonify
from asgiref.wsgi import WsgiToAsgi
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
import psutil

APP_VERSION = os.getenv("APP_VERSION", "1.0")
APP_TITLE   = os.getenv("APP_TITLE", "Devops for Cloud Assignment")
POD_NAME    = os.getenv("HOSTNAME") or os.uname().nodename

REQUEST_COUNT = Counter("get_info_requests_total", "Total /get_info requests", ["pod", "version"])
CPU_PERCENT   = Gauge("process_cpu_percent", "Process CPU percent (per replica)", ["pod", "version"])
RSS_BYTES     = Gauge("process_rss_bytes", "Resident set size in bytes (per replica)", ["pod", "version"])

app = Flask(__name__)

@app.route("/get_info", methods=["GET"])
def get_info():
    REQUEST_COUNT.labels(pod=POD_NAME, version=APP_VERSION).inc()
    p = psutil.Process(os.getpid())
    RSS_BYTES.labels(pod=POD_NAME, version=APP_VERSION).set(p.memory_info().rss)
    CPU_PERCENT.labels(pod=POD_NAME, version=APP_VERSION).set(p.cpu_percent(interval=0.0))
    return jsonify({"APP_VERSION": APP_VERSION, "APP_TITLE": APP_TITLE, "pod": POD_NAME}), 200

def metrics_app(environ, start_response):
    data = generate_latest()
    start_response("200 OK", [("Content-Type", CONTENT_TYPE_LATEST)])
    return [data]

application = DispatcherMiddleware(app, {"/metrics": metrics_app})
asgi_app = WsgiToAsgi(application)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:asgi_app", host="0.0.0.0", port=8000, reload=False)
