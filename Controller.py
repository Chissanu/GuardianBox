import RPi.GPIO as GPIO
import time
from hcsr04sensor import sensor

class Contoller():
    def __init__(self, led_pin, ultra_pin, echo_pin):   
        self.led_pin = led_pin
        self.ultra_pin = ultra_pin
        self.echo_pin = echo_pin

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ultra_pin, GPIO.OUT)  
        GPIO.setup(self.echo_pin, GPIO.IN) 
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.setup(21, GPIO.OUT)

    def turn_on(self):

        GPIO.output(self.led_pin, True)

    def turn_off(self):
        GPIO.output(self.led_pin, False)
    
    def read_ultrasonic(self):
        x = sensor.Measurement
        distance = x.basic_distance(self.ultra_pin, self.echo_pin)
        return round(distance,2)
    
    def mag_lock(self):
        GPIO.output(21, True)
        
    def mag_unlock(self):
        GPIO.output(21, False)

    
