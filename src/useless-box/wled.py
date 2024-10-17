from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms

def start_light_show(pin_no = 0, num_leds = 30, color = (255, 0, 0), wait = 25):
    # Opsætning af neopixel på GP0
    pin = Pin(pin_no, Pin.OUT)
    np = NeoPixel(pin, num_leds)

    # Funktion til at tænde en enkelt LED
    def set_led(index, color):
        np[index] = color
        np.write()

    # Funktion til at slukke alle LED'er
    def clear():
        for i in range(num_leds):
            np[i] = (0, 0, 0)
        np.write()

    d = 1
    led = 0

    # Blink alle LED'er i forskellige farver
    while True:
        set_led(led, color)  # Rød
        sleep_ms(wait)
        set_led(led, (0, 0, 0))

        led += d

        if (led >= num_leds):
            led = num_leds - 2
            d = -1
        elif led < 0:
            led = 1
            d = 1


