import os
from collections import deque
from statistics import median
from subprocess import PIPE, Popen
from time import sleep

import pexpect

# load addresses
with open('phone.mac', 'r') as f1, open('lights.mac', 'r') as f2:
    PHONE_ADDR = f1.read().strip()
    LIGHTS_ADDR = f2.read().strip()
PHONE_NAME = 'Pixel 2 XL'


def connect(mac, name):
    bt = pexpect.spawn('bluetoothctl')
    failure = 1
    while failure:
        # print('Reconnecting...')
        bt.send(f'connect {mac}\n'.encode())
        failure = bt.expect([name.encode(), b'#'])
        sleep(3)
    bt.terminate()


def rssi(mac):
    cmd = f'hcitool rssi {mac}'
    out, err = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True).communicate()
    return None if err else abs(int(out.split()[-1]))


def main():
    os.system('utility/write.sh 0000001e')
    LIGHTS_ON = False
    strengths = deque()

    while True:
        rssi_val = rssi(PHONE_ADDR)
        while rssi_val is not None:
            # print(rssi_val)
            strengths.append(rssi_val)
            if len(strengths) == 6:
                strengths.popleft()

                # set lights
                if LIGHTS_ON and median(strengths) >= 3:
                    os.system('utility/write.sh 0000001e')
                    LIGHTS_ON = False
                elif not LIGHTS_ON and median(strengths) < 3:
                    os.system('utility/write.sh ffffff1e')
                    LIGHTS_ON = True

            sleep(1)
            rssi_val = rssi(PHONE_ADDR)
        connect(PHONE_ADDR, PHONE_NAME)


if __name__ == '__main__':
    main()
