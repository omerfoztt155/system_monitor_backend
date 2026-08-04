class SystemMonitorError(Exception):
    """Base exception for all application-specific errors.

    Catching this at an entrypoint (MQTT handler, API route) guarantees
    you've handled every "expected" failure mode of this app, as opposed
    to catching bare Exception which would also swallow real bugs.
    """

class InvalidPayloadError(SystemMonitorError):
    """Raised when an incoming MQTT payload is malformed, not valid JSON,
    or missing required fields."""

class DeviceNotFoundError(SystemMonitorError):
    """Raised when a device_code has no matching registered device."""

    def __init__(self, device_code: str):
        self.device_code = device_code
        super().__init__(f"No registered device found for device_code='{device_code}'")

class DatabaseError(SystemMonitorError):
    """Raised when a database operation fails (connection lost, query
    failed, pool exhausted, etc).

    Wraps the original driver exception so we never leak psycopg
    internals to callers, while still preserving it for logging via
    `raise DatabaseError(...) from original_exception`.
    """