#
# puzzleMode.py
#

import logging
import socket
import json
import threading
from AudioPlay import AudioPlay 
from CONST import *

class Puzzle(object):
    
    def __init__(self, net, gpio):
        self.net = net
        self.gpio = gpio
        self.levelNum = 0
        self.totalLevels = 1
        self.step = SPEAK_PUZZLE_MODE
        self.params = {
                    'data': []
        }
        self._instrument = [ {'active': 0, 'maxPreset': 5, 'currentPreset': 0} for i in range(0, 4) ]
        self._importJSON();
        self._audio = AudioPlay(net)
        self.instructionsPlaying = False
        self._callbackDict = {
            'speakPuzzleModeCallback': self._speakPuzzleModeCallback,
            'speakLevelNumberCallback': self._speakLevelNumberCallback,
            'speakInstructionsCallback': self._speakInstructionsCallback,
        }

    def _importJSON(self):
        jsonFile = open('/home/pi/Documents/ovaom/python/assets/puzzle.json', 'r')
        fileAsString = jsonFile.read()
        self.puzzleData = json.loads(fileAsString)
        self.totalLevels = len(self.puzzleData)

# ================================================================================
#   Public
# ================================================================================

    def run(self):
        # if self.step != PLAY_LEVEL:
        self._callbackListen()
        if self.step == SPEAK_PUZZLE_MODE:
            self._speakPuzzleMode()
        if self.step == SPEAK_LEVEL_NUMBER:
            self._speakLevelNumber()
        if self.step == SPEAK_INSTRUCTIONS:            
            self._speakInstructions()
        if self.step == PLAY_LEVEL:
            self._playLevel()

    def setStep(self, step):
        if step == 'SPEAK_PUZZLE_MODE':
            self.step = SPEAK_LEVEL_NUMBER
        if step == 'SPEAK_LEVEL_NUMBER':
            self.step = SPEAK_LEVEL_NUMBER
        if step == 'SPEAK_INSTRUCTIONS':
            self.step = SPEAK_INSTRUCTIONS
        if step == 'PLAY_LEVEL':
            self.step = PLAY_LEVEL
    
    def incrementLevel(self):
        self.levelNum = (self.levelNum + 1) % self.totalLevels
        self.step = SPEAK_LEVEL_NUMBER

    def stopAudio(self):
        self._audio.stop()

    def reset(self):
        self.step = SPEAK_PUZZLE_MODE
        self.levelNum = 0

# ================================================================================
#   Private
# ================================================================================

    def _callbackListen(self):
        try:
            data = self.net.receiveOsc()
            logging.debug(data)
        except socket.error as e:
            pass 
        else:
            if 'callback' in data[0]:
                try:
                    self._callbackDict[data[2]]()
                except:
                    pass

# ================================================================================
#   Game states : playStart, playInstructions, playGame :
# ================================================================================

    def _speakPuzzleMode(self):
        if not self._audio.instructionsPlaying:
            self._audio.instructionsPlaying = True
            logging.info( '*** PUZZLE MODE ***' )
            path = ASSETS_FOLDER + 'audio/puzzle_mode.wav'
            threading.Thread(
                target=self._audio.playback, 
                args=(path, 'speakPuzzleModeCallback',)).start()
    
    def _speakPuzzleModeCallback(self):
        self.step = SPEAK_LEVEL_NUMBER
        self._audio.instructionsPlaying = False
    
    def _speakLevelNumber(self):
        if not self._audio.instructionsPlaying:
            self._audio.instructionsPlaying = True
            logging.info( 'Puzzle numero ' + str(self.levelNum + 1) )
            path = ASSETS_FOLDER + 'audio/' + str(self.levelNum + 1) + '/puzzle.wav'
            threading.Thread(
                target=self._audio.playback, 
                args=(path, 'speakLevelNumberCallback',)).start()

    def _speakLevelNumberCallback(self):
        self.step = SPEAK_INSTRUCTIONS
        self._audio.instructionsPlaying = False

    def _speakInstructions(self):
        if not self._audio.instructionsPlaying:
            self._audio.instructionsPlaying = True
            logging.info( 'ecoute le modele' )
            path = ASSETS_FOLDER + 'audio/a_toi_de_jouer.wav'
            threading.Thread(
                target=self._audio.playback, 
                args=(path, 'speakInstructionsCallback',)).start()
    
    def _speakInstructionsCallback(self):
        self.step = PLAY_LEVEL
        self._audio.instructionsPlaying = False

    def _playLevel(self):
        try:
            data = self.net.receiveOsc()
        except socket.error:
            pass
        else:
            if 'params' in data[0]:
                logging.debug(data)
                self.net.sendParams(data, self._instrument)
                self.params = {
                    'objectId': int(data[0][8]),
                    'data': data[2:]
                }
            elif 'state' in data[0]:
                self.net.sendState(data, self._instrument)
            elif 'presetChange' in data[0]:
                self._validateLevel()

# ================================================================================
#   Level validation
# ================================================================================

    def _validateLevel(self):
        fails = 0
        answer = self.puzzleData[self.levelNum]
        if answer[0]['objectId'] != self.params['objectId']:
            logging.info('wrong object')
            self._failure()
            return
        if len(answer[0]['values']) != len(self.params['data']):
            logging.info(('Validation Error: number of parameters does not match JSON file'))
            self._failure()
            return 
        for i in range(len(answer[0]['values'])):
            min = answer[0]['values'][i] - answer[0]['tolerance'][i]
            max = answer[0]['values'][i] + answer[0]['tolerance'][i]
            if min <= self.params['data'][i] <= max:
                logging.info('param ' + str(i) + ' is ok!')
                pass
            else:
                logging.info('fail: ' + str(self.params['data'][i]) + ' not between ' + str(min) + ' and ' + str(max))
                fails += 1
        if fails:
            self._failure()
        else:
            self._success()
            
    def _failure(self):
        logging.info('FAIL: play failure audio')
        self.step = PLAY_LEVEL
        self._playLevel()

    def _success(self):
        logging.info('SUCCESS: play success audio')
        self.incrementLevel()
        self._speak_intructions()


