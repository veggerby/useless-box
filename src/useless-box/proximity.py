from machine import Pin, SoftI2C
from apds9960.const import *
from apds9960 import uAPDS9960 as APDS9960

# Simple class to simulate an enumeration
class ProximityState:
    VERY_CLOSE = "VERY_CLOSE"
    CLOSE = "CLOSE"
    FAR = "FAR"
    NO_DETECTION = "NO_DETECTION"

class ProximitySensor:
    def __init__(self, sda_pin, scl_pin, very_close_threshold=200, close_threshold=100, far_threshold=50):
        """
        Initializes the APDS9960 proximity sensor.
        :param sda_pin: The GPIO pin used for the I2C data line (SDA).
        :param scl_pin: The GPIO pin used for the I2C clock line (SCL).
        :param very_close_threshold: The threshold value for "very close" proximity.
        :param close_threshold: The threshold value for "close" proximity.
        :param far_threshold: The threshold value for "far" proximity.
        """
        self.bus = SoftI2C(sda=Pin(sda_pin), scl=Pin(scl_pin))
        self.sensor = APDS9960(self.bus)
        self.sensor.setProximityIntLowThreshold(50)
        self.sensor.enableProximitySensor()

        self.very_close_threshold = very_close_threshold
        self.close_threshold = close_threshold
        self.far_threshold = far_threshold

    def read_proximity(self):
        """
        Reads the proximity value from the sensor and returns a ProximityState.
        :return: A string indicating the proximity level.
        """
        proximity_value = self.sensor.readProximity()
        if proximity_value >= self.very_close_threshold:
            return ProximityState.VERY_CLOSE
        elif proximity_value >= self.close_threshold:
            return ProximityState.CLOSE
        elif proximity_value >= self.far_threshold:
            return ProximityState.FAR
        else:
            return ProximityState.NO_DETECTION
