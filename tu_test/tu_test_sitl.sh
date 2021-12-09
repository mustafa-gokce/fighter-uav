#!/bin/bash

# get inside the log directory
mkdir -p "$HOME"/test-ucusu/fighter-uav/logs
cd "$HOME"/test-ucusu/fighter-uav/logs || exit 1

# start simulations
for i in $(seq 0 4)
do
	screen -S simulation_firmware$((i + 1)) -d -m bash -c "$HOME/test-ucusu/fighter-uav/tu_test/arduplane -S -I$i --model plane --speedup 1 --defaults $HOME/test-ucusu/fighter-uav/tu_test/plane.parm"
	sleep 1
done
