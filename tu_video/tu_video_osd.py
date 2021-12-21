import cv2
import tu_video_utils
import tu_settings

# drawing related settings
hit_area_top_left = (int(tu_settings.tu_video_stream_width * 0.25), int(tu_settings.tu_video_stream_height * 0.1))
hit_area_bottom_right = (tu_settings.tu_video_stream_width - hit_area_top_left[0],
                         tu_settings.tu_video_stream_height - hit_area_top_left[1])
hit_area_color = (191, 64, 191)
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

# do below always
loop_count = 0
while True:
    # receive video stream from source
    my_data, my_image = tu_video_utils.tu_video_sub(sub_socket)

    # manipulate data
    my_data["osd_loop_count"] = loop_count

    # manipulate frame
    my_image = cv2.rectangle(my_image, hit_area_top_left, hit_area_bottom_right, hit_area_color, hit_area_thickness)
    my_image = cv2.putText(my_image, "TEST UCUSU", (5, 710),
                           osd_font, osd_font_scale, osd_font_color, osd_font_thickness, osd_font_line_type)
    my_image = cv2.putText(my_image, "TEKNOFEST 2022", (1005, 710),
                           osd_font, osd_font_scale, osd_font_color, osd_font_thickness, osd_font_line_type)

    # publish video stream to endpoints
    tu_video_utils.tu_video_pub(pub_socket, my_image, my_data)

    # update loop counter
    loop_count += 1
