import logging
from backend.exceptions import DatabaseError, DeviceNotFoundError, InvalidPayloadError
from backend.services.system_metrics_service import SystemMetricsService
from mqtt.client import MQTTClient

logger = logging.getLogger(__name__)

class Subscriber(MQTTClient):
    def __init__(self):
        super().__init__()
        self.system_metrics_service = SystemMetricsService()

    def subscribe(self, topic: str):

        self.client.subscribe(topic)

        def on_message(client, userdata, message):

            payload = message.payload.decode()

            try:
                self.system_metrics_service.process(payload)

            except InvalidPayloadError as exc:
                # Expected, "bad data" case — log and move on, don't crash.
                logger.warning(
                    "Discarding invalid payload on topic '%s': %s",
                    message.topic, exc
                )

            except DeviceNotFoundError as exc:
                # Also expected — an unregistered sensor is sending data.
                logger.warning("Discarding message: %s", exc)

            except DatabaseError as exc:
                # Infrastructure failure — worth an ERROR, not a crash.
                # The message is lost, but the subscriber keeps listening
                # for the next one instead of dying entirely.
                logger.error(
                    "Could not persist metric due to a database error: %s", exc
                )

            except Exception:
                # Anything we didn't anticipate. logger.exception() records
                # the full traceback so it's still debuggable, but the
                # subscriber itself stays alive.
                logger.exception(
                    "Unexpected error while processing message on topic '%s'",
                    message.topic
                )

        self.client.on_message = on_message