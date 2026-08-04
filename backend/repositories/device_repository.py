import logging
import psycopg
from backend.database import get_connection
from backend.exceptions import DatabaseError
from backend.models.device import Device

logger = logging.getLogger(__name__)

class DeviceRepository:
    def find_by_device_code(self, device_code: str) -> Device | None:
        try:
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
        except psycopg.Error as exc:
            logger.error(
                "Database error while looking up device_code='%s': %s",
                device_code, exc
            )
            raise DatabaseError(
                f"Failed to look up device '{device_code}'"
            ) from exc

    def find_all(self) -> list[Device]:
        try:
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
        except psycopg.Error as exc:
            logger.error("Database error while listing devices: %s", exc)
            raise DatabaseError("Failed to list devices") from exc