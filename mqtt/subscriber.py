from backend.services.system_metrics_service import SystemMetricsService
from mqtt.client import MQTTClient

class Subscriber(MQTTClient):

    def __init__(self):
        super().__init__()
        self.system_metrics_service = SystemMetricsService()

    def subscribe(self, topic: str):

        self.client.subscribe(topic)

        def on_message(client, userdata, message):

            payload = message.payload.decode()

            self.system_metrics_service.process(payload)

        self.client.on_message = on_message