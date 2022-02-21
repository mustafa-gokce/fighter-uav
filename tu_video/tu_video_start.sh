#!/bin/bash

# get inside the log directory
mkdir -p "$HOME"/test-ucusu/fighter-uav/logs
cd "$HOME"/test-ucusu/fighter-uav/logs || exit 1

# start video screens
screen -L -Logfile tu_screen_video_pub_test.log -S tu_test_video_pub -d -m bash -c "PYTHONPATH=""$HOME""/test-ucusu/fighter-uav/ /usr/bin/python3 $HOME/test-ucusu/fighter-uav/tu_test/tu_test_video_pub.py"
# screen -L -Logfile tu_screen_video_pub.log -S tu_video_pub -d -m bash -c "PYTHONPATH=""$HOME""/test-ucusu/fighter-uav/ /usr/bin/python3 $HOME/test-ucusu/fighter-uav/tu_video/tu_video_pub.py"
screen -L -Logfile tu_screen_video_raw.log -S tu_video_raw -d -m bash -c "PYTHONPATH=""$HOME""/test-ucusu/fighter-uav/ /usr/bin/python3 $HOME/test-ucusu/fighter-uav/tu_video/tu_video_raw.py"
screen -L -Logfile tu_screen_video_judge.log -S tu_video_judge -d -m bash -c "PYTHONPATH=""$HOME""/test-ucusu/fighter-uav/ /usr/bin/python3 $HOME/test-ucusu/fighter-uav/tu_video/tu_video_judge.py"
screen -L -Logfile tu_screen_video_osd.log -S tu_video_osd -d -m bash -c "PYTHONPATH=""$HOME""/test-ucusu/fighter-uav/ /usr/bin/python3 $HOME/test-ucusu/fighter-uav/tu_video/tu_video_osd.py"
