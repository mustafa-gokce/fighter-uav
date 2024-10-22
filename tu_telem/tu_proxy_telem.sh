#!/bin/bash

# get inside the log directory
mkdir -p "$HOME"/test-ucusu/fighter-uav/logs
cd "$HOME"/test-ucusu/fighter-uav/logs || exit 1

# start telemetry stream
screen -S tu_telemetry_proxy -d -m bash -c "mavproxy.py --aircraft zurna --master udp:127.0.0.1:10000 --out udp:127.0.0.1:10010 --out udp:127.0.0.1:10020 --out udp:127.0.0.1:10030 --daemon"
