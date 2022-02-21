#!/bin/bash

# get inside the log directory
mkdir -p "$HOME"/test-ucusu/fighter-uav/logs
cd "$HOME"/test-ucusu/fighter-uav/logs || exit 1

# start server
screen -L -Logfile tu_screen_server.log -S tu_server -d -m bash -c "PYTHONPATH=""$HOME""/test-ucusu/fighter-uav/ /usr/bin/python3 $HOME/test-ucusu/fighter-uav/tu_core/tu_core_server.py"

# start interop
screen -L -Logfile tu_screen_interop.log -S tu_interop -d -m bash -c "PYTHONPATH=""$HOME""/test-ucusu/fighter-uav/ /usr/bin/python3 $HOME/test-ucusu/fighter-uav/tu_core/tu_core_interop.py"
