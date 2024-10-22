# boot.py -- run on boot-up
#import wifi
from controller import UselessBoxController

# wifi.connect_to_wifi("ssid", "password")

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