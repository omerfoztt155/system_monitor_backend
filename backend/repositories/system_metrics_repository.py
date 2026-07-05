from backend.database import get_connection
from backend.models.system_metric import SystemMetric

class SystemMetricsRepository:
    def save(self, metric: SystemMetric):
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

    def find_latest(self) -> SystemMetric | None:
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
            
    def find_all(self) -> list[SystemMetric]:
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