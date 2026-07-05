import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, broker="localhost", port=1883):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client()

    def connect(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()