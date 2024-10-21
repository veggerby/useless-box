from machine import Pin, SoftI2C
from apds9960.const import *
from apds9960 import uAPDS9960 as APDS9960

class ProximitySensor:
    def __init__(self, sda_pin, scl_pin, threshold=50):
        """
        Initializes the APDS9960 proximity sensor.
        :param sda_pin: The GPIO pin used for the I2C data line (SDA).
        :param scl_pin: The GPIO pin used for the I2C clock line (SCL).
        :param threshold: The low threshold for proximity interrupt.
        """
        self.bus = SoftI2C(sda=Pin(sda_pin), scl=Pin(scl_pin))
        self.sensor = APDS9960(self.bus)
        self.sensor.setProximityIntLowThreshold(threshold)
        self.sensor.enableProximitySensor()

    def read_proximity(self):
        """
        Reads the proximity value from the sensor.
        :return: An integer representing the proximity value (0-255).
        """
        return self.sensor.readProximity()