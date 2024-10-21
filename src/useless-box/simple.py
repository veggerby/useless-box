from time import sleep
from servo import SwitchArm, LidArm
from proximity import ProximitySensor
from switch import ToggleSwitch

print("useless-box version 2.0")
print("-----------------------")

# Initialize components
switch_arm = SwitchArm(pin=0)
lid_arm = LidArm(pin=2)
toggle_switch = ToggleSwitch(pin_number=21)
proximity_sensor = ProximitySensor(sda_pin=6, scl_pin=7)

# State variables
last_switch = None
lid_open = False
count = -1

switch_arm.retract(100, 0)
lid_arm.close(100, 0)

while False:
    current_switch = toggle_switch.is_on()
    prox = proximity_sensor.read_proximity()

    if current_switch and not last_switch:
        count = 20  # wait for count cycles

    if lid_open:
        if prox < 100 and count < 0:
            lid_arm.close(0, 500)  # Close the lid completely over 500ms
            lid_open = False
        elif current_switch and lid_open and count <= 0:
            switch_arm.switch_off(pre_wait=100)
            lid_arm.close(0, 500)  # Close the lid completely over 500ms
            lid_open = False
    else:
        if prox > 100 or count == 0:
            lid_arm.open(100, 500)  # Open the lid fully over 500ms
            lid_open = True

    count -= 1
    last_switch = current_switch
    sleep(0.2)
