import time
import Adafruit_ADS1x15
import RPi.GPIO as GPIO
from logger import log
from CONST import *

# GPIO Pin definitions
LED_STARTUP = 26
LED_PUZZLE = 10 
LED_JUNGLE = 27
LED_REPEAT = 11
LED_SKIP = 13

BTN_PUZZLE = 22
BTN_JUNGLE = 17
BTN_REPEAT = 9
BTN_SKIP = 5


class InOut(object):
    
    __instance = None
    
    def __init__(self, game):
        self._initADC()
        self._initGPIO()
        self._readADC()
        # self._test()
        self.volume = {
            "prev": 0,
            "curr": 0
        }
        self.jungle_press_time = 0
        self.prevJungle = 0
        self.prevRepeat = 0
        self.prevSkip = 0
        self._prevLedBlink = 0
        self._LEDState = OFF

    def _initADC(self):
        if InOut.__instance != None:
            raise Exception("This class is a singleton")
        else:
            InOut.__instance = self
        log.info("Starting ADC")
        self.adc = Adafruit_ADS1x15.ADS1115()
        self.GAIN = 1
        # log.debug('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
        # log.debug('-' * 37)
        
    def _initGPIO(self):
        log.info('GPIO setup')
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
        log.debug('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))

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
            value = self.mapvalue(self.volume["curr"], 0, 26400, 0, 100)
            value = int(19.94 * value ** 0.358)
            if value > 100:
                value = 100
            return value

    def getPuzzleButton(self):
        if GPIO.input(BTN_PUZZLE):
            return True

    def getJungleButton(self):
        value = GPIO.input(BTN_JUNGLE)
        if value != self.prevJungle:
            self.jungle_press_time = time.time()
            self.prevJungle = value
            return value
        elif value and value == self.prevJungle:
            if (time.time() - self.jungle_press_time) > LONG_PRESS_TIME:
                self.jungle_press_time = time.time()
                return LONG_PRESS        

    def getRepeatButton(self):
        value = GPIO.input(BTN_REPEAT)
        if value != self.prevRepeat:
            self.prevRepeat = value
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

    def blinkLED(self, start=True):
        if start == False:
            self.setRepeatLED(OFF)
            self.setSkipLED(OFF)
            self._LEDState = OFF
            return
        now = time.time()
        if now - self._prevLedBlink > 0.3:
            if self._LEDState == ON:
                self._LEDState = OFF;
            else:
                self._LEDState = ON
            self.setRepeatLED(self._LEDState)
            self.setSkipLED(self._LEDState)
            self._prevLedBlink = now

    def mapvalue(self, x, inMin, inMax, outMin, outMax):
        return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin