#!/bin/bash

BLE_FILES_CHANGED=0
RUN_TEST=0
cd /home/eddie/workspace/msdk


# # Check for changes made to these files
# WATCH_FILES="\
# .github/workflows/ci-tests/Examples_tests \
# Examples/MAX32655/BLE \
# Libraries/libs.mk \
# Libraries/Cordio \
# Libraries/CMSIS/Device/Maxim/MAX32655 \
# Libraries/PeriphDrivers/libPeriphDriver.mk \
# Libraries/PeriphDrivers/periphdriver.mk \
# Libraries/PeriphDrivers/max32655_files.mk \
# Libraries/PeriphDrivers/Source \
# Libraries/PeriphDrivers/Include/MAX32655 \
# Libraries/BlePhy/MAX32655 \
# Libraries/Boards/MAX32655"

# # Get the diff from main
# CHANGE_FILES=$(git diff --ignore-submodules --name-only remotes/origin/main)

# echo "Watching these locations and files"
# echo $WATCH_FILES

# echo "Checking for changes..."

# # Assume we want to actually run the workflow if no files changed
# if [[ "$CHANGE_FILES" != "" ]]; then
# for watch_file in $WATCH_FILES; do 
#     if [[ "$CHANGE_FILES" == *"$watch_file"* ]]; then
#     BLE_FILES_CHANGED=1
#     RUN_TEST=1
#     echo "Found changed files in: $watch_file"
#     fi
# done
# if [[ $BLE_FILES_CHANGED -eq 0 ]]
# then
#     echo "Skipping MAX32655 Test"
#     # Files were changed but not in MAX32655
#     RUN_TEST=0
# fi
# else 
# # Assume we want to actually run the workflow if no files changed
# RUN_TEST=1
# fi

# if [[ $RUN_TEST -eq 1 ]]
#     then
#     echo "Running Test on MAX32655"
#     cd .github/workflows/ci-tests/Examples_tests
#     chmod +x test_launcher.sh
#     FILE=/home/$USER/boards_config.json
#     dut_uart=`/usr/bin/python3 -c "import sys, json; print(json.load(open('$FILE'))['max32655_board2']['uart0'])"`
#     dut_serial=`/usr/bin/python3 -c "import sys, json; print(json.load(open('$FILE'))['max32655_board2']['daplink'])"`
#     ./test_launcher.sh max32655 $dut_uart $dut_serial
# fi
#---------------------------------------------------------------------------------
BLE_FILES_CHANGED=0
RUN_TEST=0

# Check for changes made to these files
WATCH_FILES="\
.github/workflows/ci-tests/Examples_tests \
Examples/MAX32665/BLE \
Libraries/libs.mk \
Libraries/CMSIS/Device/Maxim/MAX32665 \
Libraries/PeriphDrivers/libPeriphDriver.mk \
Libraries/PeriphDrivers/periphdriver.mk \
Libraries/PeriphDrivers/max32665_files.mk \
Libraries/PeriphDrivers/Source \
Libraries/PeriphDrivers/Include/MAX32665 \
Libraries/BlePhy/MAX32665 \
Libraries/Boards/MAX32665"

# Get the diff from main
CHANGE_FILES=$(git diff --ignore-submodules --name-only remotes/origin/main)

echo "Watching these locations and files"
echo $WATCH_FILES

echo "Checking for changes..."

# Assume we want to actually run the workflow if no files changed
if [[ "$CHANGE_FILES" != "" ]]; then
for watch_file in $WATCH_FILES; do 
    if [[ "$CHANGE_FILES" == *"$watch_file"* ]]; then
    BLE_FILES_CHANGED=1
    RUN_TEST=1
    echo "Found changed files in: $watch_file"
    fi
done
if [[ $BLE_FILES_CHANGED -eq 0 ]]
then
    echo "Skipping MAX32665 Test"
    # Files were changed but not in MAX32655
    RUN_TEST=0
fi
else 
# Assume we want to actually run the workflow if no files changed
RUN_TEST=1
fi

if [[ $RUN_TEST -eq 1 ]]
then
echo "Running Test"   
cd .github/workflows/ci-tests/Examples_tests
chmod +x test_launcher.sh
FILE=/home/$USER/boards_config.json
dut_uart=`/usr/bin/python3 -c "import sys, json; print(json.load(open('$FILE'))['max32665_board1']['uart0'])"`
dut_serial=`/usr/bin/python3 -c "import sys, json; print(json.load(open('$FILE'))['max32665_board1']['daplink'])"`
./test_launcher.sh max32665 $dut_uart $dut_serial          
fi

#------------------------------------------------------------------------------------------ME18
      
BLE_FILES_CHANGED=0
RUN_TEST=0
# Check for changes made to these files
WATCH_FILES="\
.github/workflows/ci-tests/Examples_tests \
Examples/MAX32690/BLE \
Libraries/libs.mk \
Libraries/CMSIS/Device/Maxim/MAX32690 \
Libraries/PeriphDrivers/libPeriphDriver.mk \
Libraries/PeriphDrivers/periphdriver.mk \
Libraries/PeriphDrivers/max32690_files.mk \
Libraries/PeriphDrivers/Source \
Libraries/PeriphDrivers/Include/MAX32690 \
Libraries/BlePhy/MAX32690 \
Libraries/Boards/MAX32690"

# Get the diff from main
CHANGE_FILES=$(git diff --ignore-submodules --name-only remotes/origin/main)

echo "Watching these locations and files"
echo $WATCH_FILES

echo "Checking for changes..."

# Assume we want to actually run the workflow if no files changed
if [[ "$CHANGE_FILES" != "" ]]; then
for watch_file in $WATCH_FILES; do 
    if [[ "$CHANGE_FILES" == *"$watch_file"* ]]; then
    BLE_FILES_CHANGED=1
    RUN_TEST=1
    echo "Found changed files in: $watch_file"
    fi
done
if [[ $BLE_FILES_CHANGED -eq 0 ]]
then
    echo "Skipping MAX32655 Test"
    # Files were changed but not in MAX32655
    RUN_TEST=0
fi
else 
# Assume we want to actually run the workflow if no files changed
RUN_TEST=1
fi
          
if [[ $RUN_TEST -eq 1 ]]
then

echo "Running Test"

cd .github/workflows/ci-tests/Examples_tests
chmod +x test_launcher.sh
FILE=/home/$USER/boards_config.json
dut_uart=`/usr/bin/python3 -c "import sys, json; print(json.load(open('$FILE'))['max32690_board_w1']['uart0'])"`
dut_serial=`/usr/bin/python3 -c "import sys, json; print(json.load(open('$FILE'))['max32690_board_w1']['daplink'])"`            
./test_launcher.sh max32690 $dut_uart $dut_serial     
fi     
      
