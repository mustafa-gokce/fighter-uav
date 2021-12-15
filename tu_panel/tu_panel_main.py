import time
import threading
import numpy
import cv2
import dearpygui.dearpygui as dearpygui
import tu_video.tu_video_utils as tu_video_utils
import tu_settings


def receive_video_stream(video_stream_port, video_stream_name):
    # create socket
    sub_socket = tu_video_utils.tu_video_socket_sub(tu_settings.tu_video_stream_ip_local,
                                                    video_stream_port)

    # delay first because of the socket bindings
    time.sleep(tu_settings.tu_video_stream_delay)

    while True:
        # get the contents
        my_data, my_image = tu_video_utils. tu_video_sub(sub_socket)
        my_image = cv2.resize(my_image, (640, 360), interpolation=cv2.INTER_AREA)
        data = numpy.flip(my_image, 2)
        data = data.ravel()
        data = numpy.asfarray(data, dtype="f")
        texture_data = numpy.true_divide(data, 255.0)
        dearpygui.set_value(video_stream_name, texture_data)
        global stop_threads
        if stop_threads >= 5:
            break


dearpygui.create_context()
dearpygui.create_viewport(title="tu_panel",
                          width=1920, height=1080, x_pos=0, y_pos=0,
                          resizable=False, decorated=False)

with dearpygui.texture_registry(show=False):
    dearpygui.add_raw_texture(640, 360, numpy.array(numpy.zeros((640, 360, 3)))[:], tag="tu_video_raw_frame",
                              format=dearpygui.mvFormat_Float_rgb)

with dearpygui.window(label="tu_video_raw",
                      pos=(0, 0), width=655, height=395,
                      no_title_bar=False, no_background=False, no_resize=True, no_move=True,
                      no_focus_on_appearing=True, no_bring_to_front_on_focus=True, no_scrollbar=True,
                      no_close=True, no_collapse=True):
    dearpygui.add_image("tu_video_raw_frame")

with dearpygui.texture_registry(show=False):
    dearpygui.add_raw_texture(640, 360, numpy.array(numpy.zeros((640, 360, 3)))[:], tag="tu_video_judge_frame",
                              format=dearpygui.mvFormat_Float_rgb)

with dearpygui.window(label="tu_video_judge",
                      pos=(0, 540), width=655, height=395,
                      no_title_bar=False, no_background=False, no_resize=True, no_move=True,
                      no_focus_on_appearing=True, no_bring_to_front_on_focus=True, no_scrollbar=True,
                      no_close=True, no_collapse=True):
    dearpygui.add_image("tu_video_judge_frame")

with dearpygui.texture_registry(show=False):
    dearpygui.add_raw_texture(640, 360, numpy.array(numpy.zeros((640, 360, 3)))[:], tag="tu_video_osd_frame",
                              format=dearpygui.mvFormat_Float_rgb)

with dearpygui.window(label="tu_video_osd",
                      pos=(1920 - 655, 0), width=655, height=395,
                      no_title_bar=False, no_background=False, no_resize=True, no_move=True,
                      no_focus_on_appearing=True, no_bring_to_front_on_focus=True, no_scrollbar=True,
                      no_close=True, no_collapse=True):
    dearpygui.add_image("tu_video_osd_frame")

with dearpygui.window(label="Example Window"):
    dearpygui.add_text("Hello, world")
    dearpygui.add_button(label="Save")
    dearpygui.add_input_text(label="string", default_value="Quick brown fox")
    dearpygui.add_slider_float(label="float", default_value=0.273, max_value=1)

with dearpygui.texture_registry(show=False):
    width, height, channels, data = dearpygui.load_image("../tu_asset/image/tu_image_0.png")
    dearpygui.add_static_texture(width, height, data, tag="tu_background_image")

with dearpygui.window(label="tu_background", pos=(int((1920 - 640) / 2), int((1080 - 320) / 2)),
                      no_title_bar=True, no_background=True,
                      no_resize=True, no_move=True,
                      no_focus_on_appearing=True, no_bring_to_front_on_focus=True):
    dearpygui.add_image("tu_background_image")

dearpygui.setup_dearpygui()
dearpygui.show_viewport()

stop_threads = 0
video_stream_threads = []
video_streams = {
    "tu_video_raw_frame": tu_settings.tu_video_stream_port_local_raw,
    "tu_video_judge_frame": tu_settings.tu_video_stream_port_local_judge,
    "tu_video_osd_frame": tu_settings.tu_video_stream_port_local_osd
}
for stream_name in video_streams.keys():
    video_stream_thread = threading.Thread(target=receive_video_stream, args=(video_streams[stream_name], stream_name))
    video_stream_thread.start()
    video_stream_threads.append(video_stream_thread)

while dearpygui.is_dearpygui_running():
    dearpygui.render_dearpygui_frame()
    if dearpygui.is_key_pressed(dearpygui.mvKey_Q):
        stop_threads += 1
    if stop_threads >= 5:
        dearpygui.destroy_context()
