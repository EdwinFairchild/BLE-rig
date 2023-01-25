#!/bin/bash

# file used to track state and store controller serial
FILE=/home/eddie/playground/BLE-rig/resources/ble_devices.json
#configure UART settings
controller_serial=$(/usr/bin/python3 -c "import sys, json; print(json.load(open('$FILE'))['controller']['serial'])")
controller_port=/dev/"$(ls -la /dev/serial/by-id | grep -n $controller_serial | rev | cut -d "/" -f1 | rev)"
stty -F $controller_port 115200

#get current state of the device
currentState=$(/usr/bin/python3 -c "import sys, json; print(json.load(open('$FILE'))['me17_main']['state'])")
if [[ $currentState -eq 0 ]]; then
    currentState=1
else
    currentState=0
fi

keyValuePairs=$(/usr/bin/python3 -c "import sys, json; 
fileDict=json.load(open('$FILE')); 
fileDict['me17_main']['state'] = $currentState; 
file = open('$FILE', 'w'); 
json.dump(fileDict,file,indent=4);
file.close();")

echo "me17main $currentState" >$controller_port
