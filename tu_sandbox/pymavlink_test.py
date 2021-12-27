from pymavlink import mavutil
master = mavutil.mavlink_connection("/dev/ttyACM0", baud=115200)
from pymavlink.dialects.v20 import all as mavlink2
mavlink2.MAVLink_statustext_message(mavlink2.MAV_SEVERITY_INFO, "HELLO")
mavlink2.MAVLink_mission_set_current_message()
