#!/usr/bin/env bash
esptool.py --chip esp32c3 --port /dev/cu.usbmodem1452201 erase_flash
esptool.py --chip esp32c3 --port /dev/cu.usbmodem1452201 --baud 460800 write_flash -z 0x0 ../firmware/ESP32_GENERIC_C3-20240602-v1.23.0.bin