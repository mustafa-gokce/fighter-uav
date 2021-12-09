#!/bin/bash

# get inside the log directory
mkdir -p "$HOME"/test-ucusu/fighter-uav/logs
cd "$HOME"/test-ucusu/fighter-uav/logs || exit 1

# start telemetry stream
for i in $(seq 0 4)
do
	screen -S simulation_proxy$((i + 1)) -d -m bash -c "mavproxy.py --aircraft uav$((i + 1)) --master tcp:127.0.0.1:$((5760 + i*10)) --out udp:127.0.0.1:$((9010 + i*10)) --daemon"
	sleep 1
done
