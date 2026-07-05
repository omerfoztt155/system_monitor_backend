from sensor.sensor import Sensor
from mqtt.publisher import Publisher

import time

def main():
    sensor = Sensor("laptop-01")
    publisher = Publisher()

    publisher.connect()

    try:
        while True:
            data = sensor.get_data()

            publisher.publish("iot/sensors", data)

            print(f"Gönderildi -> {data}")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nProgram kapatiliyor...")

    finally:
        publisher.disconnect()


if __name__ == "__main__":
    main()