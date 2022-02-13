import io
import picamera
import logging
import socketserver
import threading
import http.server
import tu_settings


# define streaming output object
class StreamingOutput(object):

    # initiate streaming output
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = threading.Condition()

    # write buffer to stream
    def write(self, buf):
        if buf.startswith(b"\xff\xd8"):
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)


# define streaming handler object
class StreamingHandler(http.server.BaseHTTPRequestHandler):

    # handle get requests
    def do_GET(self):

        # only process get requests from motion jpeg stream path
        if self.path == "/stream.mjpg":

            # create content headers
            self.send_response(200)
            self.send_header("Age", str(0))
            self.send_header("Cache-Control", "no-cache, private")
            self.send_header("Pragma", "no-cache")
            self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=FRAME")
            self.end_headers()

            # try to get frame
            try:

                # do below always
                while True:

                    # start output condition context
                    with output.condition:

                        # wait until the frame arrives
                        output.condition.wait()

                        # get the frame
                        frame = output.frame

                    # create frame headers
                    self.wfile.write(b"--FRAME\r\n")
                    self.send_header("Content-Type", "image/jpeg")
                    self.send_header("Content-Length", str(len(frame)))
                    self.end_headers()

                    # write frame to stream
                    self.wfile.write(frame)
                    self.wfile.write(b"\r\n")

            # unknown error is occurred
            except Exception as e:

                # notify that unknown error is occurred
                logging.warning("Removed streaming client %s: %s", self.client_address, str(e))

        # invalid request
        else:

            # prepare invalid request headers
            self.send_error(404)
            self.end_headers()


# define streaming server object
class StreamingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):

    # allow reusing streaming server address
    allow_reuse_address = True

    # allow streaming server to create daemon threads
    daemon_threads = True


# do below always
while True:

    # try to get in camera context
    try:

        # initiate camera object with context manager
        with picamera.PiCamera(resolution="{0}x{1}".format(tu_settings.tu_video_stream_width,
                                                           tu_settings.tu_video_stream_height),
                               framerate=tu_settings.tu_video_stream_fps) as capture_device:

            # initiate output object
            output = StreamingOutput()

            # start capture device to recording to output object
            capture_device.start_recording(output, format="mjpeg")

            # prepare address
            address = (tu_settings.tu_vehicle_ip, tu_settings.tu_video_stream_port_remote_raw)

            # create streaming server object
            server = StreamingServer(address, StreamingHandler)

            # start streaming server object
            server.serve_forever()

    # unknown exception is occurred
    except Exception as e:

        # stop capture device from recording
        capture_device.stop_recording()

        # notify that unknown exception is occurred
        logging.error(e)
