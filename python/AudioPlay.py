
import logging

class AudioPlay(object):
    def __init__(self, net):
        self.net = net
        self.msg = net.oscMessage("/instructions")
        self.instructionsPlaying = False

    def playback(self, path, callback):
        self.msg.append(path)
        self.msg.append(callback)
        self.net.sendOscWavPlayback(self.msg)

    def stop(self):
        self.instructionsPlaying = False
