#
# puzzleMode.py
#

from logger import log
import socket
import json
import threading

from CONST import *
from AudioPlay import AudioPlay 
from GameMode import GameMode


class Puzzle(GameMode):
    
    def __init__(self, net):
        GameMode.__init__(self)
        self.net = net
        self.levelNum = 0
        self.totalLevels = 1
        self.step = SPEAK_PUZZLE_MODE
        self.params = {
                    'data': []
        }
        self._importJSON();
        self._audio = AudioPlay(net)
        self.instructionsPlaying = False
        self._callbackDict = {
            'speakPuzzleModeCallback': self._speakPuzzleModeCallback,
            'speakLevelNumberCallback': self._speakLevelNumberCallback,
            'speakInstructionsCallback': self._speakInstructionsCallback,
            'failureCallback': self._failureCallback,
            'successCallback': self._successCallback,
        }

    def _importJSON(self):
        jsonFile = open('/home/pi/Documents/ovaom/python/assets/puzzle.json', 'r')
        fileAsString = jsonFile.read()
        self.puzzleData = json.loads(fileAsString)
        self.totalLevels = len(self.puzzleData)

# ================================================================================
#   Public
# ================================================================================

    def run(self, data):
        GameMode.killOfflineObjects(self, data)
        self._callbackListen(data)
        if self.step == SPEAK_PUZZLE_MODE:
            self._speakPuzzleMode()
        if self.step == SPEAK_LEVEL_NUMBER:
            self._speakLevelNumber()
        if self.step == SPEAK_INSTRUCTIONS:            
            self._speakInstructions()
        if self.step == PLAY_LEVEL:
            self._playLevel(data)

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

    def _callbackListen(self, data):
        if data and 'callback' in data[0]:
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
            log.info( 'Puzzle numero ' + str(self.levelNum + 1) )
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
            log.info( 'ecoute le modele' )
            path = ASSETS_FOLDER + 'audio/a_toi_de_jouer.wav'
            threading.Thread(
                target=self._audio.playback, 
                args=(path, 'speakInstructionsCallback',)).start()
    
    def _speakInstructionsCallback(self):
        self.step = PLAY_LEVEL
        self._audio.instructionsPlaying = False

    def _playLevel(self, data):
        if not data:
            return
        if 'params' in data[0]:
            log.debug(data)
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
        self.incrementLevel()
        self.step = SPEAK_LEVEL_NUMBER
        self._audio.instructionsPlaying = False
