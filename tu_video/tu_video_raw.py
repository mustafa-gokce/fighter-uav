import cv2
import tu_video_utils
import tu_settings

# create capture device
capture_device = cv2.VideoCapture("http://{0}:{1}/stream.mjpg".format(tu_settings.tu_video_stream_ip_remote,
                                                                      tu_settings.tu_video_stream_port_remote_raw))

# create pub socket
pub_socket = tu_video_utils.tu_video_create_pub(tu_settings.tu_video_stream_port_local_raw)

# do below always
loop_count = 0
while True:

    # capture frame
    success, my_image = capture_device.read()

    # manipulate data
    my_data = {"raw_loop_count": loop_count}

    # publish video stream to endpoints
    tu_video_utils.tu_video_pub(pub_socket, my_image, my_data)

    # update loop counter
    loop_count += 1
