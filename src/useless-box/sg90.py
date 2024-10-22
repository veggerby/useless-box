from machine import Pin, PWM
from time import sleep_ms

class SG90Servo:
    PWM_FREQ = 50  # 50 Hz (20 ms period)
    MIN_DUTY = 26  # 5% duty cycle
    MAX_DUTY = 123  # 10% duty cycle

    def __init__(self, pin, default_angle=0):
        """
        Initializes the SG90 servo.
        :param pin: The GPIO pin connected to the servo.
        :param default_angle: The default starting angle of the servo (default is 0 degrees).
        """
        self.servo = PWM(Pin(pin, mode=Pin.OUT))
        self.servo.freq(self.PWM_FREQ)  # Set the frequency to 50 Hz (20 ms period)
        self.default_angle = default_angle  # Set the default angle
        self.current_angle = self.default_angle  # Initialize current angle
        self.move_to_angle(self.default_angle)  # Move to the default angle on initialization

    def angle_to_duty(self, angle):
        """
        Converts the angle (0-180 degrees) to the corresponding duty cycle.
        :param angle: The angle to move the servo to (0 to 180 degrees).
        :return: The duty cycle percentage corresponding to the angle.
        """
        # Interpolate between these values based on the angle
        if angle <= 0:
            duty = self.MIN_DUTY
        elif angle >= 180:
            duty = self.MAX_DUTY
        else:
            duty = self.MIN_DUTY + (angle / 180) * (self.MAX_DUTY - self.MIN_DUTY)
        return int(duty)

    def move_to_angle(self, angle, force = False):
        """
        Moves the servo to the specified angle.
        :param angle: The angle to move the servo to (0 to 180 degrees).
        """
        # round to 2 decimal places, so we have a chance of reducing unwanted servo adjustments
        angle = round(angle, 2)

        # do we need to move?
        if not force and angle == self.current_angle:
            return

        duty_value = self.angle_to_duty(angle)
        self.servo.duty(duty_value)
        self.current_angle = angle  # Update the current angle
        sleep_ms(250)  # Wait for the servo to move

    def move_smoothly(self, target_angle, duration_full_range=1000, steps=50):
        """
        Moves the servo smoothly from the current angle to the target angle over a specified duration.
        The duration is relative to a full 0-180 degree movement.

        :param target_angle: The target angle to move the servo to (0 to 180 degrees).
        :param duration_full_range: The duration in milliseconds for a full 0-180 degree movement.
        :param steps: Number of steps for smooth movement.
        """
        start_angle = self.current_angle
        angle_difference = abs(target_angle - start_angle)

        # Calculate the duration relative to the angle difference
        duration = (angle_difference / 180) * duration_full_range

        start_duty = self.angle_to_duty(start_angle)
        end_duty = self.angle_to_duty(target_angle)

        delay = int(duration / steps)
        step_size = (end_duty - start_duty) / steps

        for step in range(steps + 1):
            duty_value = int(start_duty + step * step_size)
            self.servo.duty(duty_value)
            sleep_ms(delay)

        self.current_angle = target_angle  # Update the current angle to the target angle

    def reset(self):
        """
        Resets the servo to the default starting angle (default is 0 degrees) instantly.
        """
        print(f"Resetting servo to {self.default_angle} degrees.")
        self.move_to_angle(self.default_angle, force=True)  # Move instantly to the default angle

# Example usage
if __name__ == "__main__":
#     servo1 = SG90Servo(0, default_angle=40)
#     sleep_ms(1000)
#     servo1.move_to_angle(173)
#     sleep_ms(1000)
#     servo1.reset()

    servo2 = SG90Servo(2, default_angle=90)
    servo2.reset()
    sleep_ms(1000)
    servo2.move_to_angle(30)
    sleep_ms(1000)
    servo2.reset()
   