import logging
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

class MQTTClient:
    def __init__(self, broker="localhost", port=1883):
        self.broker = broker
        self.port = port
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