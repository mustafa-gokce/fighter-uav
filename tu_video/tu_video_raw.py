import urllib.request
import numpy
import cv2
import tu_video_utils
import tu_settings

# capture device url
capture_device_url = "http://{0}:{1}/stream.mjpg".format(tu_settings.tu_video_stream_ip_remote,
                                                                 tu_settings.tu_video_stream_port_remote_raw)

# create pub socket
pub_socket = tu_video_utils.tu_video_create_pub(tu_settings.tu_video_stream_port_local_raw)

# do below always
loop_count = 0
while True:

    # try to connect to stream
    try:

        # create stream
        capture_device = urllib.request.urlopen(capture_device_url, timeout=0.05)

        # create frame bytes
        frame_bytes = bytes()

        # do below always
        while True:

            # try to read frame bytes
            try:

                # read frame bytes
                frame_bytes += capture_device.read(1024)

                # find starting and ending point of the frame
                frame_start = frame_bytes.find(b"\xff\xd8")
                frame_end = frame_bytes.find(b"\xff\xd9")

                # we have start and end
                if frame_start != -1 and frame_end != -1:

                    # get the jpeg frame
                    frame_jpeg = frame_bytes[frame_start:frame_end + 2]

                    # update byte list
                    frame_bytes = frame_bytes[frame_end + 2:]

                    # decode image
                    my_image = cv2.imdecode(numpy.frombuffer(frame_jpeg, dtype=numpy.uint8), cv2.IMREAD_COLOR)

                    # manipulate data
                    my_data = {"raw_loop_count": loop_count}

                    # publish video stream to endpoints
                    tu_video_utils.tu_video_pub(pub_socket, my_image, my_data)

                    # update loop counter
                    loop_count += 1

            # error decoding the stream so go to top loop for clean reconnection
            except Exception as e:

                # break the decoding loop
                break

    # could not connect to stream so retry
    except Exception as e:
        pass
