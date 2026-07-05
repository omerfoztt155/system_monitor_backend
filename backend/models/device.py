from dataclasses import dataclass

@dataclass
class Device:
    id: int | None
    device_code: str
    location: str