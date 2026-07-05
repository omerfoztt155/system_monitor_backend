from backend.database import get_connection
from backend.models.device import Device

class DeviceRepository:

    def find_by_device_code(self, device_code: str) -> Device | None:
        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT id, device_code, location
                    FROM devices
                    WHERE device_code = %s
                    """,
                    (device_code,)
                )

                row = cursor.fetchone()

                if row is None:
                    return None

                return Device(
                    id=row[0],
                    device_code=row[1],
                    location=row[2]
                )
    
    def find_all(self) -> list[Device]:
        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT id, device_code, location
                    FROM devices
                    ORDER BY id
                    """
                )

                rows = cursor.fetchall()

                devices = []

                for row in rows:
                    devices.append(
                        Device(
                            id=row[0],
                            device_code=row[1],
                            location=row[2]
                        )
                    )

                return devices