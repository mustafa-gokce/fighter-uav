import time
import numpy
import zmq
import cv2
import tu_settings


# subscribe video stream ing endpoints
def tu_video_sub(socket, flags=0, copy=True, track=False):
    data = socket.recv_json(flags=flags)
    md = socket.recv_json(flags=flags)
    msg = socket.recv(flags=flags, copy=copy, track=track)
    img = numpy.frombuffer(bytes(memoryview(msg)), dtype=md["dtype"])
    return data, img.reshape(md["shape"])


# create socket
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
socket.connect("tcp://" + tu_settings.tu_vehicle_ip + ":" + str(tu_settings.tu_video_stream_port))

# delay first because of the socket bindings
time.sleep(tu_settings.tu_video_stream_initial_delay)

# receiving loop
while True:

    # get the contents
    my_data, my_image = tu_video_sub(socket)

    # visualization
    print(my_data)
    cv2.imshow("frame", my_image)

    # break the loop if requested
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    # fps limiter to prevent burst data
    time.sleep(1.0 / tu_settings.tu_video_stream_fps_max)

# destroy all the windows
cv2.destroyAllWindows()
