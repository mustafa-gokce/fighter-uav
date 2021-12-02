import time
import zmq
import cv2
import tu_settings


# publish video stream to endpoints
def tu_video_pub(socket, img, data, flags=0):
    md = dict(dtype=str(img.dtype), shape=img.shape)
    socket.send_json(data, flags | zmq.SNDMORE)
    socket.send_json(md, flags | zmq.SNDMORE)
    return socket.send(img, flags)


# open capture device
capture_device = cv2.VideoCapture(0)

# create socket
pub_context = zmq.Context()
pub_socket = pub_context.socket(zmq.PUB)
pub_socket.bind("tcp://*:" + str(tu_settings.tu_video_stream_port))

# delay first because of the socket bindings
time.sleep(tu_settings.tu_video_stream_initial_delay)

# streaming loop
loop_count = 0
while True:
    # print counter for debugging
    print("seq:", loop_count)

    # capture the frame
    ret, image_frame = capture_device.read()

    # publish video stream to endpoints
    tu_video_pub(pub_socket, image_frame, {"loop_count": loop_count})

    # update counter
    loop_count += 1

    # break the loop if requested
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    # fps limiter to prevent burst data
    time.sleep(1.0 / tu_settings.tu_video_stream_fps_max)

# release capture device
capture_device.release()
