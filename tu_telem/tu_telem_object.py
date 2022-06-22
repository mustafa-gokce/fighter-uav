import time
import requests
import threading
import logging
import settings


class Receiver:
    def __init__(self):
        self.__response = {}
        self.__session = requests.Session()
        self.__url = "http://{0}:{1}/telemetry_get".format(tu_settings.core_server_ip,
                                                           tu_settings.core_server_port)
        self.__telemetry_get_thread = threading.Thread(target=self.__telemetry_get)

        # silence the requests library
        urllib3_logger = logging.getLogger("urllib3")
        urllib3_logger.setLevel(logging.CRITICAL)

        # start the thread
        self.__telemetry_get_thread.start()

    def __telemetry_get(self):

        # do below always
        while True:

            # try to get telemetry data from core server
            try:

                # get telemetry data from core server
                response = self.__session.get(url=self.__url)

                # parse the response content
                self.__response = response.json()

            # catch all exceptions
            except Exception as e:

                # assign response to empty dictionary
                self.__response = {}

            # cool down the update rate
            time.sleep(0.2)

    @property
    def telemetry_get(self):
        return self.__response
