#!/bin/bash

# file used to track state and store controller serial
FILE=/home/eddie/playground/BLE-rig/resources/ble_devices.json
#configure UART settings
controller_serial=$(/usr/bin/python3 -c "import sys, json; print(json.load(open('$FILE'))['controller']['serial'])")
controller_port=/dev/"$(ls -la /dev/serial/by-id | grep -n $controller_serial | rev | cut -d "/" -f1 | rev)"
stty -F $controller_port 115200

keyValuePairs=$(/usr/bin/python3 -c "import sys, json; 
fileDict=json.load(open('$FILE')); 
fileDict['me18']['state'] = 1;
fileDict['me17']['state'] = 1;
fileDict['me14']['state'] = 1;
fileDict['me17_main']['state'] = 1; 
file = open('$FILE', 'w'); 
json.dump(fileDict,file,indent=4);
file.close();")

echo "allon" >$controller_port
