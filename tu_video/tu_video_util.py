import time
import cv2
import settings


def is_valid_image(image):
    """
    check if image frame is valid

    :param image: image frame
    :return: image frame is valid or not
    """

    if image is None:
        return False

    # check if image frame is valid
    return image.shape == (tu_settings.video_stream_height, tu_settings.video_stream_width, 3)


def capture_device_create(port,
                          width=tu_settings.video_stream_width,
                          height=tu_settings.video_stream_height,
                          fps=tu_settings.video_stream_fps,
                          blocking=True):
    """
    create capture device

    :param port: port of the capture device
    :param width: width of the image frame
    :param height: height of the image frame
    :param fps: fps of the video stream
    :param blocking: block until received valid frame
    :return: capture device
    """

    # create capture device
    capture_device = cv2.VideoCapture(port)
    capture_device.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture_device.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    capture_device.set(cv2.CAP_PROP_FPS, fps)

    # blocking is requested
    if blocking:

        # block until device is opened
        while not capture_device.isOpened():
            time.sleep(0.05)

        # block until received a valid frame
        while True:
            time.sleep(0.05)

            # capture frame
            success, frame = capture_device.read()

            # capture is successful and frame is valid
            if success and is_valid_image(frame):
                break

    # expose capture device
    return capture_device
