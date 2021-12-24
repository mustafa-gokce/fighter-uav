import cv2
import subprocess as sp
import sys

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

cv2.namedWindow("result", cv2.WINDOW_AUTOSIZE)

while True:
    ret, frame = cap.read()

    sys.stdout.buffer.write(frame.tobytes())

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# python3 mjpgts_test.py | ffmpeg -f rawvideo -pixel_format bgr24 -video_size 1280x720 -framerate 41 -i - -vf format=yuv420p -f v4l2 /dev/video17