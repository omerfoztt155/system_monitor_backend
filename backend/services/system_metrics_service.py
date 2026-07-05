import json
from datetime import datetime
from backend.models.system_metric import SystemMetric
from backend.repositories.device_repository import DeviceRepository
from backend.repositories.system_metrics_repository import SystemMetricsRepository

class SystemMetricsService:
    def __init__(self):
        self.device_repository = DeviceRepository()
        self.system_metrics_repository = SystemMetricsRepository()

    def process(self, payload:str):
        data = json.loads(payload)

        device = self.device_repository.find_by_device_code(data["device_code"])

        if device is None:
            print(f"Unknown device: {data['device_code']}")
            return

        metric = SystemMetric(
            id=None,
            device_id=device.id,
            cpu_usage=data["cpu_usage"],
            ram_usage=data["ram_usage"],
            disk_usage=data["disk_usage"],
            received_at=datetime.now()
        )

        self.system_metrics_repository.save(metric)

        print("System metrics saved.")

    def get_latest(self) -> SystemMetric | None:
        return self.system_metrics_repository.find_latest()
    
    def get_all(self) -> list[SystemMetric]:
        return self.system_metrics_repository.find_all()