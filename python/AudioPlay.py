
import threading
import time
import pygame 

ASSETS_FOLDER = "/home/pi/Documents/ovaom/python/assets"

class AudioPlay(object):

    def __init__(self, net):
        pygame.mixer.init()
        self.net = net
        self.instructionsPlaying = False
        self.interrupt = False

    def isBusy(self):
        return pygame.mixer.get_busy()

    def playback(self, path, callback):
        self.net.sendDspOFF()
        self.sound = pygame.mixer.Sound(path)
        pygame.mixer.Channel(0).play(self.sound)
        while self.isBusy():
            time.sleep(0.05)
            if self.interrupt:
                self.interrupt = False
                return
        print "finshed playing"
        self.net.sendDspON()
        callback()

    def stop(self):
        if self.isBusy():
            # self.sound.stop()
            pygame.mixer.Channel(0).stop()
            self.interrupt = True
            self.instructionsPlaying = False

class Sample(object):
    def __init__(self, *args):
        self.net.sendDspOFF()
        self.sound = pygame.mixer.Sound(path)
    
    def start(self):
        pygame.mixer.Channel(0).play(self.sound)
        while self.isBusy():
            time.sleep(0.05)
            if self.interrupt:
                self.interrupt = False
                return
        print "finshed playing"
        self.net.sendDspON()
        callback()
    