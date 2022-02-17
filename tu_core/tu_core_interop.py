import time
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

# get the judge
tu_judge = tu_interop.tu_interop_object.Judge()

# log the vehicle connection
tu_logger.logger.info("trying to connect to vehicle")

# connect to the vehicle
tu_vehicle.connect_telemetry()

# log the vehicle connection
tu_logger.logger.info("connected to vehicle")

# log the judge server connection
tu_logger.logger.info("trying to connect to judge server")

# connect to the judge server
tu_judge.connect_server(vehicle=tu_vehicle)

# log the judge server connection
tu_logger.logger.info("connected to judge server")

# vehicle core event loop
while True:

    # debug the vehicle
    print(tu_vehicle.location.__dict__())

    # vehicle core event loop cooldown delay
    time.sleep(1)
