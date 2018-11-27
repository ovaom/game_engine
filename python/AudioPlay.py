
import threading
import time
import pygame 

ASSETS_FOLDER = "/home/pi/Documents/ovaom/python/assets"

class AudioPlay(object):
    
    def __init__(self, net):
        pygame.mixer.init()
        self.net = net
        self.instructionsPlaying = False

    def isBusy(self):
        return pygame.mixer.get_busy()

    def playback(self, path):
        self.net.sendDspOFF()
        self.sound = pygame.mixer.Sound(path)
        self.sound.play()
        while self.isBusy():
            pass
        print "finshed playing"
        self.net.sendDspON()

    def stop(self):
        if self.isBusy():
            self.sound.stop()
            self.instructionsPlaying = False
