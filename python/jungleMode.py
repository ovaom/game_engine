# 
# jungleMode.py
# 

import logging
import time
import socket
import threading
from AudioPlay import AudioPlay
from CONST import *

# SPEAK_JUNGLE_MODE = 0
# PLAY_JUNGLE_MODE = 1

class Jungle(object):

    def __init__(self, net):
        self.net = net
        self._instrument = [ {"active": 0, "maxPreset": 5, "currentPreset": 0} for i in range(0, 4) ]
        self._msg = net.oscMessage("play")
        self._step = SPEAK_JUNGLE_MODE
        self._audio = AudioPlay(net)
        self.instructionsPlaying = False
        self._callbackDict = {
            'speakJungleModeCallback': self._speakJungleModeCallback,
        }

# ============================================================================
# Public
# ============================================================================

    def run(self):
        # logging.debug('step is: %d', self._step)
        self._callbackListen()
        if self._step == SPEAK_JUNGLE_MODE:
            # logging.debug('speak+jungle_mode')
            self._speakJungleMode()
        elif self._step == PLAY_JUNGLE_MODE:
            # logging.debug('play_jungle_mode')
            self._playJungleMode()

    def reset(self):
        self._step = SPEAK_JUNGLE_MODE

    def stopAudio(self):
        self._audio.stop()

# ============================================================================
# Private
# ============================================================================

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
                except Exception as e:
                    logging.debug(e)
                    pass

    def _speakJungleMode(self):
        if not self._audio.instructionsPlaying:
            self._audio.instructionsPlaying = True
            logging.info( '*** JUNGLE MODE ***' )
            path = ASSETS_FOLDER + 'audio/jungle_mode.wav'
            threading.Thread(
                target=self._audio.playback, 
                args=(path, 'speakJungleModeCallback',)).start()

    def _speakJungleModeCallback(self):
        self._step = PLAY_JUNGLE_MODE
        self._audio.instructionsPlaying = False
            
    def _playJungleMode(self):
        try:
            data = self.net.receiveOsc()
            logging.debug(data)
        except socket.error:
            pass
        else:
            if "params" in data[0]:
                self.net.sendParams(data, self._instrument)
            elif "state" in data[0]:
                self.net.sendState(data, self._instrument)
            elif "presetChange" in data[0] :
                objId = int(data[0][8])
                self._instrument[objId]["currentPreset"] = (self._instrument[objId]["currentPreset"] + 1) % self._instrument[objId]["maxPreset"]
                logging.debug("Preset is now " + str(self._instrument[objId]["currentPreset"]))
            elif "battery" in data[0]:
                localtime = time.asctime(time.localtime(time.time()))
                logging.debug(localtime + " : battery: " + str(data[2]) + "%")
               