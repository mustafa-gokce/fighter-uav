import time
import math
import threading
import datetime
import subprocess
import logging
import requests
import settings
import compat

# silence the requests library
urllib3_logger = logging.getLogger("urllib3")
urllib3_logger.setLevel(logging.CRITICAL)


class DevOps:
    """
    devops class
    """

    def __init__(self):
        self.__git_hash_long = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("ascii").strip()
        self.__git_hash_short = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("ascii").strip()

    @property
    def git_hash_long(self):
        """
        get git hash long

        :return: str
        """

        # return to long hash
        return self.__git_hash_long

    @property
    def git_hash_short(self):
        """
        get git hash short

        :return: str
        """

        # return to short has
        return self.__git_hash_short


class Competition:
    """
    competition class
    """

    def __init__(self):
        self.__day = settings.competition_day
        self.__round = settings.competition_round

    @property
    def day(self):
        """
        get competition day

        :return: int
        """

        # return to competition day
        return self.__day

    @property
    def day_name(self):
        """
        get competition day name

        :return: str
        """

        # return to competition day name
        return "day {0}".format(self.day)

    @property
    def round_local(self):
        """
        get local round

        :return: int
        """

        # return to local round
        return self.__round

    @property
    def round_local_name(self):
        """
        get local round name

        :return: str
        """

        # return to local round name
        return "round {0}".format(self.round_local)

    @property
    def round_global(self):
        """
        get global round

        :return: int
        """

        # return to global round
        return (self.day - 1) * 2 + self.round_local

    @property
    def round_global_name(self):
        """
        get global round name

        :return: str
        """

        # return to global round name
        return "round {0}".format(self.round_global)

    def __dict__(self):
        """
        devops class dictionary

        :return: dict
        """

        # return to devops dictionary
        return {"day": self.day,
                "day_name": self.day_name,
                "round_local": self.round_local,
                "round_local_name": self.round_local_name,
                "round_global": self.round_global,
                "round_global_name": self.round_global_name}

    def __str__(self):
        """
        devops class dictionary string

        :return: dict
        """

        # return to devops dictionary string
        return str(self.__dict__())


class Time:
    """
    time class
    """

    def __init__(self):
        self.__hour = 0
        self.__minute = 0
        self.__second = 0
        self.__millisecond = 0

    @property
    def hour(self):
        """
        get hour

        :return: int
        """

        # expose hour attribute
        return self.__hour

    @property
    def minute(self):
        """
        get minute

        :return: int
        """

        # expose minute attribute
        return self.__minute

    @property
    def second(self):
        """
        get second

        :return: int
        """

        # expose second attribute
        return self.__second

    @property
    def millisecond(self):
        """
        get millisecond

        :return: int
        """

        # expose millisecond attribute
        return self.__millisecond

    @hour.setter
    def hour(self, hour: int):
        """
        set hour

        :param hour: int
        :return: None
        """

        # hour can be int or float
        if type(hour) not in (int, float):
            raise TypeError

        # hour should be a reasonable number
        if not 0 <= hour < 24:
            raise ValueError

        # set hour attribute
        self.__hour = int(hour)

    @minute.setter
    def minute(self, minute: int):
        """
        set minute

        :param minute: int
        :return: None
        """

        # minute can be int or float
        if type(minute) not in (int, float):
            raise TypeError

        # minute should be a reasonable number
        if not 0 <= minute < 60:
            raise ValueError

        # set minute attribute
        self.__minute = int(minute)

    @second.setter
    def second(self, second: int):
        """
        set second

        :param second: int
        :return: None
        """

        # second can be int or float
        if type(second) not in (int, float):
            raise TypeError

        # second should be a reasonable number
        if not 0 <= second < 60:
            raise ValueError

        # set second attribute
        self.__second = int(second)

    @millisecond.setter
    def millisecond(self, millisecond: int):
        """
        set millisecond

        :param millisecond: int
        :return: None
        """

        # millisecond can be int or float
        if type(millisecond) not in (int, float):
            raise TypeError

        # millisecond should be a reasonable number
        if not 0 <= millisecond < 1000:
            raise ValueError

        # set second attribute
        self.__millisecond = int(millisecond)

    def __dict__(self):
        """
        time class dictionary

        :return: dict
        """

        # get time class as dictionary
        return {"hour": self.hour,
                "minute": self.minute,
                "second": self.second,
                "millisecond": self.millisecond}

    def __str__(self):
        """
        time class dictionary as string

        :return: str
        """

        # get time class dictionary as string
        return str(self.__dict__())


class Location:
    """
    location class
    """

    def __init__(self):
        self.__latitude = 0.0
        self.__longitude = 0.0
        self.__altitude = 0.0

    @property
    def latitude(self):
        """
        get latitude

        :return: float
        """

        # expose latitude attribute
        return self.__latitude

    @property
    def longitude(self):
        """
        get longitude

        :return: float
        """

        # expose longitude attribute
        return self.__longitude

    @property
    def altitude(self):
        """
        get altitude

        :return: float
        """

        # expose altitude attribute
        return self.__altitude

    @latitude.setter
    def latitude(self, latitude: float):
        """
        set latitude

        :param latitude: float
        :return: None
        """

        # latitude can be int or float
        if type(latitude) not in (int, float):
            raise TypeError

        # latitude should be a reasonable number
        if not -90.0 <= latitude <= 90.0:
            raise ValueError

        # set latitude attribute
        self.__latitude = float(latitude)

    @longitude.setter
    def longitude(self, longitude: float):
        """
        set longitude

        :param longitude: float
        :return: None
        """

        # longitude can be int or float
        if type(longitude) not in (int, float):
            raise TypeError

        # longitude should be a reasonable number
        if not -180.0 <= longitude <= 180.0:
            raise ValueError

        # set longitude attribute
        self.__longitude = float(longitude)

    @altitude.setter
    def altitude(self, altitude: float):
        """
        set altitude

        :param altitude: float
        :return: None
        """

        # altitude can be int or float
        if type(altitude) not in (int, float):
            raise TypeError

        # set altitude attribute
        self.__altitude = float(altitude)

    def __dict__(self):
        """
        location class dictionary

        :return: dict
        """

        # get location class as dictionary
        return {"latitude": self.latitude,
                "longitude": self.longitude,
                "altitude": self.altitude}

    def __str__(self):
        """
        location class dictionary as string

        :return: str
        """

        # get location class dictionary as string
        return str(self.__dict__())


class Attitude:
    """
    attitude class
    """

    def __init__(self):
        self.__roll = 0.0
        self.__pitch = 0.0
        self.__heading = 0.0

    @property
    def roll(self):
        """
        get roll angle

        :return: float
        """

        # expose roll angle attribute
        return self.__roll

    @property
    def pitch(self):
        """
        get pitch angle

        :return: float
        """

        # expose pitch angle attribute
        return self.__pitch

    @property
    def heading(self):
        """
        get heading

        :return: float
        """

        # expose heading attribute
        return self.__heading

    @roll.setter
    def roll(self, roll: float):
        """
        set roll angle

        :param roll: float
        :return: None
        """

        # roll can be int or float
        if type(roll) not in (int, float):
            raise TypeError

        # roll should be a reasonable number
        if not -180.0 <= roll <= 180.0:
            raise ValueError

        # set roll attribute
        self.__roll = float(roll)

    @pitch.setter
    def pitch(self, pitch: float):
        """
        set pitch angle

        :param pitch: float
        :return: None
        """

        # pitch can be int or float
        if type(pitch) not in (int, float):
            raise TypeError

        # pitch should be a reasonable number
        if not -180.0 <= pitch <= 180.0:
            raise ValueError

        # set pitch attribute
        self.__pitch = float(pitch)

    @heading.setter
    def heading(self, heading: float):
        """
        set heading angle

        :param heading: float
        :return: None
        """

        # heading can be int or float
        if type(heading) not in (int, float):
            raise TypeError

        # heading should be a reasonable number
        if not 0.0 <= heading <= 360.0:
            raise ValueError

        # set heading attribute
        self.__heading = float(heading)

    def __dict__(self):
        """
        attitude class dictionary

        :return: dict
        """

        # get attitude class as dictionary
        return {"roll": self.roll,
                "pitch": self.pitch,
                "heading": self.heading}

    def __str__(self):
        """
        attitude class dictionary as string

        :return: str
        """

        # get attitude class dictionary as string
        return str(self.__dict__())


class Target:
    """
    target class
    """

    def __init__(self):
        self.time_start = Time()
        self.time_end = Time()
        self.__lock = 0
        self.__x = 0
        self.__y = 0
        self.__width = 0
        self.__height = 0

    @property
    def lock(self):
        """
        get target is locked or not

        :return: int
        """

        # expose target is locked attribute
        return self.__lock

    @property
    def x(self):
        """
        get target upper left pixel x value on image frame

        :return: int
        """

        # expose target upper left pixel x value on image frame
        return self.__x

    @property
    def y(self):
        """
        get target upper left pixel y value on image frame

        :return: int
        """

        # expose target upper left pixel y value on image frame
        return self.__y

    @property
    def width(self):
        """
        get target width on image frame

        :return: int
        """

        # expose target width on image frame
        return self.__width

    @property
    def height(self):
        """
        get target height on image frame

        :return: int
        """

        # expose target height on image frame
        return self.__height

    @lock.setter
    def lock(self, lock: int):
        """
        set target is locked or not

        :param lock: int
        :return: None
        """

        # lock can be int
        if type(lock) != int:
            raise TypeError

        # lock should be a reasonable number
        if lock not in (0, 1):
            raise ValueError

        # set lock attribute
        self.__lock = lock

    @x.setter
    def x(self, x: int):
        """
        set target upper left pixel x value on image frame

        :param x: int
        :return: None
        """

        # x can be int
        if type(x) != int:
            raise TypeError

        # x should be a reasonable number
        if not 0 <= x < settings.video_stream_width:
            raise ValueError

        # set x attribute
        self.__x = x

    @y.setter
    def y(self, y: int):
        """
        set target upper left pixel y value on image frame

        :param y: int
        :return: None
        """

        # y can be int
        if type(y) != int:
            raise TypeError

        # y should be a reasonable number
        if not 0 <= y < settings.video_stream_height:
            raise ValueError

        # set y attribute
        self.__y = y

    @width.setter
    def width(self, width: int):
        """
        set target width value on image frame

        :param width: int
        :return: None
        """

        # width can be int
        if type(width) != int:
            raise TypeError

        # width should be a reasonable number
        if not 0 <= width < settings.video_stream_width:
            raise ValueError

        # set width attribute
        self.__width = width

    @height.setter
    def height(self, height: int):
        """
        set target height value on image frame

        :param height: int
        :return: None
        """

        # height can be int
        if type(height) != int:
            raise TypeError

        # height should be a reasonable number
        if not 0 <= height < settings.video_stream_height:
            raise ValueError

        # set height attribute
        self.__height = height

    def __dict__(self):
        """
        target class dictionary

        :return: dict
        """

        # get target class as dictionary
        return {"time_start": self.time_start.__dict__(),
                "time_end": self.time_end.__dict__(),
                "lock": self.lock,
                "x": self.x,
                "y": self.y,
                "width": self.width,
                "height": self.height}

    def __str__(self):
        """
        target class dictionary as string

        :return: dict
        """

        # get target class dictionary as string
        return str(self.__dict__())


class Credential:
    """
    credential class
    """

    def __init__(self, user_name=settings.credential_user_name,
                 user_password=settings.credential_user_password):
        self.__user_name = user_name
        self.__user_password = user_password

    @property
    def user_name(self):
        """
        get user name

        :return: str
        """

        # expose user name attribute
        return self.__user_name

    @property
    def user_password(self):
        """
        get user password

        :return: str
        """

        # expose user password attribute
        return self.__user_password

    @user_name.setter
    def user_name(self, user_name: str):
        """
        set user name

        :param user_name: str
        :return: None
        """

        # user name can be string
        if type(user_name) != str:
            raise TypeError

        # user name can not be empty
        if user_name == "":
            raise ValueError

        # set user name attribute
        self.__user_name = user_name

    @user_password.setter
    def user_password(self, user_password: str):
        """
        set user password

        :param user_password: str
        :return: None
        """

        # user password can be string
        if type(user_password) != str:
            raise TypeError

        # user password can not be empty
        if user_password == "":
            raise ValueError

        # set user password attribute
        self.__user_password = user_password

    @property
    def dict_credential_judge(self):
        """
        get credential as a dictionary formatted for judge server connection

        :return: dict
        """

        # get credential as a dictionary formatted for judge server connection
        return {compat.login["user_name"]["locale"]: self.user_name,
                compat.login["user_password"]["locale"]: self.user_password}

    def __dict__(self):
        """
        get credential class dictionary

        :return: dict
        """

        # get credential class as dictionary
        return {"user_name": self.user_name,
                "user_password": self.user_password}

    def __str__(self):
        """
        get credential class dictionary as string

        :return: dict
        """

        # get credential class dictionary as string
        return str(self.__dict__())


class BaseVehicle:
    """
    base vehicle class
    """

    def __init__(self):
        self.time = Time()
        self.location = Location()
        self.attitude = Attitude()
        self.__team = 0

    @property
    def team(self):
        """
        get team number of the vehicle

        :return: int
        """

        # expose team number of the vehicle
        return self.__team

    @team.setter
    def team(self, team: int):
        """
        set team number of the vehicle

        :param team: int
        :return: None
        """

        # team number can be integer
        if type(team) != int:
            raise TypeError

        # team number should be a reasonable number
        if team < 0:
            raise ValueError

        # set team number attribute
        self.__team = team

    def __dict__(self):
        """
        get team number as dictionary

        :return: dict
        """

        # get team number as dictionary
        return {"time": self.time.__dict__(),
                "location": self.location.__dict__(),
                "attitude": self.attitude.__dict__(),
                "team": self.team}

    def __str__(self):
        """
        get team number dictionary as string

        :return: dict
        """

        # get team number as dictionary
        return str(self.__dict__())


class Foe(BaseVehicle):
    """
    foe vehicle class
    """

    def __init__(self):
        super().__init__()


class Judge:
    """
    judge class
    """

    def __init__(self):
        self.credential = Credential()
        self._time = Time()
        self._path_login = compat.path_server_login
        self._path_logout = compat.path_server_logout
        self._path_time = compat.path_server_time
        self._path_send = compat.path_server_send
        self._path_lock = compat.path_server_lock
        self._logged_in = False
        self._interop_enabled = False
        self._foes = []
        self._server_connection = None
        self._server_connection_thread = None

    @property
    def time(self):
        """
        get judge server time object

        :return: Time()
        """

        # expose judge server time object attribute
        return self._time

    @property
    def path_login(self):
        """
        get judge server login path

        :return: str
        """

        # expose judge server login path
        return self._path_login

    @property
    def path_logout(self):
        """
        get judge server logout path

        :return: str
        """

        # expose judge server logout path
        return self._path_logout

    @property
    def path_time(self):
        """
        get judge server time path

        :return: str
        """

        # expose judge server time path
        return self._path_time

    @property
    def path_send(self):
        """
        get judge server telemetry dealing path

        :return: str
        """

        # expose judge server telemetry dealing path
        return self._path_send

    @property
    def path_lock(self):
        """
        get judge server target lock dealing path

        :return: str
        """

        # expose judge server target lock dealing path
        return self._path_lock

    @property
    def logged_in(self):
        """
        get logged in to judge server or not

        :return: bool
        """

        # expose logged in to judge server or not
        return self._logged_in

    @property
    def interop_enabled(self):
        """
        get enabled to deal telemetry with judge server

        :return: bool
        """

        # expose enabled to deal telemetry with judge server
        return self._interop_enabled

    @property
    def foes(self):
        """
        list of incoming foe data from judge server

        :return: list
        """

        # expose incoming foe data from judge server
        return self._foes

    def interop_enable(self):
        """
        enable to communicate with judge server

        :return: None
        """

        # enable to communicate with judge server
        self._interop_enabled = True

    def interop_disable(self):
        """
        disable to communicate with judge server

        :return: None
        """

        # disable to communicate with judge server
        self._interop_enabled = False

    def server_login(self, blocking=True):
        """
        login to judge server

        :param blocking: bool
        :return: None
        """

        # check if interop is enabled
        if self.interop_enabled:

            # while not logged in to judge server
            while not self.logged_in:

                # if there is no connection
                if self._server_connection is None:
                    # create a session
                    self._server_connection = requests.Session()

                # try to log in to the judge server
                try:

                    # request to log in to judge server
                    login_response = self._server_connection.post(url=self.path_login,
                                                                  headers={"Content-Type": "application/json"},
                                                                  json=self.credential.dict_credential_judge)

                    # check login request status
                    if login_response.status_code == 200:
                        self._logged_in = True

                # catch all exceptions
                except Exception as e:
                    pass

                # break the loop if not requested blocking
                if not blocking:
                    break

                # cool down the process
                time.sleep(0.1)

    def server_logout(self, blocking=True):
        """
        logout from judge server

        :param blocking: bool
        :return: None
        """
        # check if interop is enabled
        if self.interop_enabled:

            # while still logged in to judge server
            while self.logged_in:

                # try to log out from the judge server
                try:

                    # request to log out from judge server
                    logout_response = self._server_connection.get(url=self.path_logout)

                    # check logout request status
                    if logout_response.status_code == 200:
                        self._logged_in = False

                # catch all exceptions
                except Exception as e:
                    pass

                # break the loop if not requested blocking
                if not blocking:
                    break

                # cool down the process
                time.sleep(0.1)

    def server_time_get(self):
        """
        get server time

        :return: None
        """
        # check if interop is enabled
        if self.interop_enabled:

            # check login status
            if self.logged_in:

                # try to get server time from the judge server
                try:

                    # request system time from judge server
                    server_time_response = self._server_connection.get(url=self.path_time)

                    # parse the request system time response
                    server_time_response = server_time_response.json()

                    # update time attributes
                    self.time.hour = int(server_time_response[compat.time["hour"]["locale"]])
                    self.time.minute = int(server_time_response[compat.time["minute"]["locale"]])
                    self.time.second = int(server_time_response[compat.time["second"]["locale"]])
                    self.time.millisecond = int(server_time_response[compat.time["millisecond"]["locale"]])

                # catch all exceptions
                except Exception as e:
                    pass

    def __dict__(self):
        """
        get judge object as dictionary

        :return: dict
        """

        # get judge object as dictionary
        return {"time": self.time.__dict__(),
                # "credential": self.credential.__dict__(),
                # "path_login": self.path_login,
                # "path_logout": self.path_logout,
                # "path_time": self.path_time,
                # "path_send": self.path_send,
                # "path_lock": self.path_lock,
                "logged_in": self.logged_in,
                "interop_enabled": self.interop_enabled,
                "foes": [foe.__dict__() for foe in self.foes]}

    def __str__(self):
        """
        get judge object dictionary as string

        :return: str
        """

        # get judge object dictionary as string
        return str(self.__dict__())


class Vehicle(BaseVehicle):
    """
    vehicle class
    """

    def __init__(self):
        super().__init__()
        self._target = Target()
        self.judge = Judge()
        self._competition = Competition()
        self._foe = Foe()
        self._team = settings.credential_user_id
        self._connected = False
        self._speed = 0.0
        self._battery = 0.0
        self._auto = 0
        self._flight_mode = "UNKNOWN"
        self._armed = False
        self._thread_telemetry_get = threading.Thread(target=self._telemetry_get).start()

    @property
    def speed(self):
        """
        get ground speed of the vehicle

        :return: float
        """

        # expose ground speed of the vehicle
        return self._speed

    @property
    def battery(self):
        """
        get battery level of the vehicle

        :return: float
        """

        # expose battery level of the vehicle
        return self._battery

    @property
    def auto(self):
        """
        get vehicle is flying in auto mode or not

        :return: int
        """

        # expose vehicle is flying in auto mode or not
        return 1 if self.flight_mode in ("GUIDED", "AUTO") else 0

    @property
    def flight_mode(self):
        """
        get vehicle flight mode

        :return: str
        """

        # expose vehicle flight mode
        return self._flight_mode

    @property
    def armed(self):
        """
        get vehicle arm status

        :return: bool
        """

        # expose vehicle arm status
        return self._armed

    @property
    def connected(self):
        """
        get connected to vehicle or not

        :return: bool
        """

        # expose connected to vehicle or not
        return self._connected

    @property
    def dict_judge_telemetry(self):
        """
        get telemetry data ready for sending to the judge server

        :return: dict
        """

        # expose telemetry data ready for sending to the judge server
        return {compat.send["team"]["locale"]: self._team,
                compat.send["latitude"]["locale"]: self.location.latitude,
                compat.send["longitude"]["locale"]: self.location.longitude,
                compat.send["altitude"]["locale"]: self.location.altitude,
                compat.send["roll"]["locale"]: self.attitude.roll,
                compat.send["pitch"]["locale"]: self.attitude.pitch,
                compat.send["heading"]["locale"]: self.attitude.heading,
                compat.send["speed"]["locale"]: self.speed,
                compat.send["battery"]["locale"]: self.battery,
                compat.send["auto"]["locale"]: self.auto,
                compat.send["target_lock"]["locale"]: self._target.lock,
                compat.send["target_x"]["locale"]: self._target.x,
                compat.send["target_y"]["locale"]: self._target.y,
                compat.send["target_width"]["locale"]: self._target.width,
                compat.send["target_height"]["locale"]: self._target.height,
                compat.send["time"]["locale"]: {
                    compat.time["hour"]["locale"]: self.time.hour,
                    compat.time["minute"]["locale"]: self.time.minute,
                    compat.time["second"]["locale"]: self.time.second,
                    compat.time["millisecond"]["locale"]: self.time.millisecond}}

    @property
    def dict_judge_lock(self):
        """
        get target lock data ready for sending to the judge server

        :return: dict
        """

        # expose target lock data ready for sending to the judge server
        return {compat.lock["lock_auto"]["locale"]: self.auto,
                compat.lock["lock_start"]["locale"]: {
                    compat.time["hour"]["locale"]: self._target.time_start.hour,
                    compat.time["minute"]["locale"]: self._target.time_start.minute,
                    compat.time["second"]["locale"]: self._target.time_start.second,
                    compat.time["millisecond"]["locale"]: self._target.time_start.millisecond},
                compat.lock["lock_end"]["locale"]: {
                    compat.time["hour"]["locale"]: self._target.time_end.hour,
                    compat.time["minute"]["locale"]: self._target.time_end.minute,
                    compat.time["second"]["locale"]: self._target.time_end.second,
                    compat.time["millisecond"]["locale"]: self._target.time_end.millisecond}}

    def __dict__(self):
        """
        get vehicle class as dictionary

        :return: dict
        """

        # expose vehicle class as dictionary
        return {"connected": self.connected,
                "time": self.time.__dict__(),
                "location": self.location.__dict__(),
                "attitude": self.attitude.__dict__(),
                "target": self._target.__dict__(),
                "judge": self.judge.__dict__(),
                "competition": self._competition.__dict__(),
                "foe": self._foe.__dict__(),
                "team": self._team,
                "speed": self.speed,
                "battery": self.battery,
                "auto": self.auto,
                "flight_mode": self.flight_mode,
                "armed": self.armed}

    def __str__(self):
        """
        get vehicle class dictionary as string

        :return: str
        """

        # expose vehicle class dictionary as string
        return str(self.__dict__())

    def wait_ready(self):
        """
        wait the vehicle to be connected
        """

        # while not connect to the vehicle
        while not self.connected:
            # wait the vehicle to be connected
            time.sleep(0.1)

    # telemetry receiver thread method
    def _telemetry_get(self):

        # flight mode declarations
        flight_mode_names = list(compat.mode_mapping.keys())
        flight_mode_numbers = list(compat.mode_mapping.values())

        # create a session for telemetry get
        connection = requests.Session()

        # create connection url
        url = "http://{0}:{1}/get/all".format(settings.rest_server_ip,
                                              settings.rest_server_port)

        # do below always
        while True:

            # just to cool down
            time.sleep(settings.rest_server_delay)

            # try to receive vehicle state
            try:
                vehicle_state = connection.get(url=url).json()
            except requests.exceptions.ConnectionError:
                vehicle_state = {}

            # not received a message
            if not vehicle_state:
                self._connected = False
                continue
            self._connected = True

            # get vehicle state keys for field checking
            vehicle_state_keys = vehicle_state.keys()

            # get latitude, longitude, relative altitude and heading of the vehicle
            if "GLOBAL_POSITION_INT" in vehicle_state_keys:
                self.location.latitude = vehicle_state["GLOBAL_POSITION_INT"]["lat"] * 1e-7
                self.location.longitude = vehicle_state["GLOBAL_POSITION_INT"]["lon"] * 1e-7
                self.location.altitude = vehicle_state["GLOBAL_POSITION_INT"]["relative_alt"] * 1e-3
                self.attitude.heading = vehicle_state["GLOBAL_POSITION_INT"]["hdg"] * 1e-2

            # get roll and pitch of the vehicle
            if "ATTITUDE" in vehicle_state_keys:
                self.attitude.roll = math.degrees(vehicle_state["ATTITUDE"]["roll"])
                self.attitude.pitch = math.degrees(vehicle_state["ATTITUDE"]["pitch"])

            # get ground speed of the vehicle
            if "VFR_HUD" in vehicle_state_keys:
                self._speed = vehicle_state["VFR_HUD"]["groundspeed"]

            # get remaining battery percent of the vehicle
            if "SYS_STATUS" in vehicle_state_keys:
                self._battery = vehicle_state["SYS_STATUS"]["battery_remaining"]

            # get system time of the vehicle
            if "SYSTEM_TIME" in vehicle_state_keys:
                unix_time = vehicle_state["SYSTEM_TIME"]["time_unix_usec"]
                unix_time = datetime.datetime.utcfromtimestamp(unix_time * 1e-6)
                self.time.hour = unix_time.hour
                self.time.minute = unix_time.minute
                self.time.second = unix_time.second
                self.time.millisecond = int(unix_time.microsecond * 1e-3)

            # get heartbeat of the vehicle
            if "HEARTBEAT" in vehicle_state_keys:
                # get flight mode of the vehicle
                custom_mode = vehicle_state["HEARTBEAT"]["custom_mode"]
                custom_mode_index = flight_mode_numbers.index(custom_mode)
                self._flight_mode = flight_mode_names[custom_mode_index]

                # get arm status
                base_mode = vehicle_state["HEARTBEAT"]["base_mode"]
                armed_bit = base_mode & 128
                arm_status = armed_bit == 128
                self._armed = arm_status
