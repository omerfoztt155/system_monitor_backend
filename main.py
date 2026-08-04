import logging
import time
from backend.logging_config import configure_logging
from mqtt.publisher import Publisher
from sensor.sensor import Sensor

configure_logging()
logger = logging.getLogger(__name__)

def main():
    sensor = Sensor("laptop-01")
    publisher = Publisher()
    publisher.connect()

    try:
        while True:
            data = sensor.get_data()

            publisher.publish("iot/sensors", data)

            logger.info("Gönderildi -> %s", data)

            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Program kapatiliyor...")

    finally:
        publisher.disconnect()

if __name__ == "__main__":
    main()