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


# get time in ms
def get_time_ms():
    return int(time.time() * 1000)


# open capture device
capture_device = cv2.VideoCapture(0)

# create socket
pub_context = zmq.Context()
pub_socket = pub_context.socket(zmq.PUB)
pub_socket.bind("tcp://*:" + str(tu_settings.tu_video_stream_port))

# delay first because of the socket bindings
time.sleep(tu_settings.tu_video_stream_initial_delay)

# time related variables
time_loop_initial = 0  # timestamp that loop iterated one more
time_loop_captured = 0  # timestamp that frame captured
time_loop_calculated = 0  # timestamp that frame manipulated
time_loop_streamed = 0  # timestamp that frame streamed
time_loop_final = 0  # timestamp at end of the loop
delay_limit = 0  # calculated delay caused by limiter
delay_capture = 0  # calculate delay caused by frame capture
delay_calculate = 0  # calculate delay caused by frame manipulations
delay_stream = 0  # calculate delay caused by streaming
delay_loop = 0  # calculate delay of overall loop

# streaming loop
seq = 0
while True:
    # get the initial loop time
    time_loop_initial = get_time_ms()

    # capture the frame
    frame_status, image_frame = capture_device.read()

    # get the time after frame capture
    time_loop_captured = get_time_ms()

    # frame processing will be here
    pass

    # get the time after calculations
    time_loop_calculated = get_time_ms()

    # generate payload
    data_payload = {"seq": seq,
                    "tim": time_loop_initial,
                    "del": {"lim": delay_limit,
                            "cap": delay_capture,
                            "clc": delay_calculate,
                            "str": delay_stream,
                            "lop": delay_loop}}

    # publish video stream to endpoints
    tu_video_pub(pub_socket, image_frame, data_payload)

    # get the time after frame is sent
    time_loop_streamed = get_time_ms()

    # fps limiter to prevent burst data
    if tu_settings.tu_video_fps_limit:
        time.sleep(1.0 / tu_settings.tu_video_stream_fps_max)

    # get final time
    time_loop_final = get_time_ms()

    # calculate delays
    delay_limit = time_loop_streamed - time_loop_initial
    delay_capture = time_loop_captured - time_loop_initial
    delay_calculate = time_loop_calculated - time_loop_captured
    delay_stream = time_loop_streamed - time_loop_captured
    delay_loop = time_loop_final - time_loop_initial

    # data visualization
    print(data_payload)

    # break the loop if requested
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    # update counter
    seq += 1

# release capture device
capture_device.release()
