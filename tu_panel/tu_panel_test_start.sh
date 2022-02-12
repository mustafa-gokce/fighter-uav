#!/bin/bash

# get inside the log directory
mkdir -p "$HOME"/test-ucusu/fighter-uav/logs
cd "$HOME"/test-ucusu/fighter-uav/logs || exit 1

# start scripts
screen -S tu_test_video -d -m bash -c "PYTHONPATH=""$HOME""/test-ucusu/fighter-uav/ /usr/bin/python3 $HOME/test-ucusu/fighter-uav/tu_test/tu_test_video.py"
screen -S tu_video_raw -d -m bash -c "PYTHONPATH=""$HOME""/test-ucusu/fighter-uav/ /usr/bin/python3 $HOME/test-ucusu/fighter-uav/tu_video/tu_video_raw.py"
screen -S tu_video_judge -d -m bash -c "PYTHONPATH=""$HOME""/test-ucusu/fighter-uav/ /usr/bin/python3 $HOME/test-ucusu/fighter-uav/tu_video/tu_video_judge.py | ffmpeg -f rawvideo -pixel_format bgr24 -video_size 1280x720 -framerate 120 -i - -vf format=yuv420p -v 0 -f v4l2 /dev/video26"
screen -S tu_video_osd -d -m bash -c "PYTHONPATH=""$HOME""/test-ucusu/fighter-uav/ /usr/bin/python3 $HOME/test-ucusu/fighter-uav/tu_video/tu_video_osd.py"
screen -S tu_panel -d -m bash -c "PYTHONPATH=""$HOME""/test-ucusu/fighter-uav/ /usr/bin/python3 $HOME/test-ucusu/fighter-uav/tu_panel/tu_panel_main.py"