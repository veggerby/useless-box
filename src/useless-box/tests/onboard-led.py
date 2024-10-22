from machine import Pin
from time import sleep
#from neopixel import NeoPixel

led = Pin(8, Pin.OUT)
#np = NeoPixel(pin, 1)

while True:
    print(".")
    led.on()
    sleep(0.5)
    led.off()
    sleep(0.5)
