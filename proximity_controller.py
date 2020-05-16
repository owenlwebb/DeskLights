"""Simple proximity-based LED strip controller. Turn on/off based on RSSI of a 
third device.

    Author: Owen Webb
    Date: 5/16/2020
"""
import json
from collections import deque
from statistics import median
from time import sleep

from BluetoothDevice import BluetoothDevice


# Color codes for Lights
OFF = '0000001e'
WHITE = 'ffffff1e'

# Thresholds
RSSI_THRESHOLD = 3
RSSI_WINDOW = 8


def main():
    with open('devices/lights.json', 'r') as lightsf, \
         open('devices/phone.json', 'r') as phonef:
        lights_info = json.load(lightsf)
        phone_info = json.load(phonef)

    phone = BluetoothDevice(phone_info['mac'], phone_info['name'])
    lights = BluetoothDevice(lights_info['mac'], lights_info['name'])
    LIGHTS_ON = False
    strengths = deque()

    while True:
        phone.connect()
        while phone.is_connected():
            strengths.append(phone.signal_strength())
            if len(strengths) == RSSI_WINDOW:
                strengths.popleft()
                # set lights
                if LIGHTS_ON and median(strengths) >= RSSI_THRESHOLD:
                    lights.write(lights_info['attribute'], OFF)
                    LIGHTS_ON = False
                elif not LIGHTS_ON and median(strengths) < RSSI_THRESHOLD:
                    lights.write(lights_info['attribute'], WHITE)
                    LIGHTS_ON = True
            sleep(1)


if __name__ == '__main__':
    main()
