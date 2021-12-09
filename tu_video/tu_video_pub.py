import time
import threading
import zmq
import numpy
import cv2
import tu_settings


# get time in ms
def get_time_ms():
    return int(time.time() * 1000)


# publish video stream to endpoints
def tu_video_pub(socket, img, data, flags=0):
    md = dict(dtype=str(img.dtype), shape=img.shape)
    socket.send_json(data, flags | zmq.SNDMORE)
    socket.send_json(md, flags | zmq.SNDMORE)
    return socket.send(img, flags)


# capture frames from device
def tu_video_cap():
    # get global variables
    global frame_status, image_frame

    # do always
    while True:

        # try to open capture device
        try:

            # open capture device
            capture_device = cv2.VideoCapture(tu_settings.tu_video_capture_device_id, cv2.CAP_ANY)
            capture_device.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
            capture_device.set(cv2.CAP_PROP_FRAME_WIDTH, tu_settings.tu_video_frame_width)
            capture_device.set(cv2.CAP_PROP_FRAME_HEIGHT, tu_settings.tu_video_frame_height)
            capture_device.set(cv2.CAP_PROP_FPS, tu_settings.tu_video_fps_limit)

        # device cannot be opened
        except Exception as e:

            # clear the device
            capture_device = None

        # check if image source is opened
        if capture_device is not None:

            # device is still opened
            while capture_device.isOpened():

                # capture the frame
                frame_status, image_frame_raw = capture_device.read()
                image_frame_height, image_frame_width, image_frame_channel = image_frame_raw.shape

                # check frame is valid
                if not frame_status \
                        or image_frame_height != tu_settings.tu_video_frame_height \
                        or image_frame_width != tu_settings.tu_video_frame_width\
                        or image_frame_channel != tu_settings.tu_video_frame_channel:

                    # frame is not valid brake
                    break

                # frame is valid so copy it
                image_frame = image_frame_raw.copy()

                # break the loop if requested
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

                # fps limiter to prevent burst data
                if tu_settings.tu_video_fps_limit:
                    time.sleep(1.0 / tu_settings.tu_video_stream_fps_max)

            # release capture device
            capture_device.release()

        # fallback image
        frame_status = False
        image_frame = numpy.zeros((tu_settings.tu_video_frame_height, tu_settings.tu_video_frame_width, 3), numpy.uint8)

        # fps limiter to prevent burst data
        if tu_settings.tu_video_fps_limit:
            time.sleep(1.0 / tu_settings.tu_video_stream_fps_max)


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

image_frame = numpy.zeros((tu_settings.tu_video_frame_height, tu_settings.tu_video_frame_width, 3), numpy.uint8)
frame_status = False

# start thread
capture_thread = threading.Thread(target=tu_video_cap)
capture_thread.start()

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

    # get initial time
    time_loop_initial = get_time_ms()

    # frame processing will be here
    pass

    # generate payload
    data_payload = {"seq": seq, "tim": time_loop_initial}

    # publish video stream to endpoints
    tu_video_pub(pub_socket, image_frame, data_payload)

    # data visualization
    print(data_payload)

    # update counter
    seq += 1

    # fps limiter to prevent burst data
    if tu_settings.tu_video_fps_limit:
        time.sleep(1.0 / tu_settings.tu_video_stream_fps_max)

# release capture device
capture_device.release()