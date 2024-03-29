import RPi.GPIO as GPIO
import time
from hcsr04sensor import sensor

class Contoller():
    def __init__(self, led_pin, ultra_pin, echo_pin, mag_pin):   
        self.led_pin = led_pin
        self.ultra_pin = ultra_pin
        self.echo_pin = echo_pin
        self.mag_pin = mag_pin

        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.setup(self.mag_pin, GPIO.OUT)

    def turn_on(self):
        GPIO.output(self.led_pin, True)

    def turn_off(self):
        GPIO.output(self.led_pin, False)
    
    def read_ultrasonic(self):
        x = sensor.Measurement
        distance = x.basic_distance(self.ultra_pin, self.echo_pin)
        time.sleep(0.1)
        return round(distance,2)
    
    def mag_lock(self):
        GPIO.output(self.mag_pin, True)
        
    def mag_unlock(self):
        GPIO.output(self.mag_pin, False)

    
