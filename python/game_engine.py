# 
# game_engine.py
# 

import logging
import threading
import socket

from CONST import *
import network
import GPIO
import jungleMode
import puzzleMode
# import volume
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
            puzzle.setStep('SPEAK_INSTRUCTIONS')

    def skipClick(self, data):
        if game['mode'] == PUZZLE:
            GPIO.setSkipLED(data)
        if data:
            puzzle.stopAudio()
            puzzle.incrementLevel()

def getInputs():
    val1 = GPIO.getPuzzleButton()
    if val1 != None:
        Event('puzzleClick', val1)
    val2 = GPIO.getJungleButton()
    if val2 != None:
        Event('jungleClick', val2)
    val3 = GPIO.getRepeatButton()
    if val3 != None:
        Event('repeatClick', val3)
    val4 = GPIO.getSkipButton()
    if val4 != None:
        Event('skipClick', val4)

def getOscData():
    try:
        data = net.receiveOsc()
        logging.debug(data)
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
    logging.basicConfig(filename='/home/pi/Documents/ovaom/logs/game_engine.log', level=logging.DEBUG)
    logging.info('==========================================================')
    logging.info('Starting up')

    game = {'mode': JUNGLE,}    
    net = network.Network()
    GPIO = GPIO.InOut(game)
    # v = volume.VolumeCtrl(GPIO)
    jungle = jungleMode.Jungle(net)
    puzzle = puzzleMode.Puzzle(net)
    # # threading.Thread(target=v.mainVolume_RW).start()

    btn = Button()
    btn.observe('puzzleClick', btn.puzzleClick)
    btn.observe('jungleClick', btn.jungleClick)
    btn.observe('repeatClick', btn.repeatClick)
    btn.observe('skipClick', btn.skipClick)

    Event('jungleClick', 0)

    while True:
        getInputs()
        oscData = getOscData()
        updateGame(oscData)

