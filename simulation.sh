#!/bin/bash

# get inside the log directory
cd "$HOME"/test-ucusu/fighter-uav/ || exit 1
mkdir -p logs/
cd logs/ || exit 1

# start plane follow simulation environment
cd "$HOME"/test-ucusu/fighter-uav/plane-follow/ || exit 1
/usr/bin/bash plane_follow_start.sh

until ! screen -list | grep -q "plane_follow_deploy"; do
  sleep 1
done

# start rest server
cd "$HOME"/test-ucusu/fighter-uav/mav-rest/ || exit 1
screen -S mav-rest -d -m bash -c "PYTHONPATH=$(pwd) /usr/bin/python3 mav-rest.py --host=127.0.0.1 --port=8000 --master=127.0.0.1:10010"
