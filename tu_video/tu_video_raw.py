import urllib.request
import numpy
import cv2
import pyfakewebcam
import tu_video_util
import tu_settings

# testing mode is enabled
if tu_settings.tu_video_stream_test:

    # capture device is local
    capture_device_url = "http://{0}:{1}/stream.mjpg".format(tu_settings.tu_video_stream_ip_local,
                                                             tu_settings.tu_video_stream_port_local)

# testing mode is disabled
else:

    # capture device is remote
    capture_device_url = "http://{0}:{1}/stream.mjpg".format(tu_settings.tu_video_stream_ip_remote,
                                                             tu_settings.tu_video_stream_port_remote)

# create dummy sink for raw video streaming
sink_raw = pyfakewebcam.FakeWebcam(video_device=tu_settings.tu_video_stream_port_local_raw,
                                   width=tu_settings.tu_video_stream_width,
                                   height=tu_settings.tu_video_stream_height)

# do below always
while True:

    # try to connect to stream
    try:

        # create stream
        capture_device = urllib.request.urlopen(url=capture_device_url,
                                                timeout=tu_settings.tu_video_stream_timeout)

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

                    # check image
                    if tu_video_util.is_valid_image(my_image):

                        # change color space if testing
                        if tu_settings.tu_video_stream_test:
                            # convert image to RGB
                            my_image = cv2.cvtColor(my_image, cv2.COLOR_BGR2RGB)

                        # send image frame to judge sink
                        sink_raw.schedule_frame(my_image)

            # error decoding the stream so go to top loop for clean reconnection
            except Exception as e:

                # break the decoding loop
                break

    # could not connect to stream so retry
    except Exception as e:

        # do nothing
        pass
