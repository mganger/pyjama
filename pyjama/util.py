from threading import Thread
from time import sleep

def daemon(*args, **kwargs):
    thread = Thread(*args, **kwargs)
    thread.daemon = True
    return thread

def every(interval, target):
    def new_target():
        while True:
            target()
            sleep(interval)
    return new_target
