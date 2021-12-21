import cv2
from tu_video import tu_video_utils
import tu_settings

# open and configure camera
capture_device = cv2.VideoCapture(tu_settings.tu_video_stream_id_device)
capture_device.set(cv2.CAP_PROP_FRAME_WIDTH, tu_settings.tu_video_stream_width)
capture_device.set(cv2.CAP_PROP_FRAME_HEIGHT, tu_settings.tu_video_stream_height)
capture_device.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
capture_device.set(cv2.CAP_PROP_FPS, tu_settings.tu_video_stream_fps)

# create pub socket
pub_socket = tu_video_utils.tu_video_create_pub(tu_settings.tu_video_stream_port_remote_raw)

# do below always
loop_count = 0
while True:

    # capture image frame
    success, image_frame = capture_device.read()

    # publish video stream to endpoints
    tu_video_utils.tu_video_pub(pub_socket, image_frame, {"loop_count": loop_count})

    # update loop counter
    loop_count += 1

    # quit the script when desired
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# release the device for reuse
capture_device.release()
