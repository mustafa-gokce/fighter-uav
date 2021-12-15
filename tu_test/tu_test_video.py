import aiohttp.web
import asyncio
import cv2
import tu_settings


capture_device = cv2.VideoCapture(tu_settings.tu_video_stream_id_device)
capture_device.set(cv2.CAP_PROP_FRAME_WIDTH, tu_settings.tu_video_stream_width)
capture_device.set(cv2.CAP_PROP_FRAME_HEIGHT, tu_settings.tu_video_stream_height)
capture_device.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
capture_device.set(cv2.CAP_PROP_FPS, tu_settings.tu_video_stream_fps)


class StreamHandler:

    def __init__(self, camera):
        self._camera = camera

    async def __call__(self, request):
        my_boundary = "image-boundary"
        response = aiohttp.web.StreamResponse(
            status=200,
            reason="OK",
            headers={"Content-Type": "multipart/x-mixed-replace;boundary=image-boundary"}
        )
        await response.prepare(request)
        while True:
            frame = await self._camera.get_frame()
            with aiohttp.MultipartWriter("image/jpeg", boundary=my_boundary) as writer:
                writer.append(frame, {"Content-Type": "image/jpeg"})
                try:
                    await writer.write(response, close_boundary=False)
                except ConnectionResetError:
                    break
            await response.write(b"\r\n")


class MjpegServer:

    def __init__(self, host=tu_settings.tu_video_stream_ip_local, port=tu_settings.tu_video_stream_port_remote_raw):
        self._port = port
        self._host = host
        self._app = aiohttp.web.Application()
        self._cam_routes = []

    async def root_handler(self, request):
        text = "Available streams:\n\n"
        for route in self._cam_routes:
            text += f"{route} \n"
        return aiohttp.web.Response(text=text)

    def add_stream(self, route, camera):
        route = f"/{route}"
        self._cam_routes.append(route)
        assert hasattr(camera, "get_frame"), "arg 'cam' should have a 'get_frame' method"
        self._app.router.add_route("GET", f"{route}", StreamHandler(camera))

    def start(self):
        self._app.router.add_route("GET", "/", self.root_handler)
        aiohttp.web.run_app(self._app, host=self._host, port=self._port)

    def stop(self):
        pass


class Camera:

    def __init__(self, idx):
        self._idx = idx

    @property
    def identifier(self):
        return self._idx

    # The camera class should contain a "get_frame" method
    async def get_frame(self):
        success, image_frame = capture_device.read()
        image_frame = cv2.imencode(".jpg", image_frame)[1]
        await asyncio.sleep(1 / tu_settings.tu_video_stream_fps)
        return image_frame.tobytes()

    def stop(self):
        pass


if __name__ == "__main__":

    # Instantiate Server
    server = MjpegServer()

    # create lookup of routes and different camera objects
    cam = Camera(0)
    server.add_stream("stream.mjpg", cam)

    try:
        # start server
        server.start()

    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        cam.stop()
