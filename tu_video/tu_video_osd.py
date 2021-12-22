import time
import cv2
import tu_video_utils
import tu_settings

# drawing related settings
hit_area_top_left = (int(tu_settings.tu_video_stream_width * 0.25), int(tu_settings.tu_video_stream_height * 0.1))
hit_area_bottom_right = (tu_settings.tu_video_stream_width - hit_area_top_left[0],
                         tu_settings.tu_video_stream_height - hit_area_top_left[1])
hit_area_color = (0, 255, 0)
hit_area_thickness = 5
osd_font = cv2.FONT_HERSHEY_SIMPLEX
osd_font_scale = 1
osd_font_color = (0, 255, 0)
osd_font_thickness = 2
osd_font_line_type = cv2.LINE_AA

# create sub socket
sub_socket = tu_video_utils.tu_video_create_sub(tu_settings.tu_video_stream_ip_local,
                                                tu_settings.tu_video_stream_port_local_raw)

# create pub socket
pub_socket = tu_video_utils.tu_video_create_pub(tu_settings.tu_video_stream_port_local_osd)

# loop related variables
loop_count = 0
time_initial = 0
time_receive = 0
time_plot = 0
time_publish = 0
time_delta_loop = 0
time_delta_receive = 0
time_delta_plot = 0
time_delta_publish = 0
fps_loop = 0
fps_receive = 0
fps_plot = 0
fps_publish = 0

# do below always
while True:
    # initial time
    time_initial = time.time()

    # receive video stream from source
    my_data, my_image = tu_video_utils.tu_video_sub(sub_socket)

    # time after receiving a frame
    time_receive = time.time()

    # manipulate data
    my_data["osd_loop_count"] = loop_count
    my_data["osd_time_initial"] = time_initial
    my_data["osd_time_receive"] = time_receive
    my_data["osd_time_plot"] = time_plot
    my_data["osd_time_publish"] = time_publish
    my_data["osd_time_delta_loop"] = time_delta_loop
    my_data["osd_time_delta_receive"] = time_delta_receive
    my_data["osd_time_delta_plot"] = time_delta_plot
    my_data["osd_time_delta_publish"] = time_delta_publish
    my_data["osd_fps_loop"] = fps_loop
    my_data["osd_fps_receive"] = fps_receive
    my_data["osd_fps_plot"] = fps_plot
    my_data["osd_fps_publish"] = fps_publish

    # manipulate frame
    my_image = cv2.rectangle(my_image, hit_area_top_left, hit_area_bottom_right, hit_area_color, hit_area_thickness)
    my_image = cv2.putText(my_image, "{0:07d}".format(loop_count), (5, 30),
                           osd_font, osd_font_scale, osd_font_color, osd_font_thickness, osd_font_line_type)
    my_image = cv2.putText(my_image, "FPS:" + str(fps_receive), (5, 60),
                           osd_font, osd_font_scale, osd_font_color, osd_font_thickness, osd_font_line_type)
    my_image = cv2.putText(my_image, "TEST UCUSU", (5, 710),
                           osd_font, osd_font_scale, osd_font_color, osd_font_thickness, osd_font_line_type)
    my_image = cv2.putText(my_image, "TEKNOFEST 2022", (1005, 710),
                           osd_font, osd_font_scale, osd_font_color, osd_font_thickness, osd_font_line_type)

    # time after plotting osd
    time_plot = time.time()

    # publish video stream to endpoints
    tu_video_utils.tu_video_pub(pub_socket, my_image, my_data)

    # time after publishing to remote
    time_publish = time.time()

    # calculate time delta
    time_delta_loop = time_publish - time_initial
    time_delta_receive = time_receive - time_initial
    time_delta_plot = time_plot - time_receive
    time_delta_publish = time_publish - time_receive
    fps_loop = int(time_delta_loop and 1.0 / time_delta_loop or 0)
    fps_receive = int(time_delta_receive and 1.0 / time_delta_receive or 0)
    fps_plot = int(time_delta_plot and 1.0 / time_delta_plot or 0)
    fps_publish = int(time_delta_publish and 1.0 / time_delta_publish or 0)

    # update loop counter
    loop_count += 1
