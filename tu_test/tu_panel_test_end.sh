#!/bin/bash

# get inside the log directory
mkdir -p "$HOME"/test-ucusu/fighter-uav/logs
cd "$HOME"/test-ucusu/fighter-uav/logs || exit 1

screen -X -S tu_test_video_pub quit
screen -X -S tu_video_raw quit
screen -X -S tu_video_judge quit
screen -X -S tu_video_osd quit
screen -X -S tu_panel quit
