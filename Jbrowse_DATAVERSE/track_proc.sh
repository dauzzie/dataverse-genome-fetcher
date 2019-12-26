#!/usr/bin/bash
python alias=python3
python check_update.py
if [ $? -eq 0 ]; then
    echo "checking update OK"
else
    exit "no updates found"
fi
python cmd_collect.py
if [ $? -eq 0 ]; then
    echo "collecting commands OK"
else
    exit "no commands found"
fi
FILENAME=$(find -maxdepth 1 -type f -iname "command*.txt")
FILENAME="${FILENAME:2}"
mapfile -t cmdList < $FILENAME
for cmd in ${cmdList[@]}
do
echo "$cmd"
eval $cmd
if [ $? -eq 0 ]; then
    echo OK
else
    echo "$cmd FAIL"
fi
done

