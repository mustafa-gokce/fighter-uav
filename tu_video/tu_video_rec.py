import numpy
import cv2

# create video writer
writer = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30, (1920, 1080))

# for some frames
for _ in range(1000):

    # generate noisy frame
    frame = numpy.random.randint(0, 255, (1080, 1920, 3)).astype("uint8")

    # write the frame
    writer.write(frame)

# release the writer and close the file
writer.release()
