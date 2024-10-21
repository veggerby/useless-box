from machine import Pin, PWM
from time import sleep, sleep_ms

# Constants
FREQ = 50
SPAN = 1000 / FREQ

# PWM duty cycle calculations for SG90 servos
LOW = int(0.5 / SPAN * 1024)
HIGH = int(2.4 / SPAN * 1024)

def angle_to_duty(angle):
    percentage = angle / 180
    duty = int(LOW + (HIGH - LOW) * percentage)
    return duty

class SG90Servo:
    def __init__(self, pin):
        """
        Initializes the SG90 servo.
        :param pin: The GPIO pin connected to the servo.
        """
        self.servo = PWM(Pin(pin, mode=Pin.OUT))
        self.servo.freq(FREQ)

    def move_to_angle(self, angle):
        """
        Moves the servo to the specified angle.
        :param angle: The angle to move the servo to (0 to 180 degrees).
        """
        duty = angle_to_duty(angle)
        self.servo.duty(duty)

    def move_smoothly(self, start_angle, end_angle, duration, steps=50):
        """
        Moves the servo smoothly from start_angle to end_angle over a specified duration.
        :param start_angle: The starting angle.
        :param end_angle: The ending angle.
        :param duration: Duration in milliseconds for the movement.
        :param steps: Number of steps for smooth movement.
        """
        start_duty = angle_to_duty(start_angle)
        end_duty = angle_to_duty(end_angle)

        self.move_to_angle(start_angle)
        delay = int(duration / steps)
        step_size = max(1, int(abs(end_duty - start_duty) / steps))
        delta = 1 if start_duty < end_duty else -1
        duty = start_duty

        while delta * (end_duty - duty) > 0:
            self.servo.duty(duty)
            sleep_ms(delay)
            duty += step_size * delta

            if delta * (end_duty - duty) < 0:
                duty = end_duty
        self.servo.duty(end_duty)

class SwitchArm:
    def __init__(self, pin, retracted_angle=40, extended_angle=175):
        """
        Initializes the switch arm.
        :param pin: The GPIO pin connected to the switch arm servo.
        :param retracted_angle: The angle corresponding to the retracted position.
        :param extended_angle: The angle corresponding to the extended (fully switched off) position.
        """
        self.servo = SG90Servo(pin)
        self.retracted_angle = retracted_angle
        self.extended_angle = extended_angle

    def _percentage_to_angle(self, percentage):
        return self.retracted_angle + (self.extended_angle - self.retracted_angle) * percentage / 100

    def move(self, percentage=100, duration=500):
        """
        Moves the switch arm to the specified percentage.
        :param percentage: Percentage of movement (0 = fully retracted, 100 = fully extended).
        :param duration: Duration in milliseconds for the movement.
        """
        angle = self._percentage_to_angle(percentage)
        self.servo.move_to_angle(angle)

    def retract(self, percentage=0, duration=500):
        """
        Retracts the switch arm to the specified percentage.
        :param percentage: Percentage of retraction (0 = fully extended, 100 = fully retracted).
        :param duration: Duration in milliseconds for the movement.
        """
        angle = self._percentage_to_angle(100 - percentage)
        self.servo.move_to_angle(angle)

    def switch_off(self, duration=200, pre_wait=1000, wait=200, post_wait=0, steps=100):
        """
        Executes a switch-off sequence.
        :param duration: Duration in milliseconds for the switching movement.
        :param pre_wait: Delay before the movement in milliseconds.
        :param wait: Delay after reaching the end position in milliseconds.
        :param post_wait: Delay after retracting in milliseconds.
        :param steps: Number of steps for a smooth transition.
        """
        self.servo.move_to_angle(self.retracted_angle)
        sleep_ms(pre_wait)
        self.servo.move_smoothly(self.retracted_angle, self.extended_angle, duration, steps)
        sleep_ms(wait)
        self.servo.move_to_angle(self.retracted_angle)
        sleep_ms(post_wait)

class LidArm:
    def __init__(self, pin, close_angle=90, open_angle=8):
        """
        Initializes the lid arm.
        :param pin: The GPIO pin connected to the lid arm servo.
        :param close_angle: The angle corresponding to the closed position.
        :param open_angle: The angle corresponding to the fully open position.
        """
        self.servo = SG90Servo(pin)
        self.close_angle = close_angle
        self.open_angle = open_angle

    def _percentage_to_angle(self, percentage):
        return self.close_angle - (self.close_angle - self.open_angle) * percentage / 100

    def open(self, percentage=100, duration=500):
        """
        Opens the lid to the specified percentage.
        :param percentage: Percentage of how much to open the lid (0 = fully closed, 100 = fully open).
        :param duration: Duration in milliseconds for the movement.
        """
        angle = self._percentage_to_angle(percentage)
        self.servo.move_to_angle(angle)

    def close(self, percentage=0, duration=500):
        """
        Closes the lid to the specified percentage.
        :param percentage: Percentage of how much to close the lid (100 = fully closed, 0 = fully open).
        :param duration: Duration in milliseconds for the movement.
        """
        angle = self._percentage_to_angle(100 - percentage)
        self.servo.move_to_angle(angle)

# Example usage
if __name__ == "__main__":
    switch_arm = SwitchArm(pin=0)
    lid_arm = LidArm(pin=2)

    # Test the switch arm
    switch_arm.move(100)
    sleep(1)
    switch_arm.retract(100)

    # Test the lid arm
    lid_arm.open(100)
    sleep(1)
    lid_arm.close(0)
