import time
import cv2
import tu_video_utils
import tu_settings

# create socket
pub_socket = tu_video_utils.tu_video_socket_pub(tu_settings.tu_video_stream_port_local_raw)

# create capture device
capture_device = cv2.VideoCapture("http://{0}:{1}/stream.mjpg".format(tu_settings.tu_video_stream_ip_local,
                                                                      tu_settings.tu_video_stream_port_remote_raw))

# delay first because of the socket bindings
time.sleep(tu_settings.tu_video_stream_delay)

# do below always
loop_count = 0
while True:

    # capture frame
    success, image_frame = capture_device.read()

    # publish video stream to endpoints
    tu_video_utils.tu_video_pub(pub_socket, image_frame, {"loop_count": loop_count})

    # update counter
    loop_count += 1

    # break the loop if requested
    if cv2.waitKey(1) & 0xFF == ord("q"):
        exit(0)
