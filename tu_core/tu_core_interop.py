import os
import signal
import time
import pprint
import tu_log.tu_log_object
import tu_interop.tu_interop_object

# get the logger
tu_logger = tu_log.tu_log_object.Logger(name="tu_core_interop")

# log the script has started
tu_logger.logger.info("started")

# get the competition
tu_competition = tu_interop.tu_interop_object.Competition()

# log the competition
tu_logger.logger.info("competition info: {0} {1}".format(tu_competition.day_name, tu_competition.round_local_name))

# get the vehicle
tu_vehicle = tu_interop.tu_interop_object.Vehicle()

# log the vehicle connection
tu_logger.logger.info("vehicle telemetry connection status: " + str(tu_vehicle.connected))

# connect to the vehicle
tu_vehicle.telemetry_connect()

# log the vehicle connection
tu_logger.logger.info("vehicle telemetry connection status: " + str(tu_vehicle.connected))

# log the judge server connection
tu_logger.logger.info("judge server login status: " + str(tu_vehicle.judge.logged_in))

# connect to the judge server
tu_vehicle.server_login()

# log the judge server connection
tu_logger.logger.info("judge server login status: " + str(tu_vehicle.judge.logged_in))

time.sleep(5)
pprint.pprint(tu_vehicle.__dict__())

# disconnect to the judge server
tu_vehicle.server_logout()

# log the judge server connection
tu_logger.logger.info("judge server login status: " + str(tu_vehicle.judge.logged_in))

# forcefully kill the threads and exit
os.kill(os.getpid(), signal.SIGTERM)
