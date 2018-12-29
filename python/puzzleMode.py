#
# puzzleMode.py
#

import time
import socket
import json
import threading

from logger import log
from CONST import *
from AudioPlay import AudioPlay 
from GameMode import GameMode
import game_data

class Puzzle(GameMode):
    
    def __init__(self, net, gpio):
        GameMode.__init__(self, net)
        self.gpio = gpio
        self.levelNum = 0
        self.totalLevels = 1
        self.step = SPEAK_PUZZLE_MODE
        self.params = {
                    'data': []
        }
        self._importJSON();
        
        self._callbackDict = {
            'speakPuzzleModeCallback': self._speakPuzzleModeCallback,
            'speakLevelNumberCallback': self._speakLevelNumberCallback,
            'speakListenExampleCallback': self._speakListenExampleCallback,
            'speakInstructionsCallback': self._speakInstructionsCallback,
            'failureCallback': self._failureCallback,
            'successCallback': self._successCallback,
        }

    def _importJSON(self):
        jsonFile = open('/home/pi/Documents/ovaom/python/assets/puzzle.json', 'r')
        fileAsString = jsonFile.read()
        # self.puzzleData = json.loads(fileAsString)
        self.puzzleData = game_data.data
        self.totalLevels = len(self.puzzleData)
        self.audioPaths = game_data.paths

# ================================================================================
#   Public
# ================================================================================

    def run(self, data):
        GameMode.run(self, data)
        self._callbackListen(data)
        if self.step == SPEAK_PUZZLE_MODE:
            self._speakPuzzleMode()
        if self.step == SPEAK_LEVEL_NUMBER:
            self._speakLevelNumber()
        if self.step == SPEAK_LISTEN_EXAMPLE:            
            self._speakListenExample()
        if self.step == EMULATE_INSTRUMENT:
            self._emulateInstrument(data)
        if self.step == SPEAK_INSTRUCTIONS:
            self._speakInstructions()
        if self.step == PLAY_LEVEL:
            self._playLevel(data)
        if self.step == WAIT_USER_INPUT:
            self._waitUserInput()

    def setStep(self, step):
        self.step = step
    
    def incrementLevel(self):
        self.levelNum = (self.levelNum + 1) % self.totalLevels
        self.step = SPEAK_LEVEL_NUMBER

    def stopAudio(self):
        self._audio.stop()

    def reset(self):
        self.step = SPEAK_PUZZLE_MODE
        self.levelNum = 0

# ================================================================================
# ================================================================================
#   Private


    def _callbackListen(self, data):
        if data and 'callback' in data[0]:
            try:
                self._callbackDict[data[2]]()
            except:
                pass

    
# ================================================================================
#   Game states :
# ================================================================================

    def _speakPuzzleMode(self):
        if not self._audio.instructionsPlaying:
            self._audio.instructionsPlaying = True
            self.net.sendAllObjectsIdle()
            log.info( '*** PUZZLE MODE ***' )
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
            self.net.sendAllObjectsIdle()
            self.gpio.blinkLED(False)
            log.info( 'Puzzle numero ' + str(self.levelNum + 1) )
            path = ASSETS_FOLDER + 'audio/puzzleNum/' + str(self.levelNum + 1) + '.wav'
            threading.Thread(
                target=self._audio.playback, 
                args=(path, 'speakLevelNumberCallback',)).start()

    def _speakLevelNumberCallback(self):
        self.step = SPEAK_LISTEN_EXAMPLE
        self._audio.instructionsPlaying = False

    def _speakListenExample(self):
        if not self._audio.instructionsPlaying:
            self._audio.instructionsPlaying = True
            self.net.sendAllObjectsIdle()
            log.info( '-- speak: Ecoute le modele' )
            path = ASSETS_FOLDER + 'audio/ecoute_le_modele.wav'
            threading.Thread(
                target=self._audio.playback, 
                args=(path, 'speakListenExampleCallback',)).start()
    
    def _speakListenExampleCallback(self):
        self.step = EMULATE_INSTRUMENT
        self._audio.instructionsPlaying = False

    def _emulateInstrument(self, data):
        # if data and 'state' in data[0]:
        #     objId = int(data[0][8])
        #     GameMode.instrument[objId]["active"] = data[2]
        if not self._audio.instructionsPlaying:
            self._audio.instructionsPlaying = True
            self.gpio.setRepeatLED(ON)
            self.net.sendAllObjectsIdle()
            self._startTime = time.time()
            log.info( '-- audio: play model :D ' )
            output = []
            answer = self.puzzleData[self.levelNum]
            output.append(answer[0]['objectId'])
            output.append(1) # state = active
            output.append(0) # preset = 0
            for i in range(len(answer[0]['values'])):
                output.append(answer[0]['values'][i])
            self.net.sendEmulatedParams(output)
        if self._startTime and (time.time() - self._startTime) > 7:
            log.debug('finished playing')
            self._startTime = None
            self.step = SPEAK_INSTRUCTIONS
            self.gpio.setRepeatLED(OFF)
            self._audio.instructionsPlaying = False

    def _speakInstructions(self):
        if not self._audio.instructionsPlaying:
            self._audio.instructionsPlaying = True
            self.net.sendAllObjectsIdle()
            log.info( '-- speak: Instructions audio! ' )
            path = self.audioPaths[self.levelNum]
            threading.Thread(
                target=self._audio.playback, 
                args=(path, 'speakInstructionsCallback',)).start()
    
    def _speakInstructionsCallback(self):
        self.step = PLAY_LEVEL
        self._audio.instructionsPlaying = False
        # Last callback, update all objects state:
        self.net.sendAllObjectStates(GameMode.instrument)

    def _playLevel(self, data):
        if not data:
            return
        if 'params' in data[0]:
            self.net.sendParams(data, GameMode.instrument)
            self.params = {
                'objectId': int(data[0][8]),
                'data': data[2:]
            }
        elif 'state' in data[0]:
            objId = int(data[0][8])
            self.net.sendState(objId, GameMode.instrument[objId]["active"])
        elif 'presetChange' in data[0]:
            self._validateLevel()

# ================================================================================
#   Level validation
# ================================================================================

    def _validateLevel(self):
        fails = 0
        answer = self.puzzleData[self.levelNum]
        if answer[0]['objectId'] != self.params['objectId']:
            log.info('wrong object')
            self._failure()
            return
        if len(answer[0]['values']) != len(self.params['data']):
            log.info(('Validation Error: number of parameters does not match JSON file'))
            self._failure()
            return 
        for i in range(len(answer[0]['values'])):
            min = answer[0]['values'][i] - answer[0]['tolerance'][i]
            max = answer[0]['values'][i] + answer[0]['tolerance'][i]
            if min <= self.params['data'][i] <= max:
                log.info('param ' + str(i) + ' is ok!')
                pass
            else:
                log.info('fail: ' + str(self.params['data'][i]) + ' not between ' + str(min) + ' and ' + str(max))
                fails += 1
        if fails:
            self._failure()
        else:
            self._success()

    def _failure(self):
        log.info('FAIL: play failure audio')
        if not self._audio.instructionsPlaying:
            self._audio.instructionsPlaying = True
            log.info( 'ecoute le modele' )
            path = ASSETS_FOLDER + 'audio/failure.wav'
            threading.Thread(
                target=self._audio.playback, 
                args=(path, 'failureCallback',)).start()

    def _failureCallback(self):
        self.step = PLAY_LEVEL
        self._audio.instructionsPlaying = False

    def _success(self):
        log.info('SUCCESS: play success audio')
        if not self._audio.instructionsPlaying:
            self._audio.instructionsPlaying = True
            log.info( 'ecoute le modele' )
            path = ASSETS_FOLDER + 'audio/success.wav'
            threading.Thread(
                target=self._audio.playback, 
                args=(path, 'successCallback',)).start()

    def _successCallback(self):
        # self.incrementLevel()
        self.step = WAIT_USER_INPUT
        self._audio.instructionsPlaying = False

    def _waitUserInput(self):
        if not self._audio.instructionsPlaying:
            self._audio.instructionsPlaying = True
            log.info('-- sending allObjectsIdle, waiting for user input')
            self.net.sendAllObjectsIdle()
        self.gpio.blinkLED()
