#!/bin/bash

# get inside the log directory
mkdir -p "$HOME"/test-ucusu/fighter-uav/logs
cd "$HOME"/test-ucusu/fighter-uav/logs || exit 1

# start devices
sudo modprobe -r v4l2loopback
sudo modprobe v4l2loopback video_nr=10,11,12 card_label="Test Ucusu RAW Video Stream","Test Ucusu JUDGE Video Stream","Test Ucusu OSD Video Stream"
sudo modprobe v4l2loopback exclusive_caps=1
sudo v4l2-ctl -d /dev/video10 -c timeout=0
sudo v4l2-ctl -d /dev/video11 -c timeout=0
sudo v4l2-ctl -d /dev/video12 -c timeout=0

# run core starter script
sh "$HOME"/test-ucusu/fighter-uav/tu_core/tu_core_start.sh

# run simulated vehicle starter script
sh "$HOME"/test-ucusu/fighter-uav/tu_test/tu_test_simulation.sh

# run telemetry proxy
sh "$HOME"/test-ucusu/fighter-uav/tu_telem/tu_proxy_telem.sh

# run video starter script
sh "$HOME"/test-ucusu/fighter-uav/tu_video/tu_video_start.sh

# start panel
screen -L -Logfile tu_screen_panel.log -S tu_panel -d -m bash -c "PYTHONPATH=""$HOME""/test-ucusu/fighter-uav/ /usr/bin/python3 $HOME/test-ucusu/fighter-uav/tu_panel/tu_panel_main.py"
