import numpy
import cv2

writer = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30, (1920, 1080))

for frame in range(1000):
    writer.write(numpy.random.randint(0, 255, (1080, 1920, 3)).astype("uint8"))

writer.release()
