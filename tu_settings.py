# setting for competition
tu_competition_day = 1
tu_competition_round = 1

# settings for vehicle
tu_vehicle_ip = "10.10.27.201"

# settings for video streaming
tu_video_stream_test = True
tu_video_stream_ip_remote = tu_vehicle_ip
tu_video_stream_ip_local = "127.0.0.1"
tu_video_stream_port_remote = 9000
tu_video_stream_port_local = 9000
tu_video_stream_port_local_raw = "/dev/video10"
tu_video_stream_port_local_judge = "/dev/video11"
tu_video_stream_port_local_osd = "/dev/video12"
tu_video_stream_width = 1280
tu_video_stream_height = 720
tu_video_stream_fps = 41
tu_video_stream_delay = 2
tu_video_stream_timeout = 0.2

# setting for telemetry streaming
tu_telem_stream_ip = "127.0.0.1"
tu_telem_stream_port_failsafe = 10010  # never use it in any custom program
tu_telem_stream_port_control = 10020
tu_telem_stream_port_interop = 10030

# settings for local server
tu_core_server_ip = "127.0.0.1"
tu_core_server_port = 8000

# settings for judge server
tu_judge_server_ip = "0.0.0.0"
tu_judge_server_port = 5000

# settings for credentials
tu_credential_user_id = 26
tu_credential_user_name = "TestUcusu"
tu_credential_user_password = "ZurnaGonnaGetYouDown"
