import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time
from hx711 import HX711

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
# GPIO.cleanup()

broker = "broker.hivemq.com"
port = 1883

hx = HX711(dout_pin=6, pd_sck_pin=5)


def on_message(client, usrdata, message):
    print("Receive : " + str(message.payload.decode()) + "\n")
    if(message.payload.decode() == "0"):
        client.publish("Magna/LampSta", "0")
        GPIO.output(18, False)
    else:
        client.publish("Magna/LampSta", "1")
        GPIO.output(18, True)
        # reading = hx.get_raw_data()
        # print(reading[0])
        # client.publish("Load", str(reading[0]))

def on_connect(client, usrdata, flags, rc):
    if rc == 0:
        print("Successfully Connected")
    else:
        print("Error")
        


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

client = mqtt.Client()
# client.username_pw_set(username="kmitliot",password="KMITL@iot1234")
client.on_connect = on_connect

client.on_message = on_message


client.connect(broker, port)
client.subscribe("Magna/LampCmd", 0)

# Loop forever
while True:
    client.loop_start()

    reading = hx.get_raw_data()
    weight_reading = reading[0]     # Adjust the value output as desired (diving by 100 or so)

    # Adjust the weight_reading value as needed (I set it 2250 for testing purpose solely, since the readings are inaccurate)
    if weight_reading > 2250:
        client.publish("Load", str(weight_reading))
        print("Weight reading published successfully:", weight_reading)
    else:
        print("Weight reading is below 2250. Not publishing.")

    time.sleep(0.1)

    # Stop MQTT client loop to ensure connection maintenance
    client.loop_stop()

# client.loop_forever()