import cv2
import urllib.request
import numpy
import tu_settings

stream = urllib.request.urlopen("http://{0}:{1}/stream.mjpg".format(tu_settings.tu_video_stream_ip_remote,
                                                                    tu_settings.tu_video_stream_port_remote_raw))
bytes = bytes()
while True:
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b + 2]
        bytes = bytes[b + 2:]
        i = cv2.imdecode(numpy.fromstring(jpg, dtype=numpy.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('i', i)
        if cv2.waitKey(1) == 27:
            exit(0)
