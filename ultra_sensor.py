import RPi.GPIO as GPIO
import time
from hcsr04sensor import sensor

# set gpio pins
PIN = 17
echo = 27

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # use GPIO.BOARD for board pin values
x = sensor.Measurement

while True:
    
    distance = round(x.basic_distance(PIN, echo),2)
    
    if distance <= 28.4:
        print("Item detected")
        
    print("The distance at  20 Celsius is {} cm's".format(distance))
    # cleanup gpio pins.
    GPIO.cleanup((PIN, echo))
    
    time.sleep(1)
    