from fastapi import FastAPI
from backend.services.system_metrics_service import SystemMetricsService

app = FastAPI()
system_metrics_service = SystemMetricsService()

@app.get("/")
def root():
    return {
        "message": "IoT Backend API"
    }

@app.get("/metrics/latest")
def get_latest_metric():

    metric = system_metrics_service.get_latest()

    if metric is None:
        return {
            "message": "No metrics found."
        }

    return {
        "id": metric.id,
        "device_id": metric.device_id,
        "cpu_usage": metric.cpu_usage,
        "ram_usage": metric.ram_usage,
        "disk_usage": metric.disk_usage,
        "received_at": metric.received_at
    }

@app.get("/metrics")
def get_all_metrics():

    metrics = system_metrics_service.get_all()

    response = []

    for metric in metrics:

        response.append(
            {
                "id": metric.id,
                "device_id": metric.device_id,
                "cpu_usage": metric.cpu_usage,
                "ram_usage": metric.ram_usage,
                "disk_usage": metric.disk_usage,
                "received_at": metric.received_at
            }
        )

    return response