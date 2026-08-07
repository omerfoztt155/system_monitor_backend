import logging
import os
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

class MQTTClient:
    def __init__(self, broker=None, port=None):
        self.broker = broker or os.getenv("MQTT_BROKER_HOST", "localhost")
        self.port = port or int(os.getenv("MQTT_BROKER_PORT", "1883"))
        self.client = mqtt.Client()

    def connect(self):
        try:
            self.client.connect(self.broker, self.port)
        except (ConnectionRefusedError, OSError) as exc:
            logger.error(
                "Could not connect to MQTT broker at %s:%s — is it running? (%s)",
                self.broker, self.port, exc
            )
            raise

        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()