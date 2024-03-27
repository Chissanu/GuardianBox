import RPi.GPIO as GPIO

class Contoller():
    def __init__(self, led_pin):   
        self.led_pin = led_pin
        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)

    def turn_on(self):
        GPIO.output(self.led_pin, True)

    def turn_off(self):
        GPIO.output(self.led_pin, False)
