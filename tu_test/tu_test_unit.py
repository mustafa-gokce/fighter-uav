import unittest
import tu_interop.tu_interop_object
import tu_settings


class TestTime(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("Time class unit test started!")

    @classmethod
    def tearDownClass(cls) -> None:
        print("Time class unit test ended")

    def setUp(self) -> None:
        self.time = tu_interop.tu_interop_object.Time()

    def tearDown(self) -> None:
        pass

    def test_init(self):
        self.assertEqual(self.time.hour, 0)
        self.assertEqual(self.time.minute, 0)
        self.assertEqual(self.time.second, 0)
        self.assertEqual(self.time.millisecond, 0)

    def test_hour(self):
        self.time.hour = 23
        self.assertEqual(self.time.hour, 23)

        self.time.hour = 23.4
        self.assertEqual(self.time.hour, 23)

        self.time.hour = 23.6
        self.assertEqual(self.time.hour, 23)

        with self.assertRaises(ValueError):
            self.time.hour = -1

        with self.assertRaises(ValueError):
            self.time.hour = 24

        with self.assertRaises(TypeError):
            self.time.hour = "hour"

    def test_minute(self):
        self.time.minute = 59
        self.assertEqual(self.time.minute, 59)

        self.time.minute = 59.4
        self.assertEqual(self.time.minute, 59)

        self.time.minute = 59.6
        self.assertEqual(self.time.minute, 59)

        with self.assertRaises(ValueError):
            self.time.minute = -1

        with self.assertRaises(ValueError):
            self.time.minute = 60

        with self.assertRaises(TypeError):
            self.time.minute = "minute"

    def test_second(self):
        self.time.second = 59
        self.assertEqual(self.time.second, 59)

        self.time.second = 59.4
        self.assertEqual(self.time.second, 59)

        self.time.second = 59.6
        self.assertEqual(self.time.second, 59)

        with self.assertRaises(ValueError):
            self.time.second = -1

        with self.assertRaises(ValueError):
            self.time.second = 60

        with self.assertRaises(TypeError):
            self.time.second = "second"

    def test_millisecond(self):
        self.time.millisecond = 999
        self.assertEqual(self.time.millisecond, 999)

        self.time.millisecond = 999.4
        self.assertEqual(self.time.millisecond, 999)

        self.time.millisecond = 999.6
        self.assertEqual(self.time.millisecond, 999)

        with self.assertRaises(ValueError):
            self.time.millisecond = -1

        with self.assertRaises(ValueError):
            self.time.millisecond = 1000

        with self.assertRaises(TypeError):
            self.time.millisecond = "millisecond"


class TestLocation(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("Location class unit test started!")

    @classmethod
    def tearDownClass(cls) -> None:
        print("Location class unit test ended")

    def setUp(self) -> None:
        self.location = tu_interop.tu_interop_object.Location()

    def tearDown(self) -> None:
        pass

    def test_init(self):
        self.assertEqual(self.location.latitude, 0.0)
        self.assertEqual(self.location.longitude, 0.0)
        self.assertEqual(self.location.altitude, 0.0)

    def test_latitude(self):
        self.location.latitude = -89.999999
        self.assertEqual(self.location.latitude, -89.999999)

        self.location.latitude = 89.999999
        self.assertEqual(self.location.latitude, 89.999999)

        self.location.latitude = 0.0
        self.assertEqual(self.location.latitude, 0.0)

        with self.assertRaises(ValueError):
            self.location.latitude = -90.000001

        with self.assertRaises(ValueError):
            self.location.latitude = 90.000001

        with self.assertRaises(TypeError):
            self.location.latitude = "latitude"

    def test_longitude(self):
        self.location.longitude = -179.999999
        self.assertEqual(self.location.longitude, -179.999999)

        self.location.longitude = 179.999999
        self.assertEqual(self.location.longitude, 179.999999)

        self.location.longitude = 0.0
        self.assertEqual(self.location.longitude, 0.0)

        with self.assertRaises(ValueError):
            self.location.longitude = -180.000001

        with self.assertRaises(ValueError):
            self.location.longitude = 180.000001

        with self.assertRaises(TypeError):
            self.location.longitude = "longitude"

    def test_altitude(self):
        self.location.altitude = -1.1
        self.assertEqual(self.location.altitude, -1.1)

        self.location.altitude = 5
        self.assertEqual(self.location.altitude, 5.0)

        self.location.altitude = 0.0
        self.assertEqual(self.location.altitude, 0.0)

        with self.assertRaises(TypeError):
            self.location.altitude = "altitude"


class TestAttitude(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("Attitude class unit test started!")

    @classmethod
    def tearDownClass(cls) -> None:
        print("Attitude class unit test ended")

    def setUp(self) -> None:
        self.attitude = tu_interop.tu_interop_object.Attitude()

    def tearDown(self) -> None:
        pass

    def test_init(self):
        self.assertEqual(self.attitude.roll, 0.0)
        self.assertEqual(self.attitude.pitch, 0.0)
        self.assertEqual(self.attitude.heading, 0.0)

    def test_roll(self):
        self.attitude.roll = -179.999999
        self.assertEqual(self.attitude.roll, -179.999999)

        self.attitude.roll = 179.999999
        self.assertEqual(self.attitude.roll, 179.999999)

        self.attitude.roll = 0.0
        self.assertEqual(self.attitude.roll, 0.0)

        with self.assertRaises(ValueError):
            self.attitude.roll = -180.000001

        with self.assertRaises(ValueError):
            self.attitude.roll = 180.000001

        with self.assertRaises(TypeError):
            self.attitude.roll = "roll"

    def test_pitch(self):
        self.attitude.pitch = -179.999999
        self.assertEqual(self.attitude.pitch, -179.999999)

        self.attitude.pitch = 179.999999
        self.assertEqual(self.attitude.pitch, 179.999999)

        self.attitude.pitch = 0.0
        self.assertEqual(self.attitude.pitch, 0.0)

        with self.assertRaises(ValueError):
            self.attitude.pitch = -180.000001

        with self.assertRaises(ValueError):
            self.attitude.pitch = 180.000001

        with self.assertRaises(TypeError):
            self.attitude.pitch = "pitch"

    def test_heading(self):
        self.attitude.heading = 0.1
        self.assertEqual(self.attitude.heading, 0.1)

        self.attitude.heading = 359.9
        self.assertEqual(self.attitude.heading, 359.9)

        self.attitude.heading = 0.0
        self.assertEqual(self.attitude.heading, 0.0)

        with self.assertRaises(ValueError):
            self.attitude.heading = -0.1

        with self.assertRaises(ValueError):
            self.attitude.heading = 360.1

        with self.assertRaises(TypeError):
            self.attitude.heading = "heading"


class TestTarget(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("Target class unit test started!")

    @classmethod
    def tearDownClass(cls) -> None:
        print("Target class unit test ended")

    def setUp(self) -> None:
        self.target = tu_interop.tu_interop_object.Target()

    def tearDown(self) -> None:
        pass

    def test_init(self):
        self.assertEqual(self.target.lock, 0)
        self.assertEqual(self.target.x, 0)
        self.assertEqual(self.target.y, 0)
        self.assertEqual(self.target.width, 0)
        self.assertEqual(self.target.height, 0)

    def test_lock(self):
        self.target.lock = 1
        self.assertEqual(self.target.lock, 1)

        self.target.lock = 0
        self.assertEqual(self.target.lock, 0)

        with self.assertRaises(ValueError):
            self.target.lock = 2

        with self.assertRaises(TypeError):
            self.target.lock = 0.1

        with self.assertRaises(TypeError):
            self.target.lock = "lock"

    def test_x(self):
        self.target.x = 0
        self.assertEqual(self.target.x, 0)

        self.target.x = tu_settings.tu_video_stream_width
        self.assertEqual(self.target.x, tu_settings.tu_video_stream_width)

        with self.assertRaises(ValueError):
            self.target.x = -1

        with self.assertRaises(ValueError):
            self.target.x = tu_settings.tu_video_stream_width + 1

        with self.assertRaises(TypeError):
            self.target.x = 0.1

        with self.assertRaises(TypeError):
            self.target.x = "x"

    def test_y(self):
        self.target.y = 0
        self.assertEqual(self.target.y, 0)

        self.target.y = tu_settings.tu_video_stream_height
        self.assertEqual(self.target.y, tu_settings.tu_video_stream_height)

        with self.assertRaises(ValueError):
            self.target.y = -1

        with self.assertRaises(ValueError):
            self.target.y = tu_settings.tu_video_stream_height + 1

        with self.assertRaises(TypeError):
            self.target.y = 0.1

        with self.assertRaises(TypeError):
            self.target.y = "y"

    def test_width(self):
        self.target.width = 0
        self.assertEqual(self.target.width, 0)

        self.target.width = tu_settings.tu_video_stream_width - 1
        self.assertEqual(self.target.width, tu_settings.tu_video_stream_width - 1)

        with self.assertRaises(ValueError):
            self.target.width = -1

        with self.assertRaises(ValueError):
            self.target.width = tu_settings.tu_video_stream_width

        with self.assertRaises(TypeError):
            self.target.width = 0.1

        with self.assertRaises(TypeError):
            self.target.width = "width"

    def test_height(self):
        self.target.height = 0
        self.assertEqual(self.target.height, 0)

        self.target.height = tu_settings.tu_video_stream_height - 1
        self.assertEqual(self.target.height, tu_settings.tu_video_stream_height - 1)

        with self.assertRaises(ValueError):
            self.target.height = -1

        with self.assertRaises(ValueError):
            self.target.height = tu_settings.tu_video_stream_height

        with self.assertRaises(TypeError):
            self.target.height = 0.1

        with self.assertRaises(TypeError):
            self.target.height = "height"


class TestCredential(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("Credential class unit test started!")

    @classmethod
    def tearDownClass(cls) -> None:
        print("Credential class unit test ended")

    def setUp(self) -> None:
        self.credential = tu_interop.tu_interop_object.Credential()

    def tearDown(self) -> None:
        pass

    def test_init(self):
        self.assertEqual(self.credential.user_name, "")
        self.assertEqual(self.credential.user_password, "")

    def test_name(self):
        self.credential.user_name = "u"
        self.assertEqual(self.credential.user_name, "u")

        self.credential.user_name = "user"
        self.assertEqual(self.credential.user_name, "user")

        with self.assertRaises(ValueError):
            self.credential.user_name = ""

        with self.assertRaises(TypeError):
            self.credential.user_name = 0

    def test_password(self):
        self.credential.user_password = "p"
        self.assertEqual(self.credential.user_password, "p")

        self.credential.user_password = "password"
        self.assertEqual(self.credential.user_password, "password")

        with self.assertRaises(ValueError):
            self.credential.user_password = ""

        with self.assertRaises(TypeError):
            self.credential.user_password = 0


class TestBaseVehicle(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("BaseVehicle class unit test started!")

    @classmethod
    def tearDownClass(cls) -> None:
        print("BaseVehicle class unit test ended")

    def setUp(self) -> None:
        self.base_vehicle = tu_interop.tu_interop_object.BaseVehicle()

    def tearDown(self) -> None:
        pass

    def test_init(self):
        self.assertEqual(self.base_vehicle.team, 0)

    def test_team(self):
        self.base_vehicle.team = 0
        self.assertEqual(self.base_vehicle.team, 0)

        with self.assertRaises(ValueError):
            self.base_vehicle.team = -1

        with self.assertRaises(TypeError):
            self.base_vehicle.team = 0.1

        with self.assertRaises(TypeError):
            self.base_vehicle.team = "team"


class TestFoe(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("Foe class unit test started!")

    @classmethod
    def tearDownClass(cls) -> None:
        print("Foe class unit test ended")

    def setUp(self) -> None:
        self.foe = tu_interop.tu_interop_object.Foe()

    def tearDown(self) -> None:
        pass


class TestVehicle(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("Vehicle class unit test started!")

    @classmethod
    def tearDownClass(cls) -> None:
        print("Vehicle class unit test ended")

    def setUp(self) -> None:
        self.vehicle = tu_interop.tu_interop_object.Vehicle()

    def tearDown(self) -> None:
        pass

    def test_init(self):
        self.assertEqual(self.vehicle.speed, 0.0)
        self.assertEqual(self.vehicle.battery, 0.0)
        self.assertEqual(self.vehicle.auto, 0)

    def test_speed(self):
        self.vehicle.speed = -1.1
        self.assertEqual(self.vehicle.speed, -1.1)

        self.vehicle.speed = 5
        self.assertEqual(self.vehicle.speed, 5.0)

        self.vehicle.speed = 0.0
        self.assertEqual(self.vehicle.speed, 0.0)

        with self.assertRaises(TypeError):
            self.vehicle.speed = "speed"

    def test_battery(self):
        self.vehicle.battery = 0.1
        self.assertEqual(self.vehicle.battery, 0.1)

        self.vehicle.battery = 99.9
        self.assertEqual(self.vehicle.battery, 99.9)

        self.vehicle.battery = 0.0
        self.assertEqual(self.vehicle.battery, 0.0)

        self.vehicle.battery = 50
        self.assertEqual(self.vehicle.battery, 50.0)

        with self.assertRaises(ValueError):
            self.vehicle.battery = -0.1

        with self.assertRaises(ValueError):
            self.vehicle.battery = 100.1

        with self.assertRaises(TypeError):
            self.vehicle.battery = "battery"

    def test_auto(self):
        self.vehicle.auto = 1
        self.assertEqual(self.vehicle.auto, 1)

        self.vehicle.auto = 0
        self.assertEqual(self.vehicle.auto, 0)

        with self.assertRaises(ValueError):
            self.vehicle.auto = 2

        with self.assertRaises(TypeError):
            self.vehicle.auto = 0.1

        with self.assertRaises(TypeError):
            self.vehicle.auto = "auto"


class TestJudge(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("Judge class unit test started!")

    @classmethod
    def tearDownClass(cls) -> None:
        print("Judge class unit test ended")

    def setUp(self) -> None:
        self.judge = tu_interop.tu_interop_object.Judge()

    def tearDown(self) -> None:
        pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
