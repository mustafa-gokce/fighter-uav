import picamera
import picamera.array
import cv2
from tu_video import tu_video_utils
import tu_settings

# create pub socket
pub_socket = tu_video_utils.tu_video_create_pub(tu_settings.tu_video_stream_port_remote_raw)

# initiate camera object with context manager
with picamera.PiCamera(resolution="{0}x{1}".format(tu_settings.tu_video_stream_width,
                                                   tu_settings.tu_video_stream_height),
                       framerate=tu_settings.tu_video_stream_fps) as capture_device:

    # initiate capture array
    captured_array = picamera.array.PiRGBArray(capture_device, size=(tu_settings.tu_video_stream_width,
                                                                     tu_settings.tu_video_stream_height))

    # capture frames continuously
    loop_count = 0
    for frame in capture_device.capture_continuous(captured_array, format="bgr", use_video_port=True):

        # get image frame from the captured array
        image_frame = frame.array

        # publish video stream to endpoints
        tu_video_utils.tu_video_pub(pub_socket, image_frame, {"pub_loop_count": loop_count})

        # update loop counter
        loop_count += 1

        # clear the stream in preparation for the next frame
        captured_array.truncate(0)

        # quit the script when desired
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
