import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from rpi_rf import RFDevice

### MQTT
MQTT_BROKER = "192.168.1.164"
MQTT_TOPIC = "rpi-rf"
MQTT_MESSAGE = "Capture on RF"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    payload = str(msg.payload.decode("ascii"))  # decode the binary string
    print(msg.topic + " " + payload)


## RF and PI
RF_CODE_OF_INTEREST = "9181186"  # The code to wait for
GPIO_PIN = 27  # the data pin of your rf recevier
SLEEP_BETWEEN_SIGNALS = (
    1
)  # Seconds, the time to sleep after detecting a signal of interest.


def main():
    # Setup MQTT
    client = mqtt.Client()
    client.on_connect = on_connect  # call these on connect and on message
    client.on_message = on_message
    # client.username_pw_set(username='user', password='pass')  # need this
    client.connect(MQTT_BROKER)
    # client.loop_forever()    #  don't get past this
    client.loop_start()  # run in background and free up main thread

    # Setup RF
    timestamp = None  # Keep track of the time of the last received message on a code.
    rfdevice = RFDevice(GPIO_PIN)
    rfdevice.enable_rx()
    while True:
        if rfdevice.rx_code_timestamp != timestamp:  # a new code is received
            timestamp = rfdevice.rx_code_timestamp
            if str(rfdevice.rx_code) == RF_CODE_OF_INTEREST:
                client.publish(MQTT_TOPIC, MQTT_MESSAGE)
                time.sleep(SLEEP_BETWEEN_SIGNALS)


if __name__ == "__main__":
    main()
