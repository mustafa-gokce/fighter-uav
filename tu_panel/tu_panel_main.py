import threading
import datetime
import time
import numpy
import cv2
import dearpygui.dearpygui as dearpygui
import tu_video.tu_video_util
import tu_telem.tu_telem_object
import settings

# global variables
log_count = 0
stop_threads = 0
video_streams = {
    "tu_video_raw_frame": tu_settings.video_stream_port_local_raw,
    "tu_video_judge_frame": tu_settings.video_stream_port_local_judge,
    "tu_video_osd_frame": tu_settings.video_stream_port_local_osd
}
video_stream_threads = []
telemetry_stream_thread = None


# get current date and time
def get_time():
    now = datetime.datetime.now()
    now = "{0:02d}:{1:02d}:{2:02d}.{3:03d}".format(now.hour, now.minute, now.second, int(now.microsecond / 1000))
    return now


# write log to screen
def log_writer(severity, context, message):
    global log_count
    log_count += 1

    # log messages
    with dearpygui.table_row(tag="row" + str(log_count), parent="tu_system_log_tag_table",
                             before="row" + str(log_count - 1)):
        with dearpygui.table_cell():
            dearpygui.add_text(get_time(), tag="timestamp" + str(log_count))
        with dearpygui.table_cell():
            dearpygui.add_text(severity, tag="severity" + str(log_count))
        with dearpygui.table_cell():
            dearpygui.add_text(context, tag="context" + str(log_count))
        with dearpygui.table_cell():
            dearpygui.add_text(message, tag="message" + str(log_count))


# receive video stream
def receive_video_stream(video_stream_port, video_stream_name):
    # get global variables
    global stop_threads

    # create capture device
    capture_device = tu_video.tu_video_util.capture_device_create(video_stream_port)

    # do below always
    while True:

        # try to get image frame
        try:

            # get the contents
            my_success, my_image = capture_device.read()

            # check frame capture was successful
            if my_success:

                # check image
                if tu_video.tu_video_util.is_valid_image(my_image):
                    # resize received image
                    my_image = cv2.resize(my_image, (640, 360), interpolation=cv2.INTER_AREA)

                    # change color space from BGR to RGB of the received image
                    my_image = numpy.flip(my_image, 2)

                    # ravel the image
                    my_image = my_image.ravel()

                    # create float array for GPU acceleration benefit of interface
                    my_image = numpy.asfarray(my_image, dtype="f")

                    # create texture to be shown on interface
                    texture_data = numpy.true_divide(my_image, 255.0)

                    # update texture
                    dearpygui.set_value(video_stream_name, texture_data)

        # catch all exceptions
        except Exception as e:
            pass

        # kill the thread if user wanted exit
        if stop_threads >= 5:
            capture_device.release()
            break


def receive_telemetry_stream():
    # get global variables
    global stop_threads

    # create telemetry receiver
    telemetry_receiver = tu_telem.tu_telem_object.Receiver()

    # do below always
    while True:

        # try to get telemetry data
        try:

            # get telemetry data
            telemetry_data = telemetry_receiver.telemetry_get

            # update telemetry data related fields
            dearpygui.set_value(item="tu_system_data_tag_latitude_vehicle_value",
                                value="{0:.6f}".format(telemetry_data.get("location", {}).get("latitude", 0)))
            dearpygui.set_value(item="tu_system_data_tag_longitude_vehicle_value",
                                value="{0:.6f}".format(telemetry_data.get("location", {}).get("longitude", 0)))
            dearpygui.set_value(item="tu_system_data_tag_altitude_vehicle_value",
                                value="{0:.2f}".format(telemetry_data.get("location", {}).get("altitude", 0)))
            dearpygui.set_value(item="tu_system_data_tag_latitude_target_value",
                                value="{0:.6f}".format(
                                    telemetry_data.get("foe", {}).get("location", {}).get("latitude", 0)))
            dearpygui.set_value(item="tu_system_data_tag_longitude_target_value",
                                value="{0:.6f}".format(
                                    telemetry_data.get("foe", {}).get("location", {}).get("longitude", 0)))
            dearpygui.set_value(item="tu_system_data_tag_altitude_target_value",
                                value="{0:.2f}".format(
                                    telemetry_data.get("foe", {}).get("location", {}).get("altitude", 0)))
            dearpygui.set_value(item="tu_system_data_tag_roll_vehicle_value",
                                value="{0:.2f}".format(telemetry_data.get("attitude", {}).get("roll", 0)))
            dearpygui.set_value(item="tu_system_data_tag_pitch_vehicle_value",
                                value="{0:.2f}".format(telemetry_data.get("attitude", {}).get("pitch", 0)))
            dearpygui.set_value(item="tu_system_data_tag_heading_vehicle_value",
                                value="{0:.2f}".format(telemetry_data.get("attitude", {}).get("heading", 0)))
            dearpygui.set_value(item="tu_system_data_tag_roll_target_value",
                                value="{0:.2f}".format(
                                    telemetry_data.get("foe", {}).get("attitude", {}).get("roll", 0)))
            dearpygui.set_value(item="tu_system_data_tag_pitch_target_value",
                                value="{0:.2f}".format(
                                    telemetry_data.get("foe", {}).get("attitude", {}).get("pitch", 0)))
            dearpygui.set_value(item="tu_system_data_tag_heading_target_value",
                                value="{0:.2f}".format(
                                    telemetry_data.get("foe", {}).get("attitude", {}).get("heading", 0)))
            dearpygui.set_value(item="tu_system_data_tag_team_vehicle_value",
                                value="{0}".format(telemetry_data.get("team", 0)))
            dearpygui.set_value(item="tu_system_data_tag_team_target_value",
                                value="{0}".format(telemetry_data.get("foe", {}).get("team", 0)))
            dearpygui.set_value(item="tu_system_data_tag_mode_vehicle_value",
                                value="{0}".format(telemetry_data.get("flight_mode", "UNKNOWN")))
            dearpygui.set_value(item="tu_system_data_tag_lock_target_value",
                                value="{0}".format(telemetry_data.get("target", {}).get("lock", 0)))
            dearpygui.set_value(item="tu_system_data_tag_arm_vehicle_value",
                                value="{0}".format(telemetry_data.get("armed", "UNKNOWN")).upper())
            dearpygui.set_value(item="tu_system_data_tag_x_target_value",
                                value="{0}".format(telemetry_data.get("target", {}).get("x", 0)))
            dearpygui.set_value(item="tu_system_data_tag_telem_vehicle_value",
                                value="{0}".format(telemetry_data.get("connected", "UNKNOWN")).upper())
            dearpygui.set_value(item="tu_system_data_tag_y_target_value",
                                value="{0}".format(telemetry_data.get("target", {}).get("y", 0)))
            dearpygui.set_value(item="tu_system_data_tag_judge_vehicle_value",
                                value="{0}".format(telemetry_data.get("judge", {}).get("logged_in", "UNKNOWN")).upper())
            dearpygui.set_value(item="tu_system_data_tag_width_target_value",
                                value="{0}".format(telemetry_data.get("target", {}).get("width", 0)))
            dearpygui.set_value(item="tu_system_data_tag_interop_vehicle_value",
                                value="{0}".format(
                                    telemetry_data.get("judge", {}).get("allowed_interop", "UNKNOWN")).upper())
            dearpygui.set_value(item="tu_system_data_tag_height_target_value",
                                value="{0}".format(telemetry_data.get("target", {}).get("height", 0)))
            dearpygui.set_value(item="tu_system_data_tag_groundspeed_vehicle_value",
                                value="{0:.2f}".format(telemetry_data.get("speed", 0)))
            dearpygui.set_value(item="tu_system_data_tag_battery_vehicle_value",
                                value="{0:.2f}".format(telemetry_data.get("battery", 0)))
            dearpygui.set_value(item="tu_system_data_tag_start_target_value",
                                value="{0:02d}:{1:02d}:{2:02d}.{3:03d}".format(
                                    telemetry_data.get("target", {}).get("time_start", {}).get("hour", 0),
                                    telemetry_data.get("target", {}).get("time_start", {}).get("minute", 0),
                                    telemetry_data.get("target", {}).get("time_start", {}).get("second", 0),
                                    telemetry_data.get("target", {}).get("time_start", {}).get("millisecond", 0)))
            dearpygui.set_value(item="tu_system_data_tag_end_target_value",
                                value="{0:02d}:{1:02d}:{2:02d}.{3:03d}".format(
                                    telemetry_data.get("target", {}).get("time_end", {}).get("hour", 0),
                                    telemetry_data.get("target", {}).get("time_end", {}).get("minute", 0),
                                    telemetry_data.get("target", {}).get("time_end", {}).get("second", 0),
                                    telemetry_data.get("target", {}).get("time_end", {}).get("millisecond", 0)))

        # catch all exceptions
        except Exception as e:
            pass

        # kill the thread if user wanted exit
        if stop_threads >= 5:
            break

        # cool down the update rate
        time.sleep(0.2)


# flight mode change callback
def flight_command_callback(sender, data):
    if sender == "flight_mode_selection":
        log_writer("DEBUG", "PANEL", "Flight mode selected to: " + data)
    elif sender == "flight_mode_deploy":
        data = dearpygui.get_value("flight_mode_selection")
        if data != "Select flight mode":
            log_writer("DEBUG", "PANEL", "Flight mode deployed to: " + data)


# create interface context
dearpygui.create_context()

# create interface viewport
dearpygui.create_viewport(title="tu_panel",
                          width=1920, height=1080, x_pos=0, y_pos=0,
                          resizable=False, decorated=False)

# register raw frame texture
with dearpygui.texture_registry(show=False):
    dearpygui.add_raw_texture(640, 360, numpy.array(numpy.zeros((640, 360, 3)))[:], tag="tu_video_raw_frame",
                              format=dearpygui.mvFormat_Float_rgb)

# create window for raw frame
with dearpygui.window(label="tu_video_raw",
                      pos=(0, 0), width=655, height=395,
                      no_title_bar=False, no_background=False, no_resize=True, no_move=True,
                      no_focus_on_appearing=True, no_bring_to_front_on_focus=True, no_scrollbar=True,
                      no_close=True, no_collapse=True):
    # add image to window
    dearpygui.add_image("tu_video_raw_frame")

# register judge frame texture
with dearpygui.texture_registry(show=False):
    dearpygui.add_raw_texture(640, 360, numpy.array(numpy.zeros((640, 360, 3)))[:], tag="tu_video_judge_frame",
                              format=dearpygui.mvFormat_Float_rgb)

# create window for judge frame
with dearpygui.window(label="tu_video_judge",
                      pos=(0, 400), width=655, height=395,
                      no_title_bar=False, no_background=False, no_resize=True, no_move=True,
                      no_focus_on_appearing=True, no_bring_to_front_on_focus=True, no_scrollbar=True,
                      no_close=True, no_collapse=True):
    # add image to window
    dearpygui.add_image("tu_video_judge_frame")

# register osd frame texture
with dearpygui.texture_registry(show=False):
    dearpygui.add_raw_texture(640, 360, numpy.array(numpy.zeros((640, 360, 3)))[:], tag="tu_video_osd_frame",
                              format=dearpygui.mvFormat_Float_rgb)

# create window for osd frame
with dearpygui.window(label="tu_video_osd",
                      pos=(1920 - 655, 0), width=655, height=395,
                      no_title_bar=False, no_background=False, no_resize=True, no_move=True,
                      no_focus_on_appearing=True, no_bring_to_front_on_focus=True, no_scrollbar=True,
                      no_close=True, no_collapse=True):
    # add image to window
    dearpygui.add_image("tu_video_osd_frame")

# create window for flight plot
with dearpygui.window(label="tu_comp_plot",
                      pos=(1920 - 655, 400), width=655, height=675,
                      no_title_bar=False, no_background=False, no_resize=True, no_move=True,
                      no_focus_on_appearing=True, no_bring_to_front_on_focus=True, no_scrollbar=True,
                      no_close=True, no_collapse=True):
    with dearpygui.plot(label="tu_flight_plot", width=640, height=640, fit_button=True, no_title=True):
        dearpygui.add_plot_axis(0, tag="x")
        dearpygui.add_plot_axis(1, tag="y")
        dearpygui.add_plot_legend()
        dearpygui.set_axis_limits("x", -500, 500)
        dearpygui.set_axis_limits("y", -500, 500)
        dearpygui.add_scatter_series(x=[0, ], y=[0, ], parent="x", label="Station", tag="location_station")
        dearpygui.add_scatter_series(x=[100, ], y=[100, ], parent="x", label="Vehicle", tag="location_vehicle")
        dearpygui.add_scatter_series(x=[-100, -400, -300, 400, 100], y=[100, 300, -400, 100, -200],
                                     parent="x", label="Foe", tag="location_foe")
        # dearpygui.add_line_series([100, 100, 100, 200], [200, 200, 100, 100], parent="x")
        # dearpygui.set_value("location_station", [[200, ], [200, ]])

# create window for vehicle command
with dearpygui.window(label="tu_system_command",
                      pos=(0, 800), width=655, height=275,
                      no_title_bar=False, no_background=False, no_resize=True, no_move=True,
                      no_focus_on_appearing=True, no_bring_to_front_on_focus=True, no_scrollbar=True,
                      no_close=True, no_collapse=True):
    # create mode changing widgets
    dearpygui.add_combo(items=("MANUAL", "STABILIZE", "FBWA", "FBWB", "CRUISE", "LOITER", "AUTO", "GUIDED", "RTL"),
                        width=175, tag="flight_mode_selection", default_value="Select flight mode",
                        callback=flight_command_callback)
    dearpygui.add_button(label="Change flight mode", width=175, tag="flight_mode_deploy",
                         callback=flight_command_callback)

    # create safety changing widgets
    dearpygui.add_combo(items=("ARM", "DISARM", "FORCE ARM", "FORCE DISARM"), width=175, tag="flight_safety_selection",
                        pos=(7, 90), default_value="Select flight safety", callback=flight_command_callback)
    dearpygui.add_button(label="Change flight safety", width=175, tag="flight_safety_deploy", pos=(7, 113),
                         callback=flight_command_callback)

# create window for vehicle data
with dearpygui.window(label="tu_system_data",
                      pos=(660, 700), width=600, height=375,
                      no_title_bar=False, no_background=False, no_resize=True, no_move=True,
                      no_focus_on_appearing=True, no_bring_to_front_on_focus=True, no_scrollbar=True,
                      no_close=True, no_collapse=True):
    # create table for vehicle data
    with dearpygui.table(label="tu_system_data_table", tag="tu_system_data_tag_table",
                         header_row=True, resizable=False,
                         policy=dearpygui.mvTable_SizingStretchProp,
                         borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True):
        # add columns to vehicle data table
        dearpygui.add_table_column(label="data",
                                   tag="tu_system_data_tag_data_left",
                                   parent="tu_system_data_tag_table")
        dearpygui.add_table_column(label="value",
                                   tag="tu_system_data_tag_value_left",
                                   parent="tu_system_data_tag_table")
        dearpygui.add_table_column(label="data",
                                   tag="tu_system_data_tag_data_right",
                                   parent="tu_system_data_tag_table")
        dearpygui.add_table_column(label="value",
                                   tag="tu_system_data_tag_value_right",
                                   parent="tu_system_data_tag_table")

        # add rows
        for i in range(14):
            dearpygui.add_table_row(tag="tu_system_data_tag_row_{0}".format(i + 1),
                                    parent="tu_system_data_tag_table")

        # add vehicle latitude
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_latitude_vehicle_name",
                                 parent="tu_system_data_tag_row_1")
        dearpygui.add_text(default_value="Vehicle Latitude",
                           tag="tu_system_data_tag_latitude_vehicle_name",
                           parent="tu_system_data_tag_cell_latitude_vehicle_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_latitude_vehicle_value",
                                 parent="tu_system_data_tag_row_1")
        dearpygui.add_text(default_value="0.000000",
                           tag="tu_system_data_tag_latitude_vehicle_value",
                           parent="tu_system_data_tag_cell_latitude_vehicle_value")

        # add vehicle longitude
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_longitude_vehicle_name",
                                 parent="tu_system_data_tag_row_2")
        dearpygui.add_text(default_value="Vehicle Longitude",
                           tag="tu_system_data_tag_longitude_vehicle_name",
                           parent="tu_system_data_tag_cell_longitude_vehicle_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_longitude_vehicle_value",
                                 parent="tu_system_data_tag_row_2")
        dearpygui.add_text(default_value="0.000000",
                           tag="tu_system_data_tag_longitude_vehicle_value",
                           parent="tu_system_data_tag_cell_longitude_vehicle_value")

        # add vehicle altitude
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_altitude_vehicle_name",
                                 parent="tu_system_data_tag_row_3")
        dearpygui.add_text(default_value="Vehicle Altitude",
                           tag="tu_system_data_tag_altitude_vehicle_name",
                           parent="tu_system_data_tag_cell_altitude_vehicle_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_altitude_vehicle_value",
                                 parent="tu_system_data_tag_row_3")
        dearpygui.add_text(default_value="0.00",
                           tag="tu_system_data_tag_altitude_vehicle_value",
                           parent="tu_system_data_tag_cell_altitude_vehicle_value")

        # add vehicle roll
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_roll_vehicle_name",
                                 parent="tu_system_data_tag_row_4")
        dearpygui.add_text(default_value="Vehicle Roll",
                           tag="tu_system_data_tag_roll_vehicle_name",
                           parent="tu_system_data_tag_cell_roll_vehicle_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_roll_vehicle_value",
                                 parent="tu_system_data_tag_row_4")
        dearpygui.add_text(default_value="0.00",
                           tag="tu_system_data_tag_roll_vehicle_value",
                           parent="tu_system_data_tag_cell_roll_vehicle_value")

        # add vehicle pitch
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_pitch_vehicle_name",
                                 parent="tu_system_data_tag_row_5")
        dearpygui.add_text(default_value="Vehicle Pitch",
                           tag="tu_system_data_tag_pitch_vehicle_name",
                           parent="tu_system_data_tag_cell_pitch_vehicle_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_pitch_vehicle_value",
                                 parent="tu_system_data_tag_row_5")
        dearpygui.add_text(default_value="0.00",
                           tag="tu_system_data_tag_pitch_vehicle_value",
                           parent="tu_system_data_tag_cell_pitch_vehicle_value")

        # add vehicle heading
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_heading_vehicle_name",
                                 parent="tu_system_data_tag_row_6")
        dearpygui.add_text(default_value="Vehicle Heading",
                           tag="tu_system_data_tag_heading_vehicle_name",
                           parent="tu_system_data_tag_cell_heading_vehicle_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_heading_vehicle_value",
                                 parent="tu_system_data_tag_row_6")
        dearpygui.add_text(default_value="0.00",
                           tag="tu_system_data_tag_heading_vehicle_value",
                           parent="tu_system_data_tag_cell_heading_vehicle_value")

        # add vehicle arm status
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_arm_vehicle_name",
                                 parent="tu_system_data_tag_row_7")
        dearpygui.add_text(default_value="Arm Status",
                           tag="tu_system_data_tag_arm_vehicle_name",
                           parent="tu_system_data_tag_cell_arm_vehicle_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_arm_vehicle_value",
                                 parent="tu_system_data_tag_row_7")
        dearpygui.add_text(default_value="UNKNOWN",
                           tag="tu_system_data_tag_arm_vehicle_value",
                           parent="tu_system_data_tag_cell_arm_vehicle_value")

        # add vehicle flight mode
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_mode_vehicle_name",
                                 parent="tu_system_data_tag_row_8")
        dearpygui.add_text(default_value="Flight Mode",
                           tag="tu_system_data_tag_mode_vehicle_name",
                           parent="tu_system_data_tag_cell_mode_vehicle_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_mode_vehicle_value",
                                 parent="tu_system_data_tag_row_8")
        dearpygui.add_text(default_value="UNKNOWN",
                           tag="tu_system_data_tag_mode_vehicle_value",
                           parent="tu_system_data_tag_cell_mode_vehicle_value")

        # add vehicle ground speed
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_groundspeed_vehicle_name",
                                 parent="tu_system_data_tag_row_9")
        dearpygui.add_text(default_value="Ground Speed",
                           tag="tu_system_data_tag_groundspeed_vehicle_name",
                           parent="tu_system_data_tag_cell_groundspeed_vehicle_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_groundspeed_vehicle_value",
                                 parent="tu_system_data_tag_row_9")
        dearpygui.add_text(default_value="0",
                           tag="tu_system_data_tag_groundspeed_vehicle_value",
                           parent="tu_system_data_tag_cell_groundspeed_vehicle_value")

        # add vehicle battery
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_battery_vehicle_name",
                                 parent="tu_system_data_tag_row_10")
        dearpygui.add_text(default_value="Battery Level",
                           tag="tu_system_data_tag_battery_vehicle_name",
                           parent="tu_system_data_tag_cell_battery_vehicle_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_battery_vehicle_value",
                                 parent="tu_system_data_tag_row_10")
        dearpygui.add_text(default_value="0",
                           tag="tu_system_data_tag_battery_vehicle_value",
                           parent="tu_system_data_tag_cell_battery_vehicle_value")

        # add vehicle id
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_team_vehicle_name",
                                 parent="tu_system_data_tag_row_11")
        dearpygui.add_text(default_value="Team ID",
                           tag="tu_system_data_tag_team_vehicle_name",
                           parent="tu_system_data_tag_cell_team_vehicle_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_team_vehicle_value",
                                 parent="tu_system_data_tag_row_11")
        dearpygui.add_text(default_value="0",
                           tag="tu_system_data_tag_team_vehicle_value",
                           parent="tu_system_data_tag_cell_team_vehicle_value")

        # add vehicle telemetry connection status
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_telem_vehicle_name",
                                 parent="tu_system_data_tag_row_12")
        dearpygui.add_text(default_value="Telemetry Connected",
                           tag="tu_system_data_tag_telem_vehicle_name",
                           parent="tu_system_data_tag_cell_telem_vehicle_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_telem_vehicle_value",
                                 parent="tu_system_data_tag_row_12")
        dearpygui.add_text(default_value="UNKNOWN",
                           tag="tu_system_data_tag_telem_vehicle_value",
                           parent="tu_system_data_tag_cell_telem_vehicle_value")

        # add vehicle judge connection status
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_judge_vehicle_name",
                                 parent="tu_system_data_tag_row_13")
        dearpygui.add_text(default_value="Judge Connected",
                           tag="tu_system_data_tag_judge_vehicle_name",
                           parent="tu_system_data_tag_cell_judge_vehicle_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_judge_vehicle_value",
                                 parent="tu_system_data_tag_row_13")
        dearpygui.add_text(default_value="UNKNOWN",
                           tag="tu_system_data_tag_judge_vehicle_value",
                           parent="tu_system_data_tag_cell_judge_vehicle_value")

        # add vehicle judge interop status
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_interop_vehicle_name",
                                 parent="tu_system_data_tag_row_14")
        dearpygui.add_text(default_value="Allowed Interop",
                           tag="tu_system_data_tag_interop_vehicle_name",
                           parent="tu_system_data_tag_cell_interop_vehicle_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_interop_vehicle_value",
                                 parent="tu_system_data_tag_row_14")
        dearpygui.add_text(default_value="UNKNOWN",
                           tag="tu_system_data_tag_interop_vehicle_value",
                           parent="tu_system_data_tag_cell_interop_vehicle_value")

        # add target latitude
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_latitude_target_name",
                                 parent="tu_system_data_tag_row_1")
        dearpygui.add_text(default_value="Target Latitude",
                           tag="tu_system_data_tag_latitude_target_name",
                           parent="tu_system_data_tag_cell_latitude_target_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_latitude_target_value",
                                 parent="tu_system_data_tag_row_1")
        dearpygui.add_text(default_value="0.000000",
                           tag="tu_system_data_tag_latitude_target_value",
                           parent="tu_system_data_tag_cell_latitude_target_value")

        # add target longitude
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_longitude_target_name",
                                 parent="tu_system_data_tag_row_2")
        dearpygui.add_text(default_value="Target Longitude",
                           tag="tu_system_data_tag_longitude_target_name",
                           parent="tu_system_data_tag_cell_longitude_target_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_longitude_target_value",
                                 parent="tu_system_data_tag_row_2")
        dearpygui.add_text(default_value="0.000000",
                           tag="tu_system_data_tag_longitude_target_value",
                           parent="tu_system_data_tag_cell_longitude_target_value")

        # add target altitude
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_altitude_target_name",
                                 parent="tu_system_data_tag_row_3")
        dearpygui.add_text(default_value="Target Altitude",
                           tag="tu_system_data_tag_altitude_target_name",
                           parent="tu_system_data_tag_cell_altitude_target_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_altitude_target_value",
                                 parent="tu_system_data_tag_row_3")
        dearpygui.add_text(default_value="0.00",
                           tag="tu_system_data_tag_altitude_target_value",
                           parent="tu_system_data_tag_cell_altitude_target_value")

        # add target roll
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_roll_target_name",
                                 parent="tu_system_data_tag_row_4")
        dearpygui.add_text(default_value="Target Roll",
                           tag="tu_system_data_tag_roll_target_name",
                           parent="tu_system_data_tag_cell_roll_target_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_roll_target_value",
                                 parent="tu_system_data_tag_row_4")
        dearpygui.add_text(default_value="0.00",
                           tag="tu_system_data_tag_roll_target_value",
                           parent="tu_system_data_tag_cell_roll_target_value")

        # add target pitch
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_pitch_target_name",
                                 parent="tu_system_data_tag_row_5")
        dearpygui.add_text(default_value="Target Pitch",
                           tag="tu_system_data_tag_pitch_target_name",
                           parent="tu_system_data_tag_cell_pitch_target_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_pitch_target_value",
                                 parent="tu_system_data_tag_row_5")
        dearpygui.add_text(default_value="0.00",
                           tag="tu_system_data_tag_pitch_target_value",
                           parent="tu_system_data_tag_cell_pitch_target_value")

        # add target heading
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_heading_target_name",
                                 parent="tu_system_data_tag_row_6")
        dearpygui.add_text(default_value="Target Heading",
                           tag="tu_system_data_tag_heading_target_name",
                           parent="tu_system_data_tag_cell_heading_target_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_heading_target_value",
                                 parent="tu_system_data_tag_row_6")
        dearpygui.add_text(default_value="0.00",
                           tag="tu_system_data_tag_heading_target_value",
                           parent="tu_system_data_tag_cell_heading_target_value")

        # add target id
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_team_target_name",
                                 parent="tu_system_data_tag_row_7")
        dearpygui.add_text(default_value="Target ID",
                           tag="tu_system_data_tag_team_target_name",
                           parent="tu_system_data_tag_cell_team_target_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_team_target_value",
                                 parent="tu_system_data_tag_row_7")
        dearpygui.add_text(default_value="0",
                           tag="tu_system_data_tag_team_target_value",
                           parent="tu_system_data_tag_cell_team_target_value")

        # add target lock
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_lock_target_name",
                                 parent="tu_system_data_tag_row_8")
        dearpygui.add_text(default_value="Target Lock",
                           tag="tu_system_data_tag_lock_target_name",
                           parent="tu_system_data_tag_cell_lock_target_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_lock_target_value",
                                 parent="tu_system_data_tag_row_8")
        dearpygui.add_text(default_value="0",
                           tag="tu_system_data_tag_lock_target_value",
                           parent="tu_system_data_tag_cell_lock_target_value")

        # add target pixel x
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_x_target_name",
                                 parent="tu_system_data_tag_row_9")
        dearpygui.add_text(default_value="Target X",
                           tag="tu_system_data_tag_x_target_name",
                           parent="tu_system_data_tag_cell_x_target_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_x_target_value",
                                 parent="tu_system_data_tag_row_9")
        dearpygui.add_text(default_value="0",
                           tag="tu_system_data_tag_x_target_value",
                           parent="tu_system_data_tag_cell_x_target_value")

        # add target pixel y
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_y_target_name",
                                 parent="tu_system_data_tag_row_10")
        dearpygui.add_text(default_value="Target Y",
                           tag="tu_system_data_tag_y_target_name",
                           parent="tu_system_data_tag_cell_y_target_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_y_target_value",
                                 parent="tu_system_data_tag_row_10")
        dearpygui.add_text(default_value="0",
                           tag="tu_system_data_tag_y_target_value",
                           parent="tu_system_data_tag_cell_y_target_value")

        # add target pixel width
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_width_target_name",
                                 parent="tu_system_data_tag_row_11")
        dearpygui.add_text(default_value="Target Width",
                           tag="tu_system_data_tag_width_target_name",
                           parent="tu_system_data_tag_cell_width_target_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_width_target_value",
                                 parent="tu_system_data_tag_row_11")
        dearpygui.add_text(default_value="0",
                           tag="tu_system_data_tag_width_target_value",
                           parent="tu_system_data_tag_cell_width_target_value")

        # add target pixel height
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_height_target_name",
                                 parent="tu_system_data_tag_row_12")
        dearpygui.add_text(default_value="Target Height",
                           tag="tu_system_data_tag_height_target_name",
                           parent="tu_system_data_tag_cell_height_target_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_height_target_value",
                                 parent="tu_system_data_tag_row_12")
        dearpygui.add_text(default_value="0",
                           tag="tu_system_data_tag_height_target_value",
                           parent="tu_system_data_tag_cell_height_target_value")

        # add target lock start
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_start_target_name",
                                 parent="tu_system_data_tag_row_13")
        dearpygui.add_text(default_value="Lock Start",
                           tag="tu_system_data_tag_start_target_name",
                           parent="tu_system_data_tag_cell_start_target_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_start_target_value",
                                 parent="tu_system_data_tag_row_13")
        dearpygui.add_text(default_value="00:00:00.000",
                           tag="tu_system_data_tag_start_target_value",
                           parent="tu_system_data_tag_cell_start_target_value")

        # add target lock end
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_end_target_name",
                                 parent="tu_system_data_tag_row_14")
        dearpygui.add_text(default_value="Lock End",
                           tag="tu_system_data_tag_end_target_name",
                           parent="tu_system_data_tag_cell_end_target_name")
        dearpygui.add_table_cell(tag="tu_system_data_tag_cell_end_target_value",
                                 parent="tu_system_data_tag_row_14")
        dearpygui.add_text(default_value="00:00:00.000",
                           tag="tu_system_data_tag_end_target_value",
                           parent="tu_system_data_tag_cell_end_target_value")

# create window for vehicle log
with dearpygui.window(label="tu_system_log",
                      pos=(660, 0), width=600, height=375,
                      no_title_bar=False, no_background=False, no_resize=True, no_move=True,
                      no_focus_on_appearing=True, no_bring_to_front_on_focus=True, no_scrollbar=True,
                      no_close=True, no_collapse=True):
    # create table for vehicle log
    with dearpygui.table(label="tu_system_log_table", tag="tu_system_log_tag_table",
                         header_row=True, resizable=False,
                         policy=dearpygui.mvTable_SizingStretchProp,
                         borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True):
        # add columns to vehicle log table
        dearpygui.add_table_column(label="timestamp",
                                   tag="tu_system_log_tag_timestamp",
                                   parent="tu_system_log_tag_table",
                                   width=40, width_fixed=True)
        dearpygui.add_table_column(label="severity",
                                   tag="tu_system_log_tag_severity",
                                   parent="tu_system_log_tag_table",
                                   width=40, width_fixed=True)
        dearpygui.add_table_column(label="context",
                                   tag="tu_system_log_tag_context",
                                   parent="tu_system_log_tag_table",
                                   width=40, width_fixed=True)
        dearpygui.add_table_column(label="message",
                                   tag="tu_system_log_tag_message",
                                   parent="tu_system_log_tag_table")

        # add first debug message
        log_writer("DEBUG", context="PANEL", message="Started")

# register background image texture
with dearpygui.texture_registry(show=False):
    width, height, channels, data = dearpygui.load_image("../tu_asset/image/tu_image_0.png")
    dearpygui.add_static_texture(width, height, data, tag="tu_background_image")

# create window for background image
with dearpygui.window(label="tu_background", pos=(int((1920 - 640) / 2), int((1080 - 320) / 2)),
                      no_title_bar=True, no_background=True,
                      no_resize=True, no_move=True,
                      no_focus_on_appearing=True, no_bring_to_front_on_focus=True):
    # add background image to window
    dearpygui.add_image("tu_background_image")

# setup interface
dearpygui.setup_dearpygui()

# show viewport
dearpygui.show_viewport()

# for each stream visualization request
for i, stream_name in enumerate(video_streams.keys()):
    # create stream fetch thread
    video_stream_thread = threading.Thread(target=receive_video_stream,
                                           args=(video_streams[stream_name], stream_name))

    # start stream fetch thread
    video_stream_thread.start()

    # add thread to list
    video_stream_threads.append(video_stream_thread)

    # log messages
    log_writer("DEBUG", context="PANEL", message="Started thread: " + stream_name)

# start telemetry stream thread
telemetry_stream_thread = threading.Thread(target=receive_telemetry_stream)
telemetry_stream_thread.start()

# log message
log_writer("DEBUG", context="PANEL", message="Started thread: tu_telem_stream")

# while interface is running
while dearpygui.is_dearpygui_running():

    # render the interface
    dearpygui.render_dearpygui_frame()

    # catch exit user request command
    if dearpygui.is_key_pressed(dearpygui.mvKey_Q):
        stop_threads += 1

    # user persisted to exit
    if stop_threads >= 5:
        # kill interface
        dearpygui.destroy_context()
