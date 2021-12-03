import os
import time
import threading
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


# fallback screen media player
def tu_video_show():
    # get global variables
    global my_image, received_stream

    # open video capture
    video_capture = cv2.VideoCapture("../tu_asset/video/tu_video_2.mp4")

    # initialize frame counter
    frame_counter = 0

    # read until video is completed
    while True:

        # rollback to commercials
        if not received_stream:

            # capture frame
            frame_status, image_frame = video_capture.read()
            frame_counter += 1

            # resize the video for fitting
            image_frame = cv2.resize(image_frame, (tu_settings.tu_video_frame_width, tu_settings.tu_video_frame_height))

            # expose the frame
            my_image = image_frame

            # rollback if we reached at the end of the video
            if frame_counter == video_capture.get(cv2.CAP_PROP_FRAME_COUNT):
                frame_counter = 0
                video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_counter)

        # show image
        cv2.imshow("TU_VIDEO_RAW", my_image)

        # break the loop if requested
        if cv2.waitKey(1) & 0xFF == ord("q"):
            # destroy all the windows
            cv2.destroyAllWindows()

            # kill the code
            os._exit(0)

        # cool down
        time.sleep(1.0 / tu_settings.tu_video_stream_fps_max)


# create socket
sub_context = zmq.Context()
sub_socket = sub_context.socket(zmq.SUB)
sub_socket.setsockopt(zmq.SUBSCRIBE, b"")
sub_socket.setsockopt(zmq.RCVTIMEO, int(tu_settings.tu_video_stream_timeout * 1000))
sub_socket.connect("tcp://" + tu_settings.tu_vehicle_ip + ":" + str(tu_settings.tu_video_stream_port))

# delay first because of the socket bindings
time.sleep(tu_settings.tu_video_stream_initial_delay)

# create dummy frame
my_image = numpy.zeros((tu_settings.tu_video_frame_height, tu_settings.tu_video_frame_width, 3), numpy.uint8)
received_stream = False

# start fallback screen process
tu_video_show_thread = threading.Thread(target=tu_video_show)
tu_video_show_thread.start()

# receiving loop
while True:

    # get the contents
    try:

        # get data and image
        my_data, my_image = tu_video_sub(sub_socket)

        # incoming valid stream
        received_stream = True

    # error getting contents
    except zmq.error.Again:

        # clear data
        my_data = {}

        # could not receive the stream
        received_stream = False

    # visualization
    print(my_data)

    # fps limiter to prevent burst data
    time.sleep(1.0 / tu_settings.tu_video_stream_fps_max)
