from time import sleep
from sg90 import SG90Servo

class SwitchArm:
    def __init__(self, pin, retracted_angle=40, extended_angle=175):
        """
        Initializes the switch arm.
        :param pin: The GPIO pin connected to the switch arm servo.
        :param retracted_angle: The angle corresponding to the retracted position.
        :param extended_angle: The angle corresponding to the extended (fully switched off) position.
        """
        self.servo = SG90Servo(pin, default_angle=retracted_angle)
        self.retracted_angle = retracted_angle
        self.extended_angle = extended_angle
        self.reset()

    def _percentage_to_angle(self, percentage):
        return self.retracted_angle + (self.extended_angle - self.retracted_angle) * percentage / 100

    def extend(self, percentage=100, duration=500):
        """
        Extends the switch arm to the specified percentage.
        :param percentage: Percentage of extention (0 = fully retracted, 100 = fully extended).
        :param duration: Duration in milliseconds for the movement.
        """
        angle = self._percentage_to_angle(percentage)
        self.servo.move_smoothly(target_angle=angle, duration_full_range=duration, steps=100)

    def retract(self, percentage=100, duration=500):
        """
        Retracts the switch arm to the specified percentage.
        :param percentage: Percentage of retraction (0 = fully extended, 100 = fully retracted).
        :param duration: Duration in milliseconds for the movement.
        """
        angle = self._percentage_to_angle(100 - percentage)
        self.servo.move_smoothly(target_angle=angle, duration_full_range=duration, steps=100)

    def reset(self):
        """
        Resets the switch arm to the retracted position instantly.
        """
        print("Resetting switch arm to retracted position.")
        self.servo.reset()  # Reset the servo to its default (retracted) angle

# Example usage
if __name__ == "__main__":
    switch_arm = SwitchArm(pin=0)

    # Test the switch arm
    switch_arm.extend()
    sleep(1)
    switch_arm.retract()

    # Test resetting
    switch_arm.reset()
