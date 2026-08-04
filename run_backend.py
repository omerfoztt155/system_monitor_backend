import logging
import time
from backend.logging_config import configure_logging
from mqtt.subscriber import Subscriber

configure_logging()
logger = logging.getLogger(__name__)

def main():
    subscriber = Subscriber()
    subscriber.connect()
    subscriber.subscribe("iot/sensors")
    logger.info("Backend dinleniyor...")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Backend kapatiliyor...")

    finally:
        subscriber.disconnect()

if __name__ == "__main__":
    main()