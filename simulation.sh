#!/bin/bash

# initial configurations
TOTAL_VEHICLE_COUNT=5

# get inside the log directory
cd "$HOME"/test-ucusu/fighter-uav/ || exit 1
mkdir -p logs/
cd logs/ || exit 1

# start plane follow simulation environment
cd "$HOME"/test-ucusu/plane-follow/ || exit 1
/usr/bin/bash plane_follow_start.sh

# wait for vehicles to be fully deployed
until ! screen -list | grep -q "plane_follow_deploy"; do
  sleep 1
done

# start rest servers
cd "$HOME"/test-ucusu/mav-rest/ || exit 1
for i in $(seq 1 $TOTAL_VEHICLE_COUNT); do
  screen -S mav-rest-$((i)) -d -m bash -c "/usr/bin/python3 mav-rest.py --host=127.0.0.1 --port=$((8000 + i * 10)) --master=udpin:127.0.0.1:$((10000 + i * 10))"
done

# start judge server
cd "$HOME"/test-ucusu/fighter-judge/ || exit 1
screen -S fighter-judge -d -m bash -c "/usr/bin/python3 app.py"
