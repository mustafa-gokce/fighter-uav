import logger
import interop.object

# get the logger
logger = logger.Logger(name="tu_core_interop")

# log the script has started
logger.logger.info("started")

# get the competition
tu_competition = interop.tu_interop_object.Competition()

# log the competition
logger.logger.info("competition info: {0} {1}".format(tu_competition.day_name, tu_competition.round_local_name))

# get the vehicle
tu_vehicle = interop.tu_interop_object.Vehicle()

# log the vehicle connection
logger.logger.info("vehicle telemetry connection status: " + str(tu_vehicle.connected))

# connect to the vehicle
tu_vehicle.telemetry_connect(ip=tu_settings.telem_stream_ip,
                             port=tu_settings.telem_stream_port_interop)

# log the vehicle connection
logger.logger.info("vehicle telemetry connection status: " + str(tu_vehicle.connected))
