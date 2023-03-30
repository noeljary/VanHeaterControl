import board
import time
from digitalio  import DigitalInOut, Direction, Pull

class Heater:

    state  = False
    relay  = None
    level  = 0
    levels = []
    switch = None
    limit  = None
    safety = {"VAL" : 0, "TIME" : 0}

    def __init__(self, relay, switch, levels, limit):
        self.relay           = DigitalInOut(relay)
        self.relay.direction = Direction.OUTPUT
        self.relay.value     = False

        self.switch           = DigitalInOut(switch)
        self.switch.direction = Direction.INPUT
        self.switch.pull      = Pull.UP

        self.limit         = limit
        self.safety["VAL"] = limit.value()

        self.levels = []
        for level in levels:
            led           = DigitalInOut(level[0])
            led.direction = Direction.OUTPUT
            led.value     = False
            self.levels.append([led, level[1]])

    def readSwitch(self):
        switch = False
        while not self.switch.value:
            switch = True
            time.sleep(0.01)

        return switch

    def nextLevel(self):
        if self.level == 0:
            self.enable()

        self.level = self.level + 1 if self.level < len(self.levels) else 0
        self.setLED()

        if self.level > 0:
            self.pidLoop()
        else:
            self.disable()

    def setLED(self):
        for i in range(0, len(self.levels)):
            self.levels[i][0].value = True if self.level - 1 >= i else False

    def pidLoop(self):
        if self.level == 0:
            return

        print("Current: {} - Target: {}".format(self.limit.value(), self.levels[self.level - 1][1]))

        if self.safety["TIME"] + 300 <= time.monotonic() and self.safety["VAL"] * 1.1 < self.limit.value():
            print("SAFETY DISABLE")
            self.disable()
            return

        if self.levels[self.level - 1][1] > self.limit.value():
            print("ELEMENT ON")
            self.setHeater(True)
        else:
            print("ELEMENT OFF")
            self.setHeater(False)
            if not self.limit.maintain:
                self.disable()

    def getHeater(self):
        return self.relay.value

    def setHeater(self, value):
        self.relay.value = value

    def enable(self):
        print("ENABLE")
        self.state = True
        self.safety["TIME"] = time.monotonic()
        self.limit.start()

    def disable(self):
        print("DISABLE")
        self.setHeater(False)
        self.state = False
        self.level = 0
        self.setLED()
