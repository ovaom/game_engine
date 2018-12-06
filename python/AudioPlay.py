
import logging
import threading
import time
import pygame
import sys

ASSETS_FOLDER = "/home/pi/Documents/ovaom/python/assets"

class AudioPlay(object):

    def __init__(self, net):
        self.net = net
        self.instructionsPlaying = False
        self.interrupt = False

    def isBusy(self):
        return pygame.mixer.get_busy()

    # Version 1 :
    def playback(self, path, callback):    
        logging.debug("dspOFF send")
        self.net.sendDspOFF()
        logging.debug("pygame mixer init")     
        pygame.mixer.init()
        logging.debug("load sound")
        self.sound = pygame.mixer.Sound(path)
        logging.debug("play sound")
        pygame.mixer.Channel(0).play(self.sound)
        while self.isBusy():
            # time.sleep(0.01)
            if self.interrupt:
                self.interrupt = False
                return
        time.sleep(0.5)
        logging.debug("finshed playing")
        pygame.mixer.quit()
        logging.debug("pygame mixer closed")
        self.net.sendDspON()
        logging.debug("sent dspON")
        callback()

    def stop(self):
        if self.isBusy():
            # self.sound.stop()
            pygame.mixer.Channel(0).stop()
            self.interrupt = True
            self.instructionsPlaying = False


# ============================================================================
# PureData Version
# ============================================================================


# class AudioPlay(object):
#     def __init__(self, net):
#         self.net = net
#         self.msg = net.oscMessage("/instructions")
#         self.instructionsPlaying = False

#     def isBusy(self):
#         return pygame.mixer.get_busy()

#     def playback(self, path, callback):
#         self.msg.append(path)
#         self.msg.append(callback)
#         self.net.sendOsc(self.msg)

#     def stop(self):
#         self.instructionsPlaying = False   