from time import sleep
from arm_lid import LidArm
from arm_switch import SwitchArm
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
count = -1

# lid_arm.open()
# sleep(1)
# switch_arm.extend(50, duration = 2000)
# switch_arm.extend(duration = 100)
# sleep(1)
#
# switch_arm.retract(100, duration = 1000)
# lid_arm.close()

while True:
    current_switch = toggle_switch.is_on()
    prox = proximity_sensor.read_proximity()

#     print(f"Switch: {current_switch}, Proximity: {prox}")

    if current_switch and not last_switch:
        count = 20  # wait for count cycles

    if lid_arm.is_open():
        if prox < 100 and count < 0:
            lid_arm.close()
        elif current_switch and count <= 0:
            switch_arm.extend()
            sleep(2)
            switch_arm.retract(100)
            lid_arm.close()
    else:
        if prox > 100 or count == 0:
            lid_arm.open()

    count -= 1
    last_switch = current_switch
    sleep(0.2)
