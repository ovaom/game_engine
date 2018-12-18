
import time
from logger import log

class AudioPlay(object):
    def __init__(self, net):
        self.net = net
        self.msg = net.oscMessage("/instructions")
        self.instructionsPlaying = False

    def playback(self, path, callbackName):
        self.msg.append(path)
        self.msg.append(callbackName)
        self.net.sendOscWavPlayback(self.msg)

    def stop(self):
        self.instructionsPlaying = False
