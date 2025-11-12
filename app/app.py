from flask import Flask, jsonify
import random, time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter("app_requests_total", "Total HTTP requests", ["endpoint", "method", "http_status"])
REQUEST_LATENCY = Histogram("app_request_latency_seconds", "Latency of requests", ["endpoint"])

@app.route("/")
def index():
    start = time.time()
    # simulate some work
    time.sleep(random.uniform(0.02, 0.15))
    REQUEST_COUNT.labels(endpoint="/", method="GET", http_status="200").inc()
    REQUEST_LATENCY.labels(endpoint="/").observe(time.time() - start)
    return jsonify({"status": "ok", "message": "Hello from Flask!"})

@app.route("/fail")
def fail():
    start = time.time()
    time.sleep(random.uniform(0.01, 0.05))
    REQUEST_COUNT.labels(endpoint="/fail", method="GET", http_status="500").inc()
    REQUEST_LATENCY.labels(endpoint="/fail").observe(time.time() - start)
    return jsonify({"status": "error"}), 500

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
