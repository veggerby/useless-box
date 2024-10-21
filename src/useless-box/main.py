from useless import UselessBox
import random
import time

class UselessBoxController:
    def __init__(self, box):
        self.box = box
        self.running = True

    def reset_box(self):
        """
        Resets the box to the initial state: lid closed and arm retracted.
        """
        print("Resetting box to initial state...")
        self.box.retract_arm(0, 0)  # Fully retract the arm
        self.box.close_lid(0, 0)  # Fully close the lid

    def run(self):
        """
        Main loop that continuously checks for stimuli and responds with appropriate behaviors.
        It reacts to proximity, the switch state, or random timed events.
        """
        self.reset_box()  # Make sure the box starts in a known state

        while self.running:
            # Check proximity sensor
            proximity = self.box.get_proximity()
            if proximity > 100:  # Hand detected nearby
                print("Proximity alert: Hand detected nearby!")
                self.box.random_behavior()

            # Check if the switch is on
            if self.box.get_switch():
                print("Switch is On! Initiating switch off sequence.")
                self.box.random_behavior()

            # Randomly trigger a behavior every 10-20 seconds, simulating idle behavior
            random_time = random.randint(10, 20)
            print(f"Waiting for {random_time} seconds for next random event...")
            time.sleep(random_time)

            # Randomly decide if a behavior should be triggered even without stimuli
            if random.random() < 0.3:  # 30% chance of random behavior
                print("Random event triggered!")
                self.box.random_behavior()

            # Small delay between loop iterations to simulate real-time
            time.sleep(0.5)

    def stop(self):
        """
        Stops the controller.
        """
        self.running = False

# Example usage
if __name__ == "__main__":
    box = UselessBox(switch_pin=0, lid_pin=2, sda_pin=6, scl_pin=7, toggle_pin=21)
    controller = UselessBoxController(box)
    try:
        controller.run()
    except KeyboardInterrupt:
        print("Stopping the Useless Box Controller...")
        controller.stop()
