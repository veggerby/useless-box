import time
from arm_lid import LidArm
from arm_switch import SwitchArm
from proximity import ProximitySensor
from switch import ToggleSwitch

class UselessBox:
    def __init__(self, switch_pin, lid_pin, sda_pin, scl_pin, toggle_pin):
        self.switch_arm = SwitchArm(switch_pin)
        self.lid_arm = LidArm(lid_pin)
        self.proximity_sensor = ProximitySensor(sda_pin, scl_pin)
        self.toggle_switch = ToggleSwitch(toggle_pin)

    def open_lid(self, percentage, duration):
        """
        Opens the lid to the specified percentage over a given duration.
        """
        print(f"Opening lid to {percentage}% over {duration}ms.")
        self.lid_arm.open(percentage, duration)

    def close_lid(self, percentage, duration):
        """
        Closes the lid to the specified percentage over a given duration.
        """
        print(f"Closing lid to {percentage}% over {duration}ms.")
        self.lid_arm.close(percentage, duration)

    def switch_off(self, duration):
        """
        Extends the switch arm to turn off the toggle.
        """
        print("Extending switch arm to turn off the toggle.")
        self.switch_arm.extend(100, duration)
        time.sleep(0.5)
        self.switch_arm.retract(100, duration)

    def play_peekaboo(self):
        """
        Performs the peek-a-boo sequence.
        """
        print("Playing peek-a-boo!")
        self.lid_arm.open(50, 300)
        time.sleep(0.5)
        self.lid_arm.close(0, 300)

    def tease(self):
        """
        Performs a teasing sequence when the hand is detected at a medium distance.
        """
        print("Teasing the user!")
        self.lid_arm.open(30, 300)
        time.sleep(0.3)
        self.lid_arm.close(0, 300)

    def threatening_tease(self):
        """
        A more involved teasing sequence where the switch arm moves partially.
        """
        print("Threatening to switch off!")
        self.lid_arm.open(100, 500)
        self.switch_arm.extend(50, 300)
        time.sleep(0.5)
        self.switch_arm.retract(50, 300)
        self.lid_arm.close(0, 500)

    def get_proximity(self):
        """
        Returns the proximity reading from the sensor.
        """
        return self.proximity_sensor.read_proximity()

    def get_switch_state(self):
        """
        Returns the current state of the switch.
        """
        return self.toggle_switch.is_on()
