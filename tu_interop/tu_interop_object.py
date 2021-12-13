import tu_interop.tu_interop_compat as tu_interop_compat
import tu_settings


class Time:
    def __init__(self):
        self.__hour = 0
        self.__minute = 0
        self.__second = 0
        self.__millisecond = 0

    @property
    def hour(self):
        return self.__hour

    @property
    def minute(self):
        return self.__minute

    @property
    def second(self):
        return self.__second

    @property
    def millisecond(self):
        return self.__millisecond

    @hour.setter
    def hour(self, hour: int):
        if type(hour) not in (int, float):
            raise TypeError
        if not 0 <= hour < 24:
            raise ValueError
        self.__hour = int(hour)

    @minute.setter
    def minute(self, minute: int):
        if type(minute) not in (int, float):
            raise TypeError
        if not 0 <= minute < 60:
            raise ValueError
        self.__minute = int(minute)

    @second.setter
    def second(self, second: int):
        if type(second) not in (int, float):
            raise TypeError
        if not 0 <= second < 60:
            raise ValueError
        self.__second = int(second)

    @millisecond.setter
    def millisecond(self, millisecond: int):
        if type(millisecond) not in (int, float):
            raise TypeError
        if not 0 <= millisecond < 1000:
            raise ValueError
        self.__millisecond = int(millisecond)

    def __dict__(self):
        return {"hour": self.hour,
                "minute": self.minute,
                "second": self.second,
                "millisecond": self.millisecond}

    def __str__(self):
        return str(self.__dict__())


class Location:
    def __init__(self):
        self.__latitude = 0.0
        self.__longitude = 0.0
        self.__altitude = 0.0

    @property
    def latitude(self):
        return self.__latitude

    @property
    def longitude(self):
        return self.__longitude

    @property
    def altitude(self):
        return self.__altitude

    @latitude.setter
    def latitude(self, latitude: float):
        if type(latitude) not in (int, float):
            raise TypeError
        if not -90.0 <= latitude <= 90.0:
            raise ValueError
        self.__latitude = float(latitude)

    @longitude.setter
    def longitude(self, longitude: float):
        if type(longitude) not in (int, float):
            raise TypeError
        if not -180.0 <= longitude <= 180.0:
            raise ValueError
        self.__longitude = float(longitude)

    @altitude.setter
    def altitude(self, altitude: float):
        if type(altitude) not in (int, float):
            raise TypeError
        self.__altitude = float(altitude)

    def __dict__(self):
        return {"latitude": self.latitude,
                "longitude": self.longitude,
                "altitude": self.altitude}

    def __str__(self):
        return str(self.__dict__())


class Attitude:
    def __init__(self):
        self.__roll = 0.0
        self.__pitch = 0.0
        self.__heading = 0.0

    @property
    def roll(self):
        return self.__roll

    @property
    def pitch(self):
        return self.__pitch

    @property
    def heading(self):
        return self.__heading

    @roll.setter
    def roll(self, roll: float):
        if type(roll) not in (int, float):
            raise TypeError
        if not -180.0 <= roll <= 180.0:
            raise ValueError
        self.__roll = float(roll)

    @pitch.setter
    def pitch(self, pitch: float):
        if type(pitch) not in (int, float):
            raise TypeError
        if not -180.0 <= pitch <= 180.0:
            raise ValueError
        self.__pitch = float(pitch)

    @heading.setter
    def heading(self, heading: float):
        if type(heading) not in (int, float):
            raise TypeError
        if not 0.0 <= heading <= 360.0:
            raise ValueError
        self.__heading = float(heading)

    def __dict__(self):
        return {"roll": self.roll,
                "pitch": self.pitch,
                "heading": self.heading}

    def __str__(self):
        return str(self.__dict__())


class Target:
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
        return self.__lock

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @lock.setter
    def lock(self, lock: int):
        if type(lock) != int:
            raise TypeError
        if lock not in (0, 1):
            raise ValueError
        self.__lock = lock

    @x.setter
    def x(self, x: int):
        if type(x) != int:
            raise TypeError
        if not 0 <= x <= tu_settings.tu_video_stream_width:
            raise ValueError
        self.__x = x

    @y.setter
    def y(self, y: int):
        if type(y) != int:
            raise TypeError
        if not 0 <= y <= tu_settings.tu_video_stream_height:
            raise ValueError
        self.__y = y

    @width.setter
    def width(self, width: int):
        if type(width) != int:
            raise TypeError
        if not 0 <= width < tu_settings.tu_video_stream_width:
            raise ValueError
        self.__width = width

    @height.setter
    def height(self, height: int):
        if type(height) != int:
            raise TypeError
        if not 0 <= height < tu_settings.tu_video_stream_height:
            raise ValueError
        self.__height = height

    def __dict__(self):
        return {"time_start": self.time_start.__dict__(),
                "time_end": self.time_end.__dict__(),
                "lock": self.lock,
                "x": self.x,
                "y": self.y,
                "width": self.width,
                "height": self.height}

    def __str__(self):
        return str(self.__dict__())


class Credential:
    def __init__(self):
        self.__user_name = ""
        self.__user_password = ""

    @property
    def user_name(self):
        return self.__user_name

    @property
    def user_password(self):
        return self.__user_password

    @user_name.setter
    def user_name(self, user_name: str):
        if type(user_name) != str:
            raise TypeError
        if user_name == "":
            raise ValueError
        self.__user_name = user_name

    @user_password.setter
    def user_password(self, user_password: str):
        if type(user_password) != str:
            raise TypeError
        if user_password == "":
            raise ValueError
        self.__user_password = user_password

    def __dict__(self):
        return {"user_name": self.user_name,
                "user_password": self.user_password}

    def __str__(self):
        return str(self.__dict__())


class BaseVehicle:
    def __init__(self):
        self.time = Time()
        self.location = Location()
        self.attitude = Attitude()
        self.__team = 0

    @property
    def team(self):
        return self.__team

    @team.setter
    def team(self, team: int):
        if type(team) != int:
            raise TypeError
        if team < 0:
            raise ValueError
        self.__team = team

    def __dict__(self):
        return {"time": self.time.__dict__(),
                "location": self.location.__dict__(),
                "attitude": self.attitude.__dict__(),
                "team": self.team}

    def __str__(self):
        return str(self.__dict__())


class Foe(BaseVehicle):
    def __init__(self):
        super().__init__()

    def __dict__(self):
        return {"time": self.time.__dict__(),
                "location": self.location.__dict__(),
                "attitude": self.attitude.__dict__(),
                "team": self.team}

    def __str__(self):
        return str(self.__dict__())


class Vehicle(BaseVehicle):
    def __init__(self):
        super().__init__()
        self.target = Target()
        self.credential = Credential()
        self.foe = Foe()
        self.__speed = 0.0
        self.__battery = 0.0
        self.__auto = 0

    @property
    def speed(self):
        return self.__speed

    @property
    def battery(self):
        return self.__battery

    @property
    def auto(self):
        return self.__auto

    @speed.setter
    def speed(self, speed: float):
        if type(speed) not in (int, float):
            raise TypeError
        self.__speed = float(speed)

    @battery.setter
    def battery(self, battery: float):
        if type(battery) not in (int, float):
            raise TypeError
        if not 0.0 <= battery <= 100.0:
            raise ValueError
        self.__battery = float(battery)

    @auto.setter
    def auto(self, auto: int):
        if type(auto) != int:
            raise TypeError
        if auto not in (0, 1):
            raise ValueError
        self.__auto = auto

    @property
    def dict_judge_telemetry(self):
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
    def dict_judge_lock(self):
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

    @property
    def dict_judge_login(self):
        return {tu_interop_compat.tu_interop_compat_login["user_name"]["locale"]: self.credential.user_name,
                tu_interop_compat.tu_interop_compat_login["user_password"]["locale"]: self.credential.user_password}

    def __dict__(self):
        return {"time": self.time.__dict__(),
                "location": self.location.__dict__(),
                "attitude": self.attitude.__dict__(),
                "target": self.target.__dict__(),
                "credential": self.credential.__dict__(),
                "foe": self.foe.__dict__(),
                "team": self.team,
                "speed": self.speed,
                "battery": self.battery,
                "auto": self.auto}

    def __str__(self):
        return str(self.__dict__())


class Judge:
    def __init__(self):
        self.__time = Time()
        self.__path_login = tu_interop_compat.tu_interop_compat_path_server_login
        self.__path_logout = tu_interop_compat.tu_interop_compat_path_server_logout
        self.__path_time = tu_interop_compat.tu_interop_compat_path_server_time
        self.__path_send = tu_interop_compat.tu_interop_compat_path_server_send
        self.__path_lock = tu_interop_compat.tu_interop_compat_path_server_lock
        self.__connected = False
        self.__allowed = False
        self.__foes = []

    @property
    def time(self):
        return self.__time

    @property
    def path_login(self):
        return self.__path_login

    @property
    def path_logout(self):
        return self.__path_logout

    @property
    def path_time(self):
        return self.__path_time

    @property
    def path_send(self):
        return self.__path_send

    @property
    def path_lock(self):
        return self.__path_lock

    @property
    def connected(self):
        return self.__connected

    @property
    def allowed(self):
        return self.__allowed

    @property
    def foes(self):
        return self.__foes

    def __dict__(self):
        return {"time": self.time.__dict__(),
                "path_login": self.path_login,
                "path_logout": self.path_logout,
                "path_time": self.path_time,
                "path_send": self.path_send,
                "path_lock": self.path_lock,
                "connected": self.connected,
                "allowed": self.allowed,
                "foes": [foe.__dict__() for foe in self.foes]}

    def __str__(self):
        return str(self.__dict__())


if __name__ == "__main__":
    import pprint

    my_vehicle = Vehicle()
    my_judge = Judge()

    pprint.pprint(my_vehicle.__dict__(), width=1)
    pprint.pprint(my_judge.__dict__(), width=1)
    # pprint.pprint(my_vehicle.dict_judge_telemetry, width=1)
    # pprint.pprint(my_vehicle.dict_judge_lock, width=1)
    # pprint.pprint(my_vehicle.dict_judge_login, width=1)
