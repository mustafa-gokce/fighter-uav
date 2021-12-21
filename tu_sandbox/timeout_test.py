import time
import wrapt_timeout_decorator as timeout


@timeout.timeout(0.1)
def func():
    while True:
        time.sleep(1)


func()
