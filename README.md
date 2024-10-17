# Useless Box

This is a further development of [useless-box](https://github.com/balassy/useless-box/) by @balassy. 3D Sketches available on [Thingiverse](https://www.thingiverse.com/thing:3856965), with [local copy](./resources/Smart%20Useless%20Box%20with%20ESP8266%20and%20Gesture%20Sensor%20-%203856965.zip).

## Firnware

Using [ESP32-C3 Super Mini](https://ardustore.dk/produkt/esp32-c3-super-mini-wifi-4mb-ble5-udviklingsboard)

[Datasheet](./resources/ESP32C3%20Datasheet.PDF) from [ardustore.dk](https://ardustore.dk/error/ESP32C3%20Datasheet.PDF)

[Generic ESP32-C3 firmare](https://micropython.org/download/ESP32_GENERIC_C3/).

### Flash

```sh
brew install esptool
```

or

```sh
pip install esptool
```

Flash ESP32:

```sh
esptool.py --chip esp32c3 --port /dev/cu.usbmodem1452201 erase_flash
esptool.py --chip esp32c3 --port /dev/cu.usbmodem1452201 --baud 460800 write_flash -z 0x0 ./firmware/ESP32_GENERIC_C3-20240602-v1.23.0.bin
```
