# 
# jungleMode.py
# 

from logger import log
import time
import socket
import threading

from CONST import *
from AudioPlay import AudioPlay
from GameMode import GameMode


class Jungle(GameMode):

    def __init__(self, net):
        GameMode.__init__(self)
        self.net = net
        self._msg = net.oscMessage('play')
        self._step = SPEAK_JUNGLE_MODE
        self._audio = AudioPlay(net)
        self.instructionsPlaying = False
        self._callbackDict = {
            'speakJungleModeCallback': self._speakJungleModeCallback,
        }

# ============================================================================
# Public
# ============================================================================

    def run(self, data=None):
        GameMode.killOfflineObjects(self, data)
        self._callbackListen(data)
        if self._step == SPEAK_JUNGLE_MODE:
            self._speakJungleMode()
        elif self._step == PLAY_JUNGLE_MODE:
            self._playJungleMode(data)

    def reset(self):
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
                log.debug(e)
                pass

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
            
    def _playJungleMode(self, data):
        if not data:
            return
        if 'params' in data[0]:
            self.net.sendParams(data, self._instrument)
        elif 'state' in data[0]:
            self.net.sendState(data, self._instrument)
        elif 'presetChange' in data[0] :
            objId = int(data[0][8])
            self._instrument[objId]['currentPreset'] = (self._instrument[objId]['currentPreset'] + 1) % self._instrument[objId]['maxPreset']
            log.debug('Preset is now ' + str(self._instrument[objId]['currentPreset']))
        # elif data and 'battery' in data[0]:
        #     localtime = time.asctime(time.localtime(time.time()))
        #     log.debug(localtime + ' : battery: ' + str(data[2]) + '%')

