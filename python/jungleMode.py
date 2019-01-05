# 
# jungleMode.py
# 

import time
import threading

from logger import log
from CONST import *
from AudioPlay import AudioPlay
from GameMode import GameMode


class Jungle(GameMode):

    def __init__(self, net):
        GameMode.__init__(self, net)
        self._msg = net.oscMessage('play')
        self._step = SPEAK_JUNGLE_MODE
        self._audio = AudioPlay(net)
        self._callbackDict = {
            'speakJungleModeCallback': self._speakJungleModeCallback,
        }

# ============================================================================
# Public
# ============================================================================

    def run(self, data=None):
        GameMode.run(self, data)
        self._callbackListen(data)
        if self._step == SPEAK_JUNGLE_MODE:
            self._speakJungleMode()
        elif self._step == PLAY_JUNGLE_MODE:
            self._playJungleMode(data)

    def reset(self):
        for i in GameMode.instrument:
            i['currentPreset'] = 0
        self._step = SPEAK_JUNGLE_MODE

    def stopAudio(self):
        self._audio.stop()

# ============================================================================
# Private
# ============================================================================

    def _callbackListen(self, data):
        if data and 'callback' in data[0]:
            try:
                self._callbackDict[data[2]]()
            except Exception as e:
                log.error(e)

    def _speakJungleMode(self):
        if not self._audio.instructionsPlaying:
            self._audio.instructionsPlaying = True
            log.info( '*** JUNGLE MODE ***' )
            path = ASSETS_FOLDER + 'audio/jungle_mode.wav'
            threading.Thread(
                target=self._audio.playback, 
                args=(path, 'speakJungleModeCallback',)).start()

    def _speakJungleModeCallback(self):
        self._step = PLAY_JUNGLE_MODE
        self._audio.instructionsPlaying = False
        ### Last callback, update all objects state:
        log.info('Last callback, sending all objects states: ')
        self.net.sendAllObjectStates(GameMode.instrument)
            
    def _playJungleMode(self, data):
        if not data:
            return
        
        elif 'state' in data[0]:
            objId = int(data[0][8])
            self.net.sendState(objId, GameMode.instrument[objId]["active"])
        if 'presetChange' in data[0]:
            objId = int(data[0][8])
            newPreset = GameMode.instrument[objId]['currentPreset'] + 1
            maxPreset = GameMode.instrument[objId]['maxPreset']
            preset = GameMode.instrument[objId]['currentPreset'] = newPreset % maxPreset
            log.debug('Preset is now ' + str(preset))
            self.net.sendPreset(objId, preset)
        elif 'params' in data[0]:
            self.net.sendParams(data, GameMode.instrument)
