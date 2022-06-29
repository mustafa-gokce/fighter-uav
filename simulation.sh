#!/bin/bash

# get inside the log directory
cd "$HOME"/test-ucusu/fighter-uav/ || exit 1
mkdir -p logs/
cd logs/ || exit 1

# start plane follow simulation environment
cd "$HOME"/test-ucusu/plane-follow/ || exit 1
/usr/bin/bash plane_follow_start.sh

# start judge server
cd "$HOME"/test-ucusu/fighter-judge/ || exit 1
screen -S fighter-judge -d -m bash -c "/usr/bin/python3 app.py"
