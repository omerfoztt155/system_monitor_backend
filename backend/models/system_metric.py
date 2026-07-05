from dataclasses import dataclass
from datetime import datetime

@dataclass
class SystemMetric:
    id: int | None
    device_id: int
    cpu_usage: float
    ram_usage: float
    disk_usage: float
    received_at: datetime