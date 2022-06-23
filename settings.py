# setting for competition
competition_day = 1
competition_round = 1

# settings for vehicle
vehicle_ip = "10.10.27.201"

# settings for video streaming
video_stream_test = True
video_stream_ip_remote = vehicle_ip
video_stream_ip_local = "127.0.0.1"
video_stream_port_remote = 9000
video_stream_port_local = 9000
video_stream_port_local_raw = "/dev/video10"
video_stream_port_local_judge = "/dev/video11"
video_stream_port_local_osd = "/dev/video12"
video_stream_width = 1280
video_stream_height = 720
video_stream_fps = 41
video_stream_delay = 2
video_stream_timeout = 0.2

# setting for telemetry streaming
telem_stream_ip = "127.0.0.1"
telem_stream_port_failsafe = 10010  # never use it in any custom program
telem_stream_port_control = 10020
telem_stream_port_interop = 10030

# settings for local server
rest_server_ip = "127.0.0.1"
rest_server_port = 8000
rest_server_delay = 0.1

# settings for judge server
judge_server_ip = "0.0.0.0"
judge_server_port = 5000

# settings for credentials
credential_user_id = 26
credential_user_name = "TestUcusu"
credential_user_password = "ZurnaGonnaGetYouDown"
