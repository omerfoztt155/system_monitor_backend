import time
from mqtt.subscriber import Subscriber

def main():
    subscriber = Subscriber()
    subscriber.connect()
    subscriber.subscribe("iot/sensors")

    print("Backend dinleniyor...")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nBackend kapatiliyor...")

    finally:
        subscriber.disconnect()


if __name__ == "__main__":
    main()