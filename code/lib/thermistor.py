import board
from digitalio  import DigitalInOut, Direction
from analogio   import AnalogIn

class Thermistor:

    a = None
    b = None

    maintain = True

    temperature = {"AIN" : AnalogIn(board.GP28), "PWR" : DigitalInOut(board.GP3), "SEL_A" : DigitalInOut(board.GP4), "SEL_B" : DigitalInOut(board.GP5)}
    for pin in ("PWR", "SEL_A", "SEL_B"):
        temperature[pin].direction = Direction.OUTPUT
        temperature[pin].value     = False

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def value(self):
        Thermistor.temperature["SEL_A"].value = self.a
        Thermistor.temperature["SEL_B"].value = self.b

        Thermistor.temperature["PWR"].value = True
        temp_value = (Thermistor.temperature["AIN"].value * 3.3) / 65536
        Thermistor.temperature["PWR"].value = False

        return temp_value

    def start(self):
        return
