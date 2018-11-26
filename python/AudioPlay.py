
import threading
import time
import pygame 

ASSETS_FOLDER = "/home/pi/Documents/ovaom/python/assets"

class AudioPlay(object):
    
    def __init__(self):
        pygame.mixer.init()

    def isBusy(self):
        return pygame.mixer.get_busy()

    def playback(self, path):
        self.sound = pygame.mixer.Sound(path)
        self.sound.play()
        print "play"

    def stop(self):
        self.sound.stop()

# def test():
#     pygame.mixer.init()
#     sound = pygame.mixer.Sound("/home/pi/piano2.wav")
#     sound.play()
#     print "play"
#     while pygame.mixer.get_busy():
#         pass
#     sound.stop()
#     print "stop"