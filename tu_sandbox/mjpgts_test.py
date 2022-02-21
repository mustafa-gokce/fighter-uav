# ffmpeg -f rawvideo -pixel_format bgr24 -video_size 1280x720 -framerate 120 -i - -vf format=yuv420p -v 0 -vb 64M -threads 2 -tune zerolatency -f mpegts udp://127.0.0.1:23000
# ffplay -analyzeduration 1 -fflags -nobuffer -probesize 32 -sync ext -fast udp://127.0.0.1:23000
# sudo modprobe v4l2loopback video_nr=26
# sudo apt install v4l2loopback-dkms
# sudo apt-get install v4l2loopback-utils
# sudo modprobe v4l2loopback devices=1
# ffplay /dev/video26
