import tu_interop_compat


class Time:
    def __init__(self, hour=0, minute=0, second=0, millisecond=0):
        self.__hour = hour
        self.__minute = minute
        self.__second = second
        self.__millisecond = millisecond

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
        self.__hour = hour

    @minute.setter
    def minute(self, minute: int):
        self.__minute = minute

    @second.setter
    def second(self, second: int):
        self.__second = second

    @millisecond.setter
    def millisecond(self, millisecond: int):
        self.__millisecond = millisecond

    def __dict__(self):
        return {"hour": self.hour,
                "minute": self.minute,
                "second": self.second,
                "millisecond": self.millisecond}

    def __str__(self):
        return str(self.__dict__())


class Location:
    def __init__(self, latitude=0.0, longitude=0.0, altitude=0.0):
        self.__latitude = latitude
        self.__longitude = longitude
        self.__altitude = altitude

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
        self.__latitude = latitude

    @longitude.setter
    def longitude(self, longitude: float):
        self.__longitude = longitude

    @altitude.setter
    def altitude(self, altitude: float):
        self.__altitude = altitude

    def __dict__(self):
        return {"latitude": self.latitude,
                "longitude": self.longitude,
                "altitude": self.altitude}

    def __str__(self):
        return str(self.__dict__())


class Attitude:
    def __init__(self, roll=0.0, pitch=0.0, heading=0.0):
        self.__roll = roll
        self.__pitch = pitch
        self.__heading = heading

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
        self.__roll = roll

    @pitch.setter
    def pitch(self, pitch: float):
        self.__pitch = pitch

    @heading.setter
    def heading(self, heading: float):
        self.__heading = heading

    def __dict__(self):
        return {"roll": self.roll,
                "pitch": self.pitch,
                "heading": self.heading}

    def __str__(self):
        return str(self.__dict__())


class Target:
    def __init__(self, lock=0, x=0, y=0, width=0, height=0):
        self.time_start = Time()
        self.time_end = Time()
        self.__lock = lock
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height

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
        self.__lock = lock

    @x.setter
    def x(self, x: int):
        self.__x = x

    @y.setter
    def y(self, y: int):
        self.__y = y

    @width.setter
    def width(self, width: int):
        self.__width = width

    @height.setter
    def height(self, height: int):
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


class Judge:
    def __init__(self):
        self.time = Time()

    def __dict__(self):
        return {"time": self.time.__dict__()}

    def __str__(self):
        return str(self.__dict__())


class Vehicle:
    def __init__(self, team: int):
        self.time = Time()
        self.location = Location()
        self.attitude = Attitude()
        self.target = Target()
        self.__team = team
        self.__speed = 0.0
        self.__battery = 0.0
        self.__auto = 0

    @property
    def team(self):
        return self.__team

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
        self.__speed = speed

    @battery.setter
    def battery(self, battery: float):
        self.__battery = battery

    @auto.setter
    def auto(self, auto: int):
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

    def __dict__(self):
        return {"time": self.time.__dict__(),
                "location": self.location.__dict__(),
                "attitude": self.attitude.__dict__(),
                "target": self.target.__dict__(),
                "team": self.team,
                "speed": self.speed,
                "battery": self.battery,
                "auto": self.auto}

    def __str__(self):
        return str(self.__dict__())


if __name__ == "__main__":
    import pprint

    my_vehicle = Vehicle(team=26)
    my_judge = Judge()

    pprint.pprint(my_vehicle.__dict__(), width=1, sort_dicts=False)
    pprint.pprint(my_judge.__dict__(), width=1, sort_dicts=False)
    pprint.pprint(my_vehicle.dict_judge_telemetry, width=1, sort_dicts=False)
    pprint.pprint(my_vehicle.dict_judge_lock, width=1, sort_dicts=False)
