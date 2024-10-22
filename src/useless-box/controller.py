import random
import time
from arm_lid import LidArm
from arm_switch import SwitchArm
from proximity import ProximitySensor, ProximityState
from switch import ToggleSwitch
from led import LED
from useless_box import UselessBox

class UselessBoxController:
    PEEKABOO_PROBABILITY = 0.05  # Probability for peek-a-boo (5%)
    THREATEN_PROBABILITY = 0.2   # Probability for threatening movement (20%)
    PEEKABOO_RARE_PROBABILITY = 0.01  # Probability when hand is very close (1%)

    IDLE = 0
    LID_OPEN = 1
    TEASING = 2
    SWITCH_OFF = 3

    def __init__(self, switch_pin, lid_pin, sda_pin, scl_pin, toggle_pin, led_pin, inactivity_timeout=5):
        """
        Initializes the UselessBoxController with the necessary components.
        :param switch_pin: GPIO pin connected to the switch arm servo.
        :param lid_pin: GPIO pin connected to the lid arm servo.
        :param sda_pin: GPIO pin used for the I2C data line (SDA).
        :param scl_pin: GPIO pin used for the I2C clock line (SCL).
        :param toggle_pin: GPIO pin connected to the toggle switch.
        :param led_pin: GPIO pin connected to the LED.
        :param inactivity_timeout: Time in seconds before the lid closes automatically if no interaction occurs.
        """
        self.box = UselessBox(switch_pin, lid_pin, sda_pin, scl_pin, toggle_pin)
        self.led = LED(led_pin)  # Initialize the onboard LED
        self.state = UselessBoxController.IDLE
        self.last_proximity = ProximityState.NO_DETECTION
        self.last_switch_state = None
        self.inactivity_timeout = inactivity_timeout  # Inactivity timeout in seconds
        self.last_interaction_time = time.time()  # Track the last time an interaction occurred

    def run(self):
        """
        Main method to run the interactive sequences based on user input.
        """
        while True:
            self.update()

    def update(self):
        """
        Updates the box's behavior based on the state of the toggle switch and proximity sensor.
        """
        current_switch = self.box.get_switch_state()
        proximity = self.box.get_proximity()

        # Output the actual proximity state for feedback
        if proximity != self.last_proximity:
            print(f"Proximity state: {proximity}")

        # Check for interactions and update the state
        if current_switch and not self.last_switch_state:
            self.state = UselessBoxController.SWITCH_OFF
            self.led.on()  # Turn on the LED when the switch is turned on
            self._handle_switch_toggle()
            self._reset_inactivity_timer()

        elif proximity == ProximityState.VERY_CLOSE and self.state == UselessBoxController.IDLE:
            # Occasionally play peek-a-boo (5% chance)
            if random.random() < UselessBoxController.PEEKABOO_PROBABILITY:
                self.state = UselessBoxController.LID_OPEN
                self._handle_peekaboo()
                self._reset_inactivity_timer()
            # Occasionally move the switch arm to a threatening position (20% chance)
            elif random.random() < UselessBoxController.THREATEN_PROBABILITY:
                print("Threatening to switch off!")
                self._handle_threaten()
                self._reset_inactivity_timer()
            else:
                print("Hand detected very close, but not playing peek-a-boo or threatening this time.")

        elif proximity == ProximityState.CLOSE and self.state == UselessBoxController.IDLE:
            self.state = UselessBoxController.TEASING
            self._handle_tease()
            self._reset_inactivity_timer()

        elif proximity == ProximityState.FAR and self.state != UselessBoxController.IDLE:
            self.state = UselessBoxController.IDLE
            self.led.off()  # Turn off the LED when returning to idle
            self._handle_close_lid()
            self._reset_inactivity_timer()

        # If proximity is very close, ensure the lid stays closed and occasionally blink the LED
        elif proximity == ProximityState.VERY_CLOSE:
            if self.state != UselessBoxController.IDLE:
                print("Hand too close, keeping the lid closed.")
                self._handle_close_lid()
                self.led.off()
            # Occasionally do a peek-a-boo, even when proximity is very close, and blink the LED
            elif random.random() < UselessBoxController.PEEKABOO_RARE_PROBABILITY:
                self.led.toggle()  # Blink the LED occasionally
                self.state = UselessBoxController.LID_OPEN
                self._handle_peekaboo()
                self._reset_inactivity_timer()

        # Check if the inactivity timeout has been reached and close the lid if necessary
        if time.time() - self.last_interaction_time > self.inactivity_timeout:
            print("No interaction detected for a while. Closing the lid.")
            self._handle_close_lid()

        self.last_switch_state = current_switch
        self.last_proximity = proximity
        time.sleep(0.2)  # Small delay for responsiveness

    def _handle_switch_toggle(self):
        """
        Handles the switch toggle interaction.
        """
        print("Switch turned on, turning it off.")
        self.box.open_lid(100, 500)
        self.box.switch_off(500)
        self.box.close_lid(100, 500)  # Close the lid fully
        self.led.off()  # Turn off the LED after handling the toggle
        self.state = UselessBoxController.IDLE

    def _handle_peekaboo(self):
        """
        Handles the peek-a-boo interaction.
        """
        self.box.play_peekaboo()
        self.state = UselessBoxController.IDLE

    def _handle_tease(self):
        """
        Handles the teasing interaction.
        """
        self.box.tease()
        self.state = UselessBoxController.IDLE

    def _handle_threaten(self):
        """
        Handles the threatening movement of the switch arm.
        Ensures the lid is open before threatening.
        """
        if not self.box.lid_arm.is_open():  # Check if the lid is already open
            self.box.open_lid(100, 500)  # Open the lid fully if it's not

        self.box.switch_arm.extend(50, 300)  # Move arm halfway as if threatening to switch
        time.sleep(0.5)
        self.box.switch_arm.retract(50, 300)

    def _handle_close_lid(self):
        """
        Handles closing the lid when no hand is detected close or after inactivity.
        Ensures the switch arm is retracted before closing the lid.
        """
        print("Retracting switch arm and closing lid.")
        self.box.switch_arm.retract(100, 300)  # Ensure the switch arm is fully retracted
        self.box.close_lid(100, 500)  # Fully close the lid (100%)
        self.state = UselessBoxController.IDLE

    def _reset_inactivity_timer(self):
        """
        Resets the inactivity timer to the current time.
        """
        self.last_interaction_time = time.time()

if __name__ == "__main__":
    controller = UselessBoxController(
        switch_pin=0,
        lid_pin=2,
        sda_pin=6,
        scl_pin=7,
        toggle_pin=21,
        led_pin=8,
        inactivity_timeout=5  # Set to 5 seconds, but you can adjust as needed
    )
    controller.run()
