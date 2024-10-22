from time import sleep
from sg90 import SG90Servo

class LidArm:
    def __init__(self, pin, close_angle=90, open_angle=30):
        """
        Initializes the lid arm.
        :param pin: The GPIO pin connected to the lid arm servo.
        :param close_angle: The angle corresponding to the closed position.
        :param open_angle: The angle corresponding to the fully open position.
        """
        self.servo = SG90Servo(pin, default_angle=close_angle)
        self.close_angle = close_angle
        self.open_angle = open_angle
        self.reset()

    def _percentage_to_angle(self, percentage):
        return self.close_angle - (self.close_angle - self.open_angle) * percentage / 100

    def open(self, percentage=100, duration=500):
        """
        Opens the lid to the specified percentage.
        :param percentage: Percentage of how much to open the lid (0 = fully closed, 100 = fully open).
        :param duration: Duration in milliseconds for the movement.
        """
        angle = self._percentage_to_angle(percentage)
        self.servo.move_smoothly(target_angle=angle, duration_full_range=duration)

    def close(self, percentage=100, duration=500):
        """
        Closes the lid to the specified percentage.
        :param percentage: Percentage of how much to close the lid (100 = fully closed, 0 = fully open).
        :param duration: Duration in milliseconds for the movement.
        """
        angle = self._percentage_to_angle(100 - percentage)
        self.servo.move_smoothly(target_angle=angle, duration_full_range=duration)

    def is_open(self):
        return self.servo.current_angle < 50

    def reset(self):
        """
        Resets the lid arm to the closed position instantly.
        """
        print("Resetting lid arm to closed position.")
        self.servo.reset()  # Reset the servo to its default (closed) angle

# Example usage
if __name__ == "__main__":
    lid_arm = LidArm(pin=2)

    # Test the lid arm
    lid_arm.open()
    sleep(1)
    lid_arm.close()

    # Test resetting
    lid_arm.reset()
