#!/bin/bash
#configure UART settings
stty -F /dev/ttyACM0 115200

#get current state of the device
FILE=/home/eddie/my-scripts/streamdeck/ble_devices.json
currentState=$(/usr/bin/python3 -c "import sys, json; print(json.load(open('$FILE'))['me18']['state'])")
if [[ $currentState -eq 0 ]]; then
    currentState=1
else
    currentState=0
fi

keyValuePairs=$(/usr/bin/python3 -c "import sys, json; 
fileDict=json.load(open('$FILE')); 
fileDict['me18']['state'] = $currentState; 
file = open('$FILE', 'w'); 
json.dump(fileDict,file,indent=4);
file.close();")

echo "me18 $currentState" >/dev/ttyACM0