import board
import time

from digitalio  import DigitalInOut, Direction, Pull
from analogio   import AnalogIn

from heater     import Heater
from timer      import Timer
from thermistor import Thermistor

# Engine Running Signal
engine_pin           = DigitalInOut(board.GP26)
engine_pin.direction = Direction.INPUT
engine_pin.pull      = Pull.DOWN

# Battery Charge Signal
charge_pin           = DigitalInOut(board.GP27)
charge_pin.direction = Direction.OUTPUT
charge_pin.value     = False

# Debug LED
dbg_pin              = DigitalInOut(board.GP21)
dbg_pin.direction    = Direction.OUTPUT
dbg_pin.value        = True

# Event Loop Timer
timer    = time.monotonic()

# Heater Array
heaters = {}
heaters["WINDSHIELD"] = Heater(                                # Heated Windscreen
    board.GP0,                                                 # Relay Pin
    board.GP2,                                                 # Switch Pin
    ((board.GP1, 300),),                                       # Levels
    Timer()                                                    # Limit Class
)
heaters["MIRROR"] = Heater(                                    # Heated Mirrors
    board.GP6,                                                 # Relay Pin
    board.GP8,                                                 # Switch Pin
    ((board.GP7, 300),),                                       # Levels
    Timer()                                                    # Limit Class
)
heaters["WHEEL"] = Heater(                                     # Heated Steering Wheel
    board.GP10,                                                # Relay Pin
    board.GP22,                                                # Switch Pin
    ((board.GP9, 18),),                                        # Levels
    Thermistor(1, 1)                                           # Limit Class
)
heaters["DRV_SEAT"] = Heater(                                  # Heated Drivers Seat
    board.GP11,                                                # Relay Pin
    board.GP15,                                                # Switch Pin
    ((board.GP12, 28), (board.GP13, 30), (board.GP14, 32)),    # Levels
    Thermistor(1, 0)                                           # Limit Class
)
heaters["PAS_SEAT"] = Heater(                                  # Heated Passenger Seat
    board.GP16,                                                # Relay Pin
    board.GP20,                                                # Switch Pin
    ((board.GP19, 28), (board.GP18, 30), (board.GP17, 32)),    # Levels
    Thermistor(0, 1)                                           # Limit Class
)

while True:
    # Scan for Button Presses
    for key in heaters.keys():
        if heaters[key].readSwitch():
            heaters[key].nextLevel()

    # Run Slow PID Loop
    if timer + 5 <= time.monotonic():
        timer = time.monotonic()
        for key in heaters.keys():
            heaters[key].pidLoop()


    # Enable Battery Charge Output if Engine ON and Heated Windscreen OFF
    charge_pin.value = False if heaters["WINDSHIELD"].getHeater() or not engine_pin.value else True

    time.sleep(0.001)
