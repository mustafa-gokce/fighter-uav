import cv2
import tu_settings

# create capture device
capture_device = cv2.VideoCapture("http://{0}:{1}/stream.mjpg".format(tu_settings.tu_vehicle_ip,
                                                                      tu_settings.tu_video_stream_port))

# do below always
while True:

    # capture frame
    success, image_frame = capture_device.read()

    # show the frame
    cv2.imshow("tu_video_raw", image_frame)

    # break the loop if requested
    if cv2.waitKey(1) & 0xFF == ord("q"):
        exit(0)
