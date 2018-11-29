# 
# game_engine.py
# 

import network
import GPIO
import jungleMode
import puzzleMode
import volume
import threading
import time

class Observer():
    _observers = []
    def __init__(self):
        self._observers.append(self)
        self._observables = {}
    def observe(self, eventName, callback):
        self._observables[eventName] = callback

class Event():
    def __init__(self, name, data, autofire = True):
        self.name = name
        self.data = data
        if autofire:
            self.fire()
    def fire(self):
        for observer in Observer._observers:
            if self.name in observer._observables: 
                observer._observables[self.name](self.data)

class Button(Observer):
    def __init__(self):
        Observer.__init__(self)

    def puzzleClick(self, data):
        game["mode"] = "PUZZLE"
        GPIO.setPuzzleLedON()

    def jungleClick(self, data):
        game["mode"] = "JUNGLE"
        GPIO.setJungleLedON()

    def repeatClick(self, data):
        GPIO.setRepeatLED(data)
        if data:
            puzzle.stopAudio()
            puzzle.setStep("INSTRUCTIONS")

    def skipClick(self, data):
        GPIO.setSkipLED(data)
        if data:
            puzzle.stopAudio()
            puzzle.incrementLevel()
            puzzle.stopAudio()
        
def getInputs():
    val1 = GPIO.getPuzzleButton()
    if val1 != None:
        Event("puzzleClick", val1)
    val2 = GPIO.getJungleButton()
    if val2 != None:
        Event("jungleClick", val2)
    val3 = GPIO.getRepeatButton()
    if val3 != None:
        Event("repeatClick", val3)
    val4 = GPIO.getSkipButton()
    if val4 != None:
        Event("skipClick", val4)

def updateGame():
    if game["mode"] == "JUNGLE":
        jungle.run()
    elif game["mode"] == "PUZZLE":
        puzzle.run()

if __name__ == "__main__":   
    game = {"mode": "JUNGLE",}    
    net = network.Network()
    GPIO = GPIO.InOut(game)
    v = volume.VolumeCtrl(GPIO)
    jungle = jungleMode.Jungle(net)
    puzzle = puzzleMode.Puzzle(net, GPIO)
    # # threading.Thread(target=v.mainVolume_RW).start()

    btn = Button()
    btn.observe("puzzleClick", btn.puzzleClick)
    btn.observe("jungleClick", btn.jungleClick)
    btn.observe("repeatClick", btn.repeatClick)
    btn.observe("skipClick", btn.skipClick)

    while True:
        getInputs()
        updateGame()
