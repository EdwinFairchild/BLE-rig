#!/bin/bash
#configure UART settings
stty -F /dev/ttyACM0 115200

#get current state of the device
FILE=/home/eddie/my-scripts/streamdeck/ble_devices.json

keyValuePairs=$(/usr/bin/python3 -c "import sys, json; 
fileDict=json.load(open('$FILE')); 
fileDict['me18']['state'] = 1;
fileDict['me17']['state'] = 1;
fileDict['me14']['state'] = 1;
fileDict['me17_main']['state'] = 1; 
file = open('$FILE', 'w'); 
json.dump(fileDict,file,indent=4);
file.close();")

echo "allon" >/dev/ttyACM0
