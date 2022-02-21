import io
import time
import http.server
import socketserver
import PIL.Image
import cv2
import tu_settings


class StreamingHandler(http.server.BaseHTTPRequestHandler):
    """
    streaming handler object
    """

    # handle get requests
    def do_GET(self):
        """
        handle get requests

        :return: None
        """

        # only process get requests from motion jpeg stream path
        if self.path == "/stream.mjpg":

            # send headers
            self.send_response(200)
            self.send_header("Content-type", "multipart/x-mixed-replace; boundary=--jpgboundary")
            self.end_headers()

            # do below always
            while True:

                # try to capture and stream an image frame
                try:

                    # capture an image frame
                    success, image_frame = capture.read()

                    # failed to capture an image frame
                    if not success:
                        continue

                    # convert image to RGB
                    image_frame = cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGB)

                    # convert image frame from numpy array to PIL JPEG object
                    jpg = PIL.Image.fromarray(image_frame)

                    # create temporary file in memory
                    temporary_file = io.BytesIO()

                    # save JPEG to temporary file in memory
                    jpg.save(temporary_file, "JPEG")

                    # write boundary
                    self.wfile.write("--jpgboundary".encode())

                    # send headers
                    self.send_header("Content-type", "image/jpeg")
                    self.send_header("Content-length", str(temporary_file.getbuffer().nbytes))
                    self.end_headers()

                    # publish JPEG object to stream
                    jpg.save(self.wfile, "JPEG")

                    # cool down
                    time.sleep(0.05)

                # interrupted by user
                except KeyboardInterrupt:
                    break

                # user left the server
                except BrokenPipeError:
                    break


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """
    handle requests in a separate thread
    """


# configure the capture device
capture = cv2.VideoCapture(-1)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, tu_settings.tu_video_stream_width)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, tu_settings.tu_video_stream_height)
capture.set(cv2.CAP_PROP_FPS, tu_settings.tu_video_stream_fps)

# try to start the server
try:

    # create streaming server object
    server = ThreadedHTTPServer((tu_settings.tu_video_stream_ip_local,
                                 tu_settings.tu_video_stream_port_local),
                                StreamingHandler)

    # start streaming server object
    server.serve_forever()

# interrupted by user
except KeyboardInterrupt:

    # release capture device and server
    capture.release()
    server.socket.close()
