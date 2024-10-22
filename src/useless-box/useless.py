import random
import time
from arm_lid import LidArm
from arm_switch import SwitchArm
from proximity import ProximitySensor
from switch import ToggleSwitch  # Import the new ToggleSwitch class

class UselessBox:
    def __init__(self, switch_pin, lid_pin, sda_pin, scl_pin, toggle_pin):
        """
        Initializes the UselessBox with switch, lid control, proximity sensor, and toggle switch.
        :param switch_pin: The GPIO pin connected to the switch arm servo.
        :param lid_pin: The GPIO pin connected to the lid arm servo.
        :param sda_pin: The GPIO pin used for the I2C data line (SDA).
        :param scl_pin: The GPIO pin used for the I2C clock line (SCL).
        :param toggle_pin: The GPIO pin connected to the toggle switch.
        """
        self.switch_arm = SwitchArm(switch_pin)
        self.lid_arm = LidArm(lid_pin)
        self.proximity_sensor = ProximitySensor(sda_pin, scl_pin)
        self.toggle_switch = ToggleSwitch(toggle_pin)
        self._behaviors = [
            self._behavior_peekaboo,
            self._behavior_slow_approach,
            self._behavior_quick_threat,
            self._behavior_double_fakeout,
            self._behavior_rapid_switch_off,
            self._behavior_insistent_switch,
            self._behavior_long_pause,
            self._behavior_random_lid_movement,
            self._behavior_slow_retract,
            self._behavior_triple_fake
        ]

    def open_lid(self, percentage, time_ms):
        """
        Opens the lid to the specified percentage over the given time in milliseconds.
        :param percentage: Percentage to open the lid (0 = closed, 100 = fully open).
        :param time_ms: Time in milliseconds it should take to open the lid.
        """
        print(f"Opening lid to {percentage}% over {time_ms}ms.")
        self.lid_arm.open(percentage, time_ms)

    def close_lid(self, percentage, time_ms):
        """
        Closes the lid to the specified percentage over the given time in milliseconds.
        :param percentage: Percentage to close the lid (0 = fully closed, 100 = fully open).
        :param time_ms: Time in milliseconds it should take to close the lid.
        """
        print(f"Closing lid to {percentage}% over {time_ms}ms.")
        self.lid_arm.close(percentage, time_ms)

    def get_proximity(self):
        """
        Returns the proximity reading from the sensor.
        :return: An integer from 0 to 255, where 100 indicates a hand in the vicinity and 255 means it's about 1cm away from the switch.
        """
        proximity_value = self.proximity_sensor.read_proximity()
        print(f"Proximity detected: {proximity_value}")
        return proximity_value

    def switch_arm_to_off(self, time_ms, percentage):
        """
        Moves the switch arm towards the "Off" position of the switch.
        :param time_ms: Time in milliseconds it should take to perform the switch movement.
        :param percentage: Percentage of the arm's movement towards switching off (0 = no movement, 100 = fully switched off).
        """
        print(f"Moving switch arm to {percentage}% over {time_ms}ms.")
        self.switch_arm.move(percentage, time_ms)

    def retract_arm(self, time_ms, percentage):
        """
        Retracts the arm away from the switch.
        :param time_ms: Time in milliseconds it should take to perform the retraction.
        :param percentage: Percentage of the arm's movement during retraction (0 = fully extended, 100 = fully retracted).
        """
        print(f"Retracting arm to {percentage}% over {time_ms}ms.")
        self.switch_arm.retract(percentage, time_ms)

    def get_switch(self):
        """
        Returns the current state of the switch.
        :return: True if the switch is "On" (requires arm to switch off), False if the switch is already "Off".
        """
        switch_value = self.toggle_switch.is_switch_on()
        print(f"Switch is currently {'On' if switch_value else 'Off'}.")
        return switch_value

    def random_behavior(self):
        behavior_choice = random.choice(self._behaviors)
        print(f"Executing behavior: {behavior_choice.__name__}")
        behavior_choice()

    def _behavior_peekaboo(self):
        self.open_lid(50, 500)
        if self.get_proximity() < 150:
            print("Hand detected nearby! Playing peek-a-boo!")
            self.close_lid(0, 300)
            time.sleep(0.5)
            self.open_lid(100, 500)
        else:
            self.open_lid(100, 500)
        if self.get_switch():
            self.switch_arm_to_off(500, 100)
        self.retract_arm(300, 100)
        self.close_lid(0, 500)

    def _behavior_slow_approach(self):
        self.open_lid(100, 1000)
        proximity = self.get_proximity()
        if proximity < 100:
            print("Hand detected! Approaching switch slowly...")
            self.switch_arm_to_off(1000, 50)
            if self.get_proximity() < 120:
                print("Hand is very close, retracting!")
                self.retract_arm(800, 50)
            else:
                print("Switching off halfway.")
                self.switch_arm_to_off(500, 100)
        else:
            if self.get_switch():
                self.switch_arm_to_off(800, 100)
        self.retract_arm(500, 100)
        self.close_lid(0, 700)

    def _behavior_quick_threat(self):
        self.open_lid(100, 300)
        if self.get_proximity() < 120:
            print("Threat detected, quick switch off attempt!")
            self.switch_arm_to_off(300, 70)
            self.retract_arm(200, 70)
            if self.get_switch():
                self.switch_arm_to_off(300, 100)
        else:
            if self.get_switch():
                self.switch_arm_to_off(500, 100)
        self.retract_arm(300, 100)
        self.close_lid(0, 500)

    def _behavior_double_fakeout(self):
        self.open_lid(100, 400)
        if self.get_proximity() < 150:
            print("Hand detected! Double fake-out time.")
            self.switch_arm_to_off(200, 50)
            self.retract_arm(200, 50)
            time.sleep(0.3)
            self.switch_arm_to_off(300, 80)
            self.retract_arm(300, 80)
        else:
            if self.get_switch():
                self.switch_arm_to_off(500, 100)
        self.retract_arm(400, 100)
        self.close_lid(0, 600)

    def _behavior_rapid_switch_off(self):
        self.open_lid(100, 300)
        if self.get_switch():
            self.switch_arm_to_off(200, 100)
        self.retract_arm(100, 100)
        self.close_lid(0, 300)

    def _behavior_insistent_switch(self):
        self.open_lid(100, 400)
        print("Insistent behavior: Rapidly switching off!")
        for _ in range(3):
            if self.get_switch():
                self.switch_arm_to_off(200, 100)
            self.retract_arm(200, 100)
            time.sleep(0.2)
        self.close_lid(0, 500)

    def _behavior_long_pause(self):
        self.open_lid(100, 500)
        print("Pausing to see if the hand comes closer...")
        time.sleep(2)
        if self.get_proximity() < 120 and self.get_switch():
            self.switch_arm_to_off(600, 100)
        else:
            print("No hand detected, closing lid slowly.")
            self.close_lid(0, 1000)

    def _behavior_random_lid_movement(self):
        print("Random lid movement behavior activated!")
        for _ in range(3):
            self.open_lid(random.randint(50, 100), random.randint(200, 500))
            self.close_lid(random.randint(0, 50), random.randint(200, 500))
        if self.get_switch():
            self.switch_arm_to_off(500, 100)
        self.retract_arm(300, 100)
        self.close_lid(0, 600)

    def _behavior_slow_retract(self):
        self.open_lid(100, 500)
        print("Moving arm slowly...")
        if self.get_switch():
            self.switch_arm_to_off(1000, 100)
        time.sleep(0.5)
        print("Slowly retracting arm...")
        self.retract_arm(1200, 100)
        self.close_lid(0, 700)

    def _behavior_triple_fake(self):
        self.open_lid(100, 300)
        for _ in range(3):
            self.switch_arm_to_off(200, 50)
            self.retract_arm(200, 50)
        if self.get_switch():
            print("Switching off for real this time!")
            self.switch_arm_to_off(300, 100)
        self.retract_arm(300, 100)
        self.close_lid(0, 400)

    _behaviors = [
        _behavior_peekaboo,
        _behavior_slow_approach,
        _behavior_quick_threat,
        _behavior_double_fakeout,
        _behavior_rapid_switch_off,
        _behavior_insistent_switch,
        _behavior_long_pause,
        _behavior_random_lid_movement,
        _behavior_slow_retract,
        _behavior_triple_fake
    ]

#
# # Example usage:
# box = UselessBox()
# while True:
#     box.random_behavior()
#     time.sleep(2)

# box.retract_arm(100, 0)
# box.open_lid(100, 100)
# time.sleep(1)
# box.switch_arm_to_off(100, 100)
# time.sleep(1)
# box.retract_arm(100, 0)