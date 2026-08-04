import logging
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from backend.exceptions import DatabaseError, DeviceNotFoundError, SystemMonitorError
from backend.logging_config import configure_logging
from backend.services.system_metrics_service import SystemMetricsService

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
system_metrics_service = SystemMetricsService()
STATIC_DIR = Path(__file__).resolve().parent / "static"

# --- Exception handlers -----------------------------------------------
# Registered from most specific to least specific. FastAPI/Starlette
# matches the exact exception type first, so a route can `raise
# DatabaseError(...)` and this handler runs without any try/except
# needed in the route itself.

@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError):
    logger.error("Database error on %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=503,
        content={"detail": "Service temporarily unavailable. Please try again later."},
    )


@app.exception_handler(DeviceNotFoundError)
async def device_not_found_handler(request: Request, exc: DeviceNotFoundError):
    logger.warning("Device not found on %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )

@app.exception_handler(SystemMonitorError)
async def system_monitor_error_handler(request: Request, exc: SystemMonitorError):
    # Catch-all for any other domain error we haven't special-cased above,
    # e.g. InvalidPayloadError if a future route ever accepts raw payloads.
    logger.error(
        "Unhandled application error on %s %s: %s", request.method, request.url.path, exc
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal error occurred."},
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Truly unexpected bugs (not one of our domain exceptions). Log the
    # full traceback for debugging, but never leak it to the client.
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )

# --- Routes --------------------------------------------------------------

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

@app.get("/dashboard")
def dashboard():
    return FileResponse(STATIC_DIR / "dashboard.html")