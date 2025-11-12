from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# Attach Prometheus metrics exporter
metrics = PrometheusMetrics(app)
metrics.info("app_info", "Application info", version="1.0.0")

@app.route('/')
def home():
    return jsonify({
        "message": "Hello from Flask!",
        "status": "ok"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
