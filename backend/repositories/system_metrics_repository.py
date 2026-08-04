import logging
import psycopg
from backend.database import get_connection
from backend.exceptions import DatabaseError
from backend.models.system_metric import SystemMetric

logger = logging.getLogger(__name__)

class SystemMetricsRepository:
    def save(self, metric: SystemMetric):
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO system_metrics
                        (device_id, cpu_usage, ram_usage, disk_usage, received_at)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            metric.device_id,
                            metric.cpu_usage,
                            metric.ram_usage,
                            metric.disk_usage,
                            metric.received_at
                        )
                    )
                    conn.commit()
        except psycopg.Error as exc:
            logger.error(
                "Database error while saving metric for device_id=%s: %s",
                metric.device_id, exc
            )
            raise DatabaseError("Failed to save system metric") from exc

    def find_latest(self) -> SystemMetric | None:
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id, device_id, cpu_usage, ram_usage, disk_usage, received_at
                        FROM system_metrics
                        ORDER BY id DESC
                        LIMIT 1
                        """
                    )
                    row = cursor.fetchone()

                    if row is None:
                        return None

                    return SystemMetric(
                        id=row[0], device_id=row[1], cpu_usage=row[2],
                        ram_usage=row[3], disk_usage=row[4], received_at=row[5]
                    )
        except psycopg.Error as exc:
            logger.error("Database error while fetching latest metric: %s", exc)
            raise DatabaseError("Failed to fetch latest metric") from exc

    def find_all(self) -> list[SystemMetric]:
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:

                    cursor.execute(
                        """
                        SELECT
                            id,
                            device_id,
                            cpu_usage,
                            ram_usage,
                            disk_usage,
                            received_at
                        FROM system_metrics
                        ORDER BY id DESC
                        """
                    )

                    rows = cursor.fetchall()

                    metrics = []

                    for row in rows:
                        metrics.append(
                            SystemMetric(
                                id=row[0],
                                device_id=row[1],
                                cpu_usage=row[2],
                                ram_usage=row[3],
                                disk_usage=row[4],
                                received_at=row[5]
                            )
                        )

                    return metrics
        except psycopg.Error as exc:
            logger.error("Database error while listing metrics: %s", exc)
            raise DatabaseError("Failed to list metrics") from exc