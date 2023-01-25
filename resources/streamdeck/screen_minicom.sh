#!/bin/bash
#give time for daplink to show up in the system
sleep 10
screen -d -m minicom -D /dev/ttyACM0
