import time

class Timer:

    maintain = False

    def __init__(self):
        self.reset()

    def reset(self):
        self.timer = 0

    def value(self):
        return time.monotonic() - self.timer

    def start(self):
        self.timer = time.monotonic()
