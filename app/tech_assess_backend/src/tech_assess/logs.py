import logging
import os
import sys
import time
from functools import wraps

from flask import request

DEFAULT_LOG_FORMAT = "[%(asctime)-15s] %(levelname)-8s %(name)s: %(message)s"
DEFAULT_LOG_FORMATTER = logging.Formatter(DEFAULT_LOG_FORMAT)

info_handler = logging.StreamHandler(stream=sys.stdout)
info_handler.setFormatter(DEFAULT_LOG_FORMATTER)
info_handler.setLevel(logging.INFO)

error_handler = logging.StreamHandler(stream=sys.stderr)
error_handler.setFormatter(DEFAULT_LOG_FORMATTER)
error_handler.setLevel(logging.ERROR)

logging.basicConfig(format=DEFAULT_LOG_FORMAT)
logger = logging.getLogger()

werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.setLevel(logging.INFO)
werkzeug_logger.addHandler(info_handler)
werkzeug_logger.addHandler(error_handler)


def log_request_time(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        start = time.perf_counter()
        result = f(*args, **kwargs)
        elapsed = time.perf_counter() - start

        logger.info({"endpoint": request.endpoint, "elapsed": elapsed})
        return result

    return decorated_function


class Benchmarker:

    def __init__(self, name, logger=logger):
        self.logger = logger
        self.name = name + " BM"
        self.steps = []

    def start(self):
        self.steps.append(time.time())
        self.logger.info(self.name + ": start : " + str(self.steps[0]))
        return self

    def add_step(self, step_name="step"):
        self.steps.append(time.time())
        self.logger.info(self.name + ": " + step_name + " : " +
                         str(self.steps[-1] - self.steps[-2]))

    def end(self):
        self.steps.append(time.time())
        self.logger.info(self.name + ": total : " +
                         str(self.steps[-1] - self.steps[0]))
