#!/bin/bash

address=$(cat mac_address.txt)
DELAY=0.04 # 0.04 is the empirical minimum needed to work properly
CONNECT="connect $address"
SELECT="select-attribute /org/bluez/hci0/dev_94_49_19_14_C9_AF/service000b/char000c"
QUIT="quit"

intensity=$(python3 -c "print(hex(round(($1/100)*255)))")
brightness="write $intensity 0xde 0x88 0x2a"

{
    for cmd in "$CONNECT" "$SELECT" "$brightness" "$QUIT"; do
        echo $cmd
        sleep $DELAY
    done  
} | bluetoothctl &> /dev/null
