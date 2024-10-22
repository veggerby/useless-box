from machine import Pin

class ToggleSwitch:
    def __init__(self, pin_number):
        """
        Initializes the toggle switch.
        :param pin_number: The GPIO pin connected to the toggle switch.
        """
        self.pin = Pin(pin_number, mode=Pin.IN, pull=Pin.PULL_DOWN)

    def is_on(self):
        """
        Checks if the toggle switch is in the "On" state.
        :return: True if the switch is "On", False otherwise.
        """
        return self.pin.value() < 0.5