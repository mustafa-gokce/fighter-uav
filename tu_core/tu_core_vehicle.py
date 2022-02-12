import time
import tu_interop.tu_interop_object

# get the vehicle
tu_vehicle = tu_interop.tu_interop_object.Vehicle()

# connect to the vehicle
tu_vehicle.connect_telemetry()

while True:
    time.sleep(1)
