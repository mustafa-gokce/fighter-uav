#!/bin/bash

# get inside the log directory
mkdir -p "$HOME"/test-ucusu/fighter-uav/logs
cd "$HOME"/test-ucusu/fighter-uav/logs || exit 1

# start simulations
screen -S tu_simulation_firmware -d -m bash -c "$HOME/test-ucusu/fighter-uav/tu_test/arduplane -S -I0 --model plane --speedup 1 --defaults $HOME/test-ucusu/fighter-uav/tu_test/plane.parm"
screen -S tu_simulation_proxy -d -m bash -c "mavproxy.py --aircraft zurna --master tcp:127.0.0.1:5760 --out udp:127.0.0.1:9010 --daemon"
