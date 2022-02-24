import datetime
import cv2
import pyfakewebcam
import tu_video_util
import tu_telem.tu_telem_object
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

# create dummy sink for judge server streaming
sink_osd = pyfakewebcam.FakeWebcam(video_device=tu_settings.tu_video_stream_port_local_osd,
                                   width=tu_settings.tu_video_stream_width,
                                   height=tu_settings.tu_video_stream_height)

# create capture device
capture_device = tu_video_util.capture_device_create(port=tu_settings.tu_video_stream_port_local_raw)

# create telemetry receiver
telemetry_receiver = tu_telem.tu_telem_object.Receiver()

# do below always
while True:

    # try to do below
    try:

        # get time
        current_date = str(datetime.datetime.now())[:10:]

        # get telemetry data
        telemetry_data = telemetry_receiver.telemetry_get

        # process received telemetry data for stamping
        current_time = "{0:02d}:{1:02d}:{2:02d}.{3:03d}".format(telemetry_data.get("time", {}).get("hour", 0),
                                                                telemetry_data.get("time", {}).get("minute", 0),
                                                                telemetry_data.get("time", {}).get("second", 0),
                                                                telemetry_data.get("time", {}).get("millisecond", 0))
        current_latitude = "LAT: {0:.6f}".format(telemetry_data.get("location", {}).get("latitude", 0))
        current_longitude = "LON: {0:.6f}".format(telemetry_data.get("location", {}).get("longitude", 0))
        current_altitude = "ALT: {0:.2f}".format(telemetry_data.get("location", {}).get("altitude", 0))
        current_roll = "RLL: {0:.2f}".format(telemetry_data.get("attitude", {}).get("roll", 0))
        current_pitch = "PIT: {0:.2f}".format(telemetry_data.get("attitude", {}).get("pitch", 0))
        current_heading = "HDG: {0:.2f}".format(telemetry_data.get("attitude", {}).get("heading", 0))
        current_speed = "SPD: {0:.2f}".format(telemetry_data.get("speed", 0))
        current_battery = "BAT: {0:.2f}".format(telemetry_data.get("battery", 0))

        # get the image frame
        my_success, my_image = capture_device.read()

        # check frame capture was successful
        if my_success:

            # check image
            if tu_video_util.is_valid_image(my_image):

                # manipulate frame
                my_image = cv2.rectangle(my_image, hit_area_top_left, hit_area_bottom_right, hit_area_color,
                                         hit_area_thickness)
                my_image = cv2.putText(my_image, current_date, (5, 30),
                                       osd_font, osd_font_scale, osd_font_color, osd_font_thickness, osd_font_line_type)
                my_image = cv2.putText(my_image, current_time, (5, 60),
                                       osd_font, osd_font_scale, osd_font_color, osd_font_thickness, osd_font_line_type)
                my_image = cv2.putText(my_image, current_latitude, (5, 120),
                                       osd_font, osd_font_scale, osd_font_color, osd_font_thickness, osd_font_line_type)
                my_image = cv2.putText(my_image, current_longitude, (5, 150),
                                       osd_font, osd_font_scale, osd_font_color, osd_font_thickness, osd_font_line_type)
                my_image = cv2.putText(my_image, current_altitude, (5, 180),
                                       osd_font, osd_font_scale, osd_font_color, osd_font_thickness, osd_font_line_type)
                my_image = cv2.putText(my_image, current_roll, (5, 240),
                                       osd_font, osd_font_scale, osd_font_color, osd_font_thickness, osd_font_line_type)
                my_image = cv2.putText(my_image, current_pitch, (5, 270),
                                       osd_font, osd_font_scale, osd_font_color, osd_font_thickness, osd_font_line_type)
                my_image = cv2.putText(my_image, current_heading, (5, 300),
                                       osd_font, osd_font_scale, osd_font_color, osd_font_thickness, osd_font_line_type)
                my_image = cv2.putText(my_image, current_speed, (5, 360),
                                       osd_font, osd_font_scale, osd_font_color, osd_font_thickness, osd_font_line_type)
                my_image = cv2.putText(my_image, current_battery, (5, 390),
                                       osd_font, osd_font_scale, osd_font_color, osd_font_thickness, osd_font_line_type)
                my_image = cv2.putText(my_image, "TEST UCUSU", (5, 710),
                                       osd_font, osd_font_scale, osd_font_color, osd_font_thickness, osd_font_line_type)
                my_image = cv2.putText(my_image, "TEKNOFEST 2022", (1005, 710),
                                       osd_font, osd_font_scale, osd_font_color, osd_font_thickness, osd_font_line_type)

                # change color space if testing
                if tu_settings.tu_video_stream_test:
                    # convert image to RGB
                    my_image = cv2.cvtColor(my_image, cv2.COLOR_BGR2RGB)

                # send image frame to judge sink
                sink_osd.schedule_frame(my_image)

    # catch all exceptions
    except Exception as e:
        pass
