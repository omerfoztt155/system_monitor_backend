import platform
import psutil

class Sensor:
    def __init__(self, device_code: str):
        self.device_code = device_code
        self.disk_path = "C:\\" if platform.system() == "Windows" else "/"

    def get_cpu_usage(self) -> float:
        return psutil.cpu_percent(interval=1)

    def get_ram_usage(self) -> float:
        return psutil.virtual_memory().percent

    def get_disk_usage(self) -> float:
        return psutil.disk_usage(self.disk_path).percent

    def get_data(self) -> dict:
        return {
            "device_code": self.device_code,
            "cpu_usage": self.get_cpu_usage(),
            "ram_usage": self.get_ram_usage(),
            "disk_usage": self.get_disk_usage()
        }