from machine import Pin

class LED:
    def __init__(self, pin_number=8):
        """
        Initializes the onboard LED.
        :param pin_number: The GPIO pin connected to the onboard LED (default is 8).
        """
        self.led = Pin(pin_number, Pin.OUT)
        self.state = False  # False means off (LED is physically on)

    def on(self):
        """
        Turns the LED on (actually off because of the inversion).
        """
        self.led.value(0)  # Inverted pin, 0 means on
        self.state = True
        print("LED is ON (physically OFF)")

    def off(self):
        """
        Turns the LED off (actually on because of the inversion).
        """
        self.led.value(1)  # Inverted pin, 1 means off
        self.state = False
        print("LED is OFF (physically ON)")

    def toggle(self):
        """
        Toggles the state of the LED.
        """
        if self.state:
            self.off()
        else:
            self.on()

if __name__ == "__main__":
    led = LED()

    # Test the LED methods
    led.on()    # This will turn the LED off physically (logically on)
    led.off()   # This will turn the LED on physically (logically off)
    led.toggle() # Toggles the LED state
