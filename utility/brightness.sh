#!/bin/bash

address=$(cat lights.mac)
intensity=$(python3 -c "print(hex(round(($1/100)*255)))")

CONNECT="connect $address"
GATT="menu gatt"
SELECT="select-attribute 0000ffe1-0000-1000-8000-00805f9b34fb"
WRITE="write \"$intensity 0x00 0x00 0x2a\""
QUIT="quit"

{
    for cmd in "$CONNECT" "$GATT" "$SELECT" "$WRITE" "$QUIT"; do
        echo $cmd
    done
} | bluetoothctl &> /dev/null
