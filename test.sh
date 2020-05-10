#!/bin/bash

address=$(cat mac_address.txt)
DELAY=0.04 # 0.04 is the empirical minimum needed to work properly
CONNECT="connect $address"
SELECT="select-attribute /org/bluez/hci0/dev_94_49_19_14_C9_AF/service000b/char000c"
DATA=$(python3 -c "print(' '.join('0x'+'$1'[i:i+2] for i in range(0,${#1},2)))")
QUIT="quit"

{
    for cmd in "$CONNECT" "$SELECT" "write $DATA" "$QUIT"; do
        echo $cmd
        sleep $DELAY
    done
} | bluetoothctl &> /dev/null
