#!/bin/bash

address=$(jq -r ".mac" devices/lights.json)
data=$(python3 -c "print(' '.join('0x'+'$1'[i:i+2] for i in range(0,${#1},2)))")

CONNECT="connect $address"
GATT="menu gatt"
SELECT="select-attribute 0000ffe1-0000-1000-8000-00805f9b34fb"
WRITE="write \"$data\""
QUIT="quit"

{
    for cmd in "$CONNECT" "$GATT" "$SELECT" "$WRITE" "$QUIT"; do
        echo $cmd
    done
} | bluetoothctl &> /dev/null
