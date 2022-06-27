import sys
import logging


class Logger:

    def __init__(self, name="tu_log"):

        # logger settings
        file_name = name
        log_name = name
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        # create log file path
        full_path = "logs/" + file_name + ".log"

        # basic configs for logger
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format=log_format)

        # create logger and set level
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)

        # create a file handler
        handler = logging.FileHandler(full_path)
        handler.setLevel(logging.DEBUG)

        # create a logging format
        formatter = logging.Formatter(log_format)
        handler.setFormatter(formatter)

        # add the file handler to the logger
        logger.addHandler(handler)

        # bind logger
        self.logger = logging.getLogger(name)
