# main.py -- put your code here!

from time import sleep

from machine import Pin, SoftI2C

from apds9960.const import *
from apds9960 import uAPDS9960 as APDS9960

print("Gesture Test")
print("============")

bus = SoftI2C(sda=Pin(6), scl=Pin(7))

apds = APDS9960(bus)

dirs = {
    APDS9960_DIR_NONE: "none",
    APDS9960_DIR_LEFT: "left",
    APDS9960_DIR_RIGHT: "right",
    APDS9960_DIR_UP: "up",
    APDS9960_DIR_DOWN: "down",
    APDS9960_DIR_NEAR: "near",
    APDS9960_DIR_FAR: "far",
}

apds.setProximityIntLowThreshold(50)

apds.enableGestureSensor()

while True:
    sleep(0.5)
    if apds.isGestureAvailable():
        motion = apds.readGesture()
        print("Gesture={}".format(dirs.get(motion, "unknown")))
