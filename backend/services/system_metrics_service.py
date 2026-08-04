import json
import logging
from datetime import datetime
from backend.exceptions import DeviceNotFoundError, InvalidPayloadError
from backend.models.system_metric import SystemMetric
from backend.repositories.device_repository import DeviceRepository
from backend.repositories.system_metrics_repository import SystemMetricsRepository

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = ("device_code", "cpu_usage", "ram_usage", "disk_usage")

class SystemMetricsService:
    def __init__(self, device_repository=None, system_metrics_repository=None):
        # Defaults to the real repositories (unchanged behavior for
        # main.py / run_backend.py / api/main.py). Tests pass in fakes
        # here so they never touch a real database.
        self.device_repository = device_repository or DeviceRepository()
        self.system_metrics_repository = system_metrics_repository or SystemMetricsRepository()

    def process(self, payload: str):
        data = self._parse_payload(payload)

        device = self.device_repository.find_by_device_code(data["device_code"])
        # NOTE: DatabaseError from the repository is intentionally NOT caught
        # here — it propagates to the caller (the MQTT handler), which is the
        # layer that decides how to react to infrastructure failures.

        if device is None:
            raise DeviceNotFoundError(data["device_code"])

        metric = SystemMetric(
            id=None,
            device_id=device.id,
            cpu_usage=data["cpu_usage"],
            ram_usage=data["ram_usage"],
            disk_usage=data["disk_usage"],
            received_at=datetime.now()
        )

        self.system_metrics_repository.save(metric)

        logger.info(
            "Saved metric for device_code='%s' (device_id=%s)",
            data["device_code"], device.id
        )

    def _parse_payload(self, payload: str) -> dict:
        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise InvalidPayloadError(f"Payload is not valid JSON: {exc}") from exc

        if not isinstance(data, dict):
            raise InvalidPayloadError(
                f"Expected a JSON object, got {type(data).__name__}"
            )

        missing = [field for field in REQUIRED_FIELDS if field not in data]
        if missing:
            raise InvalidPayloadError(f"Payload missing required field(s): {missing}")

        for field in ("cpu_usage", "ram_usage", "disk_usage"):
            if not isinstance(data[field], (int, float)):
                raise InvalidPayloadError(
                    f"Field '{field}' must be a number, got {type(data[field]).__name__}"
                )

        return data

    def get_latest(self) -> SystemMetric | None:
        return self.system_metrics_repository.find_latest()

    def get_all(self) -> list[SystemMetric]:
        return self.system_metrics_repository.find_all()