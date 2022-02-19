import math
import threading
import datetime
import subprocess
import logging
import requests
import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect
import tu_settings
import tu_interop.tu_interop_compat as tu_interop_compat


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
        self.__day = tu_settings.tu_competition_day
        self.__round = tu_settings.tu_competition_round

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
        if not 0 <= x < tu_settings.tu_video_stream_width:
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
        if not 0 <= y < tu_settings.tu_video_stream_height:
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
        if not 0 <= width < tu_settings.tu_video_stream_width:
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
        if not 0 <= height < tu_settings.tu_video_stream_height:
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

    def __init__(self, user_name=tu_settings.tu_credential_user_name,
                 user_password=tu_settings.tu_credential_user_password):
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
        return {tu_interop_compat.tu_interop_compat_login["user_name"]["locale"]: self.user_name,
                tu_interop_compat.tu_interop_compat_login["user_password"]["locale"]: self.user_password}

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
        self.__time = Time()
        self.__path_login = tu_interop_compat.tu_interop_compat_path_server_login
        self.__path_logout = tu_interop_compat.tu_interop_compat_path_server_logout
        self.__path_time = tu_interop_compat.tu_interop_compat_path_server_time
        self.__path_send = tu_interop_compat.tu_interop_compat_path_server_send
        self.__path_lock = tu_interop_compat.tu_interop_compat_path_server_lock
        self.__logged_in = False
        self.__allowed_interop = False
        self.__foes = []
        self.__server_connection = None
        self.__server_connection_thread = None

    @property
    def time(self):
        """
        get judge server time object

        :return: Time()
        """

        # expose judge server time object attribute
        return self.__time

    @property
    def path_login(self):
        """
        get judge server login path

        :return: str
        """

        # expose judge server login path
        return self.__path_login

    @property
    def path_logout(self):
        """
        get judge server logout path

        :return: str
        """

        # expose judge server logout path
        return self.__path_logout

    @property
    def path_time(self):
        """
        get judge server time path

        :return: str
        """

        # expose judge server time path
        return self.__path_time

    @property
    def path_send(self):
        """
        get judge server telemetry dealing path

        :return: str
        """

        # expose judge server telemetry dealing path
        return self.__path_send

    @property
    def path_lock(self):
        """
        get judge server target lock dealing path

        :return: str
        """

        # expose judge server target lock dealing path
        return self.__path_lock

    @property
    def logged_in(self):
        """
        get logged in to judge server or not

        :return: bool
        """

        # expose logged in to judge server or not
        return self.__logged_in

    @property
    def allowed_interop(self):
        """
        get enabled to deal telemetry with judge server

        :return: bool
        """

        # expose enabled to deal telemetry with judge server
        return self.__allowed_interop

    @property
    def foes(self):
        """
        list of incoming foe data from judge server

        :return: list
        """

        # expose incoming foe data from judge server
        return self.__foes

    def server_login(self, blocking=True):
        """
        login to judge server

        :param blocking: bool
        :return: None
        """

        # while not logged in to judge server
        while not self.logged_in:

            # if there is no connection
            if self.__server_connection is None:

                # silence the requests library
                urllib3_logger = logging.getLogger("urllib3")
                urllib3_logger.setLevel(logging.CRITICAL)

                # create a session
                self.__server_connection = requests.Session()

            # request to log in to judge server
            login_response = self.__server_connection.post(url=self.path_login,
                                                           headers={"Content-Type": "application/json"},
                                                           json=self.credential.dict_credential_judge)

            # parse the login response
            login_response = login_response.json()

            # check login request status
            if login_response.get("result", "failure") == "success":
                self.__logged_in = True

            # break the loop if not requested blocking
            if not blocking:
                break

    def server_logout(self, blocking=True):
        """
        logout from judge server

        :param blocking: bool
        :return: None
        """

        # while still logged in to judge server
        while self.logged_in:

            # request to log out from judge server
            logout_response = self.__server_connection.get(url=self.path_logout)

            # parse the logout response
            logout_response = logout_response.json()

            # check logout request status
            if logout_response.get("result", "failure") == "success":
                self.__logged_in = False

            # break the loop if not requested blocking
            if not blocking:
                break

    def server_time_get(self):
        """
        get server time

        :return: None
        """

        # check login status
        if self.logged_in:

            # request system time from judge server
            server_time_response = self.__server_connection.get(url=self.path_time)

            # parse the request system time response
            server_time_response = server_time_response.json()

            # update time attributes
            self.time.hour = int(server_time_response[tu_interop_compat.tu_interop_compat_time["hour"]["locale"]])
            self.time.minute = int(server_time_response[tu_interop_compat.tu_interop_compat_time["minute"]["locale"]])
            self.time.second = int(server_time_response[tu_interop_compat.tu_interop_compat_time["second"]["locale"]])
            self.time.millisecond = int(
                server_time_response[tu_interop_compat.tu_interop_compat_time["millisecond"]["locale"]])

    def __dict__(self):
        """
        get judge object as dictionary

        :return: dict
        """

        # get judge object as dictionary
        return {"time": self.time.__dict__(),
                "credential": self.credential.__dict__(),
                "path_login": self.path_login,
                "path_logout": self.path_logout,
                "path_time": self.path_time,
                "path_send": self.path_send,
                "path_lock": self.path_lock,
                "logged_in": self.logged_in,
                "allowed_interop": self.allowed_interop,
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
        self.target = Target()
        self.judge = Judge()
        self.competition = Competition()
        self.foe = Foe()
        self.team = tu_settings.tu_credential_user_id
        self.__connected = False
        self.__speed = 0.0
        self.__battery = 0.0
        self.__auto = 0
        self.__mavlink = None
        self.__thread_telemetry_get = None

    @property
    def speed(self):
        """
        get ground speed of the vehicle

        :return: float
        """

        # expose ground speed of the vehicle
        return self.__speed

    @property
    def battery(self):
        """
        get battery level of the vehicle

        :return: float
        """

        # expose battery level of the vehicle
        return self.__battery

    @property
    def auto(self):
        """
        get vehicle is flying in auto mode or not

        :return: int
        """

        # expose vehicle is flying in auto mode or not
        return self.__auto

    @property
    def connected(self):
        """
        get connected to vehicle or not

        :return: bool
        """

        # expose connected to vehicle or not
        return self.__connected

    @property
    def __dict_judge_telemetry(self):
        """
        get telemetry data ready for sending to the judge server

        :return: dict
        """

        # expose telemetry data ready for sending to the judge server
        return {tu_interop_compat.tu_interop_compat_send["team"]["locale"]: self.team,
                tu_interop_compat.tu_interop_compat_send["latitude"]["locale"]: self.location.latitude,
                tu_interop_compat.tu_interop_compat_send["longitude"]["locale"]: self.location.longitude,
                tu_interop_compat.tu_interop_compat_send["altitude"]["locale"]: self.location.altitude,
                tu_interop_compat.tu_interop_compat_send["roll"]["locale"]: self.attitude.roll,
                tu_interop_compat.tu_interop_compat_send["pitch"]["locale"]: self.attitude.pitch,
                tu_interop_compat.tu_interop_compat_send["heading"]["locale"]: self.attitude.heading,
                tu_interop_compat.tu_interop_compat_send["speed"]["locale"]: self.speed,
                tu_interop_compat.tu_interop_compat_send["battery"]["locale"]: self.battery,
                tu_interop_compat.tu_interop_compat_send["auto"]["locale"]: self.auto,
                tu_interop_compat.tu_interop_compat_send["target_lock"]["locale"]: self.target.lock,
                tu_interop_compat.tu_interop_compat_send["target_x"]["locale"]: self.target.x,
                tu_interop_compat.tu_interop_compat_send["target_y"]["locale"]: self.target.y,
                tu_interop_compat.tu_interop_compat_send["target_width"]["locale"]: self.target.width,
                tu_interop_compat.tu_interop_compat_send["target_height"]["locale"]: self.target.height,
                tu_interop_compat.tu_interop_compat_send["time"]["locale"]: {
                    tu_interop_compat.tu_interop_compat_time["hour"]["locale"]: self.time.hour,
                    tu_interop_compat.tu_interop_compat_time["minute"]["locale"]: self.time.minute,
                    tu_interop_compat.tu_interop_compat_time["second"]["locale"]: self.time.second,
                    tu_interop_compat.tu_interop_compat_time["millisecond"]["locale"]: self.time.millisecond}}

    @property
    def __dict_judge_lock(self):
        """
        get target lock data ready for sending to the judge server

        :return: dict
        """

        # expose target lock data ready for sending to the judge server
        return {tu_interop_compat.tu_interop_compat_lock["lock_auto"]["locale"]: self.auto,
                tu_interop_compat.tu_interop_compat_lock["lock_start"]["locale"]: {
                    tu_interop_compat.tu_interop_compat_time["hour"]["locale"]: self.target.time_start.hour,
                    tu_interop_compat.tu_interop_compat_time["minute"]["locale"]: self.target.time_start.minute,
                    tu_interop_compat.tu_interop_compat_time["second"]["locale"]: self.target.time_start.second,
                    tu_interop_compat.tu_interop_compat_time["millisecond"][
                        "locale"]: self.target.time_start.millisecond},
                tu_interop_compat.tu_interop_compat_lock["lock_end"]["locale"]: {
                    tu_interop_compat.tu_interop_compat_time["hour"]["locale"]: self.target.time_end.hour,
                    tu_interop_compat.tu_interop_compat_time["minute"]["locale"]: self.target.time_end.minute,
                    tu_interop_compat.tu_interop_compat_time["second"]["locale"]: self.target.time_end.second,
                    tu_interop_compat.tu_interop_compat_time["millisecond"][
                        "locale"]: self.target.time_end.millisecond}}

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
                "target": self.target.__dict__(),
                "judge": self.judge.__dict__(),
                "competition": self.competition.__dict__(),
                "foe": self.foe.__dict__(),
                "team": self.team,
                "speed": self.speed,
                "battery": self.battery,
                "auto": self.auto}

    def __str__(self):
        """
        get vehicle class dictionary as string

        :return: str
        """

        # expose vehicle class dictionary as string
        return str(self.__dict__())

    def server_login(self):
        """
        login to judge server

        :return: None
        """

        # call server login method from judge object
        self.judge.server_login()

    def server_logout(self):
        """
        logout from judge server

        :return: None
        """

        # call server logout method from judge object
        self.judge.server_logout()

    def server_time_get(self):
        """
        get server time from judge server

        :return: None
        """

        # call get server time method from judge object
        self.judge.server_time_get()

    def telemetry_connect(self):
        """
        connect to vehicle MAVLINK telemetry stream

        :return: None
        """

        # never connected before
        if self.__mavlink is None:

            # build up the connection string
            connection_string = "{0}:{1}".format(tu_settings.tu_telem_stream_ip,
                                                 tu_settings.tu_telem_stream_port_interop)

            # connect to the vehicle MAVLINK telemetry stream
            self.__mavlink = utility.mavlink_connection(connection_string)

            # wait for a single heartbeat
            self.__mavlink.wait_heartbeat()

            # vehicle connection is successful
            self.__connected = True

            # set telemetry stream rates
            self.__stream_rate_set()

            # never started the telemetry stream receiver thread
            if self.__thread_telemetry_get is None:

                # create the telemetry stream receiver thread
                self.__thread_telemetry_get = threading.Thread(target=self.__telemetry_get)

                # start the telemetry stream receiver thread
                self.__thread_telemetry_get.start()

    # set telemetry stream rates
    def __stream_rate_set(self):

        # create stream rate set message
        def stream_rate_set_message(target_system, target_component, message_id, message_frequency):

            # build up the MAVLINK command
            return dialect.MAVLink_command_long_message(target_system=target_system,
                                                        target_component=target_component,
                                                        command=dialect.MAV_CMD_SET_MESSAGE_INTERVAL,
                                                        confirmation=0,
                                                        param1=message_id,
                                                        param2=1e6 / message_frequency,
                                                        param3=0,
                                                        param4=0,
                                                        param5=0,
                                                        param6=0,
                                                        param7=0)

        # send stream rate set message to vehicle
        def stream_rate_set(message_id, message_frequency):

            # create message (command)
            message = stream_rate_set_message(target_system=self.__mavlink.target_system,
                                              target_component=self.__mavlink.target_component,
                                              message_id=message_id,
                                              message_frequency=message_frequency)

            # send built message (command) to the vehicle
            self.__mavlink.mav.send(message)

        # for each telemetry stream
        for stream_id in (dialect.MAVLINK_MSG_ID_GLOBAL_POSITION_INT,
                          dialect.MAVLINK_MSG_ID_ATTITUDE,
                          dialect.MAVLINK_MSG_ID_VFR_HUD,
                          dialect.MAVLINK_MSG_ID_SYS_STATUS,
                          dialect.MAVLINK_MSG_ID_SYSTEM_TIME):

            # set the stream rate
            stream_rate_set(message_id=stream_id, message_frequency=5)

    # telemetry receiver thread method
    def __telemetry_get(self):

        # do below always
        while True:

            # receive a single MAVLINK message
            message = self.__mavlink.recv_msg()

            # not received a message
            if not message:
                continue

            # convert received message to dictionary
            message = message.to_dict()

            # message is GLOBAL_POSITION_INT MAVLINK message
            if message["mavpackettype"] == dialect.MAVLink_global_position_int_message.name:

                # get latitude, longitude, relative altitude and heading of the vehicle
                self.location.latitude = message["lat"] * 1e-7
                self.location.longitude = message["lon"] * 1e-7
                self.location.altitude = message["relative_alt"] * 1e-3
                self.attitude.heading = message["hdg"] * 1e-2

            # message is ATTITUDE MAVLINK message
            elif message["mavpackettype"] == dialect.MAVLink_attitude_message.name:

                # get roll and pitch of the vehicle
                self.attitude.roll = math.degrees(message["roll"])
                self.attitude.pitch = math.degrees(message["pitch"])

            # message is VFR_HUD MAVLINK message
            elif message["mavpackettype"] == dialect.MAVLink_vfr_hud_message.name:

                # get ground speed of the vehicle
                self.__speed = message["groundspeed"]

            # message is SYS_STATUS MAVLINK message
            elif message["mavpackettype"] == dialect.MAVLink_sys_status_message.name:

                # get remaining battery percent of the vehicle
                self.__battery = message["battery_remaining"]

            # message is SYSTEM_TIME MAVLINK message
            elif message["mavpackettype"] == dialect.MAVLink_system_time_message.name:

                # get system time of the vehicle
                unix_time = message["time_unix_usec"]
                unix_time = datetime.datetime.utcfromtimestamp(unix_time * 1e-6)
                self.time.hour = unix_time.hour
                self.time.minute = unix_time.minute
                self.time.second = unix_time.second
                self.time.millisecond = int(unix_time.microsecond * 1e-3)
