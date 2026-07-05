import json

from mqtt.client import MQTTClient

class Publisher(MQTTClient):

    def publish(self, topic: str, data: dict):
        payload = json.dumps(data)
        self.client.publish(topic, payload)