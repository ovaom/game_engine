# 
# game_engine.py
# 

import logging
import threading
import socket
import time
from subprocess import call

from CONST import *
import network
import GPIO
import jungleMode
import puzzleMode
import volume
from Observer import Observer, Event


class Button(Observer):
    def __init__(self):
        Observer.__init__(self)

    def puzzleClick(self, data):
        game['mode'] = PUZZLE
        GPIO.setPuzzleLedON()
        jungle.reset()
        jungle.stopAudio()

    def jungleClick(self, data):
        game['mode'] = JUNGLE
        GPIO.setJungleLedON()
        puzzle.reset()
        puzzle.stopAudio()

    def repeatClick(self, data):
        if game['mode'] == PUZZLE:
            GPIO.setRepeatLED(data)
        if data:
            puzzle.stopAudio()
            puzzle.setStep(SPEAK_LISTEN_EXAMPLE)

    def skipClick(self, data):
        if game['mode'] == PUZZLE:
            GPIO.setSkipLED(data)
        if data:
            puzzle.stopAudio()
            puzzle.incrementLevel()

    def changeDifficulty(self, data):
        puzzle.toggleDifficulty()

    def shutdown(self, data):
        GPIO.setStartupLed(OFF)
        call("sudo nohup shutdown -h now", shell=True)

    def resetWifi(self, data):
        log.debug('reset wifi')
        call("sudo ifconfig wlan0 down && sudo ifconfig wlan0 up", shell=True)

def getInputs():
    val1 = GPIO.getPuzzleButton()
    if val1 != None:
        Event('puzzleClick', val1)
    if val1 == LONG_PRESS:
        Event('shutdown', None)
    val2 = GPIO.getJungleButton()
    if val2 != None:
        Event('jungleClick', val2)
    if val2 == LONG_PRESS:
        Event('changeDifficulty', None)
    val3 = GPIO.getRepeatButton()
    if val3 != None:
        Event('repeatClick', val3)
    if val3 == LONG_PRESS:
        Event('resetWifi', None)
    val4 = GPIO.getSkipButton()
    if val4 != None:
        Event('skipClick', val4)

def getOscData():
    ''' Receive OSC data from objects and puredata and store it into a 'data'
    variable that is passed down '''
    try:
        data = net.receiveOsc()
        if not 'ping' in data[0] and not 'battery' in data[0] :
            log.debug('Incoming Data: %s', data)
    except socket.error as e:
        return None
    else:
        return data

def updateGame(oscData):
    if game['mode'] == JUNGLE:
        jungle.run(oscData)
    elif game['mode'] == PUZZLE:
        puzzle.run(oscData)

if __name__ == '__main__': 
    log = logging.getLogger('ovaom')
    logging.getLogger('Adafruit_I2C.Device.Bus.1.Address.0X48').setLevel(logging.WARNING)
    logging.basicConfig(filename='/home/pi/Documents/ovaom/logs/game_engine.log', level=logging.DEBUG)
    log.info('==========================================================')
    log.info('Starting up')
    
    game = {'mode': JUNGLE,}

    net = network.Network()
    GPIO = GPIO.InOut(game)

    v = volume.VolumeCtrl(GPIO)
    jungle = jungleMode.Jungle(net)
    puzzle = puzzleMode.Puzzle(net, GPIO)
    

    btn = Button()
    btn.observe('puzzleClick', btn.puzzleClick)
    btn.observe('jungleClick', btn.jungleClick)
    btn.observe('repeatClick', btn.repeatClick)
    btn.observe('skipClick', btn.skipClick)
    btn.observe('changeDifficulty', btn.changeDifficulty)
    btn.observe('shutdown', btn.shutdown)
    btn.observe('resetWifi', btn.resetWifi)
    

    Event('jungleClick', 0)

    while True:
        threading.Thread(target=v.mainVolume_RW).start()
        getInputs()
        oscData = getOscData()
        updateGame(oscData)

