from pymavlink import mavutil
master = mavutil.mavlink_connection("/dev/ttyACM0", baud=115200)
