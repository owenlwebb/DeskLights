"""Python abstraction of a Bluetooth device by wrapping Bluez utilities."""
import json
from subprocess import DEVNULL, CalledProcessError, check_output
from time import sleep

import pexpect

DEBUG = False


def printd(*args):
    """Print Debug Message. Print arguments (space separated) if debug flag 
    is set."""
    if DEBUG:
        for s in args:
            print(s, end=' ')
        print()


class BluetoothDevice():
    def __init__(self, _mac, _name):
        self.CONNECTION_INTERVAL = 5

        self.mac = _mac
        self.name = _name
        self.btctl = pexpect.spawn('bluetoothctl')

    def __del__(self):
        """Cleanup blutoothctl process."""
        self.btctl.terminate()

    def is_connected(self):
        """Return True if currently connected to device."""
        self.btctl.sendline(f'info {self.mac}'.encode())
        return self.btctl.expect(['Connected: no', 'Connected: yes'])

    def connect(self, retry=True):
        """Attempt to establish connection. If retry=True, block until 
        successfully connected."""
        if retry:
            while not self.is_connected():
                printd('Reconnecting...')
                self.btctl.sendline(f'connect {self.mac}'.encode())
                sleep(self.CONNECTION_INTERVAL)
        else:
            self.btctl.sendline(f'connect {self.mac}'.encode())

    def signal_strength(self):
        """Return 0 - 120 signal strength indication (RSSI) where higher values
        indicate a weaker connection. Return None if hcitool fails to get rssi,
        common on some BT devices for some unknown reason..."""
        try:
            out = check_output(f'hcitool rssi {self.mac}', stderr=DEVNULL, shell=True)
            return abs(int(out.split()[-1]))
        except CalledProcessError:
            return None

    def write(self, attribute, data):
        """Write data to device attribute. Assumes already connected. 
        
            data = hex string representing a whole number of bytes.
            attribute = GATT attribute to write data to.
        """
        # format data into byte string acceptable by bluetoothctl
        data = ' '.join(f'0x{data[i:i + 2]}' for i in range(0, len(data), 2))

        # go to gatt menu, select proper attrib, write, back to main menu
        self.btctl.sendline(b'menu gatt')
        self.btctl.sendline(f'select-attribute {attribute}'.encode())
        self.btctl.sendline(f'write \"{data}\"'.encode())
        self.btctl.sendline(b'back')


if __name__ == '__main__':
    # TESTING
    with open('devices/lights.json', 'r') as fin:
        dev_info = json.load(fin)
    lights = BluetoothDevice(dev_info['mac'], dev_info['name'])
    lights.connect()
    print('RSSI:', lights.signal_strength())
    lights.write(dev_info['attribute'], 'ffffff1e')
