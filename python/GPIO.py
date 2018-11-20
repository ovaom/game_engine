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

class InOut(object):
    # GPIO pins
    ledStartupPin = 5
    ledPuzzlePin = 27
    ledJunglePin = 10
    ledRepeatPin = 11
    ledSkipPin = 26

    btnPuzzlePin = 17
    btnJunglePin = 22
    btnRepeatPin = 9
    btnSkipPin = 13

    def __init__(self, game):
        self._initADC()
        self._initGPIO()
        self._readADC()
        self.volume = {
            "prev": 0,
            "curr": 0
        }
        self.prevRepeat = False
        self.prevSkip = False

    def _initADC(self):
        self.adc = Adafruit_ADS1x15.ADS1115()
        self.GAIN = 1
        print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
        print('-' * 37)
        
    def _initGPIO(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ledStartupPin,  GPIO.OUT)
        GPIO.setup(self.ledPuzzlePin,   GPIO.OUT)
        GPIO.setup(self.ledJunglePin,   GPIO.OUT)
        GPIO.setup(self.btnPuzzlePin,   GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.btnJunglePin,   GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.btnRepeatPin,   GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.btnSkipPin,     GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def _readADC(self):
        values = [0]*4
        for i in range(4):
            values[i] = self.adc.read_adc(i, gain=self.GAIN)
        print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))

    def readVolumeKnob(self):
        self.volume["curr"] = self.adc.read_adc(0, gain=self.GAIN)
        if abs(self.volume["curr"] - self.volume["prev"]) > 0:
            self.volume["prev"] = self.volume["curr"]
            return self.volume["curr"]

    def readGameMode(self):
        if GPIO.input(self.btnPuzzlePin):
            game["mode"] = "PUZZLE"
        elif GPIO.input(self.btnJunglePin):
            game["mode"] = "JUNGLE"

    def isRepeat(self):
        value = GPIO.input(self.btnRepeatPin)
        if value and value != self.prevRepeat:
            self.prevRepeat = value
            return value

    def isSkip(self):
        value = GPIO.input(self.btnSkipPin)
        if value and value != self.prevSkip:
            self.prevSkip = value
            return value        

    def setPuzzleModeLED(self):
        GPIO.output(self.ledJunglePin, GPIO.HIGH)
        GPIO.output(self.ledPuzzlePin, GPIO.LOW)

    def setJungleModeLED(self):
        GPIO.output(self.ledJunglePin, GPIO.LOW)
        GPIO.output(self.ledPuzzlePin, GPIO.HIGH)
        
    def setRepeatLED(self):
        GPIO.output(self.btnRepeatPin, GPIO.LOW)

    def setSkipLED(self):
        GPIO.output(self.btnSkipPin, GPIO.LOW)    