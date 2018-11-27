# Simple demo of reading each analog input from the ADS1x15 and printing it to
# the screen.
# Author: Tony DiCola
# License: Public Domain
# import time

# # Import the ADS1x15 module.
# import Adafruit_ADS1x15


# # Create an ADS1115 ADC (16-bit) instance.
# adc = Adafruit_ADS1x15.ADS1115()

# # Or create an ADS1015 ADC (12-bit) instance.
# #adc = Adafruit_ADS1x15.ADS1015()

# # Note you can change the I2C address from its default (0x48), and/or the I2C
# # bus by passing in these optional parameters:
# #adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# # Choose a gain of 1 for reading voltages from 0 to 4.09V.
# # Or pick a different gain to change the range of voltages that are read:
# #  - 2/3 = +/-6.144V
# #  -   1 = +/-4.096V
# #  -   2 = +/-2.048V
# #  -   4 = +/-1.024V
# #  -   8 = +/-0.512V
# #  -  16 = +/-0.256V
# # See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
# GAIN = 1

# # Print nice channel column headers.
# print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
# print('-' * 37)
# # Main loop.
# def read():
#     # Read all the ADC channel values in a list.
#     values = [0]*4
#     for i in range(4):
#         # Read the specified ADC channel using the previously set gain value.
#         values[i] = adc.read_adc(i, gain=GAIN)
#         # Note you can also pass in an optional data_rate parameter that controls
#         # the ADC conversion time (in samples/second). Each chip has a different
#         # set of allowed data rate values, see datasheet Table 9 config register
#         # DR bit values.
#         #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
#         # Each value will be a 12 or 16 bit signed integer value depending on the
#         # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
#     # Print the ADC values.
#     print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
#     # Pause for half a second.
#     # time.sleep(0.5)

import Adafruit_ADS1x15
import RPi.GPIO as GPIO
import time

# GPIO Pin definitions
LED_STARTUP = 26
LED_PUZZLE = 27
LED_JUNGLE = 10
LED_REPEAT = 11
LED_SKIP = 13

BTN_PUZZLE = 17
BTN_JUNGLE = 22
BTN_REPEAT = 9
BTN_SKIP = 5

class InOut(object):
    
    __instance = None
    
    def __init__(self, game):
        self._initADC()
        self._initGPIO()
        # self._readADC()
        # self._test()
        self.volume = {
            "prev": 0,
            "curr": 0
        }
        self.prevRepeat = 0
        self.prevSkip = 0

    def _initADC(self):
        if InOut.__instance != None:
            raise Exception("This class is a singleton")
        else:
            InOut.__instance = self
        print "Starting ADC"
        self.adc = Adafruit_ADS1x15.ADS1115()
        self.GAIN = 1
        # print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
        # print('-' * 37)
        
    def _initGPIO(self):
        print "GPIO setup"
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # LED pin definition
        GPIO.setup(LED_STARTUP,  GPIO.OUT)
        GPIO.setup(LED_PUZZLE,   GPIO.OUT)
        GPIO.setup(LED_JUNGLE,   GPIO.OUT)
        GPIO.setup(LED_REPEAT,   GPIO.OUT)
        GPIO.setup(LED_SKIP,     GPIO.OUT)
        # Set all LEDs off
        GPIO.output(LED_PUZZLE, GPIO.HIGH)
        GPIO.output(LED_JUNGLE, GPIO.HIGH)
        GPIO.output(LED_REPEAT, GPIO.HIGH)
        GPIO.output(LED_SKIP,   GPIO.HIGH)
        # Buttons
        GPIO.setup(BTN_PUZZLE,   GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(BTN_JUNGLE,   GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(BTN_REPEAT,   GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(BTN_SKIP,     GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # Set startup LED off:
        GPIO.output(LED_STARTUP, GPIO.HIGH)
        
    def _readADC(self):
        values = [0]*4
        for i in range(4):
            values[i] = self.adc.read_adc(i, gain=self.GAIN)
        print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))

    def _test(self):
        self.puzzleLedON()
        time.sleep(1)
        self.jungleLedON()
        time.sleep(1)
        self.repeatLED(1)
        time.sleep(1)
        self.repeatLED(0)
        time.sleep(1)
        self.skipLED(1)
        time.sleep(1)
        self.skipLED(0)
        time.sleep(1)

    # ------------------------------------------------------------------------- 
    # Public 
    # -------------------------------------------------------------------------

    def getVolumeKnob(self):
        self.volume["curr"] = self.adc.read_adc(0, gain=self.GAIN)
        if abs(self.volume["curr"] - self.volume["prev"]) > 1:
            self.volume["prev"] = self.volume["curr"]
            value = self.mapvalue(self.volume["curr"], 0, 26480, 0, 100)
            value = int(19.94 * value ** 0.358)
            if value > 100:
                value = 100
            return value

    def getPuzzleButton(self):
        if GPIO.input(BTN_PUZZLE):
            return True

    def getJungleButton(self):
        if GPIO.input(BTN_JUNGLE):
            return True

    def getRepeatButton(self):
        value = GPIO.input(BTN_REPEAT)
        # print ("value " + str(value) + " prev: " + str(self.prevRepeat))
        if value != self.prevRepeat:
            self.prevRepeat = value
            print "repeat btn changed"
            return value
        return None
        
    def getSkipButton(self):
        value = GPIO.input(BTN_SKIP)
        if value != self.prevSkip:
            self.prevSkip = value
            return value 

    # ------------------------------------------------------------------------- 
    # LED control
    # -------------------------------------------------------------------------

    def setPuzzleLedON(self):
        GPIO.output(LED_JUNGLE, GPIO.HIGH)
        GPIO.output(LED_PUZZLE, GPIO.LOW)

    def setJungleLedON(self):
        GPIO.output(LED_JUNGLE, GPIO.LOW)
        GPIO.output(LED_PUZZLE, GPIO.HIGH)
        
    def setRepeatLED(self, status):
        if status == 1:
            GPIO.output(LED_REPEAT, GPIO.LOW)
        elif status == 0:
            GPIO.output(LED_REPEAT, GPIO.HIGH)

    def setSkipLED(self, status):
        if status == 1:
            GPIO.output(LED_SKIP, GPIO.LOW)
        elif status == 0:
            GPIO.output(LED_SKIP, GPIO.HIGH)

    def mapvalue(self, x, inMin, inMax, outMin, outMax):
        return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin