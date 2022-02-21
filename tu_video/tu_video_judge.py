import sys
import cv2
import pyfakewebcam
import tu_video_utils
import tu_settings

# drawing related settings
hit_area_top_left = (int(tu_settings.tu_video_stream_width * 0.25), int(tu_settings.tu_video_stream_height * 0.1))
hit_area_bottom_right = (tu_settings.tu_video_stream_width - hit_area_top_left[0],
                         tu_settings.tu_video_stream_height - hit_area_top_left[1])
hit_area_color = (191, 64, 191)
hit_area_thickness = 5

# create sub socket
sub_socket = tu_video_utils.tu_video_create_sub(ip=tu_settings.tu_video_stream_ip_local,
                                                port=tu_settings.tu_video_stream_port_local_raw)

# create pub socket
pub_socket = tu_video_utils.tu_video_create_pub(ip=tu_settings.tu_video_stream_ip_local,
                                                port=tu_settings.tu_video_stream_port_local_judge)

# create dummy sink for judge server streaming
judge_sink = pyfakewebcam.FakeWebcam(video_device="/dev/video26",
                                     width=tu_settings.tu_video_stream_width,
                                     height=tu_settings.tu_video_stream_height)

# do below always
loop_count = 0
while True:

    # receive video stream from source
    my_data, my_image = tu_video_utils.tu_video_sub(socket=sub_socket)

    # manipulate data
    my_data["judge_loop_count"] = loop_count

    # manipulate frame
    my_image = cv2.rectangle(my_image, hit_area_top_left, hit_area_bottom_right, hit_area_color, hit_area_thickness)

    # publish video stream to endpoints
    tu_video_utils.tu_video_pub(socket=pub_socket,
                                image=my_image,
                                data=my_data)

    # send image frame to judge sink
    judge_sink.schedule_frame(my_image)

    # update loop counter
    loop_count += 1
