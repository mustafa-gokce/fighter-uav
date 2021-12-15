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


# create socket
pub_context = zmq.Context()
pub_socket = pub_context.socket(zmq.PUB)
pub_socket.bind("tcp://*:" + str(tu_settings.tu_video_stream_port_local_raw))

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
    tu_video_pub(pub_socket, image_frame, {"loop_count": loop_count})

    # print counter for debugging
    print("seq:", loop_count)

    # update counter
    loop_count += 1

    # break the loop if requested
    if cv2.waitKey(1) & 0xFF == ord("q"):
        exit(0)
