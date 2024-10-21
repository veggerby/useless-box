# main.py -- put your code here!

from time import sleep

from machine import Pin, SoftI2C

from apds9960.const import *
from apds9960 import uAPDS9960 as APDS9960

print("Gesture Test")
print("============")

bus = SoftI2C(sda=Pin(6), scl=Pin(7))

apds = APDS9960(bus)

apds.setProximityIntLowThreshold(50)

print("Proximity Sensor Test")
print("=====================")
apds.enableProximitySensor()

oval = -1
while True:
    sleep(0.25)
    val = apds.readProximity()
    if val != oval:
        print("proximity={}".format(val))
        oval = val
