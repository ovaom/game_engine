#
# puzzleMode.py
#

import socket
import json

class Puzzle(object):
    def __init__(self,):
        self.levelNum = 0
        self.step = "begin"
        self.params = None
        self._instrument = [ {"active": 0, "maxPreset": 5, "currentPreset": 0} for i in range(0, 4) ]

    def run(self, net):
        if self.step == "begin":
            currentLevel = Level(self.levelNum)
            currentLevel.speakInstructions()
            self.step = "play"
        if self.step == "play":
            self.play(net)


    def play(self, net):
        try:
            data = net.receiveOsc()
            # print(data)
        except socket.error:
            pass
        else:
            if "params" in data[0]:
                net.sendParams(data, self._instrument)
                self.params = data
            elif "state" in data[0]:
                net.sendState(data, self._instrument)
            elif "presetChange" in data[0] :
                print ("validation = check answer")
                validateLvl()

    def validateLvl(self):
        if self.params == currentLevel.successCondition:
            print ("play success audio")
            self.levelNum += 1
            self.step = "begin"
        else:
            print("play failure audio")
            self.step = "begin"


class Level(object):
    def __init__(self, level):
        self.level = level 
        #parse json file for variables
        self.successCondition = 1;

    def speakInstructions(self):
        print("play audio instructions for the level")
        print("puzzle numero x")
        print("ecoute le modele")
        print("modele")
        print("a toi de jouer")




# Check the current level
# check if loading a new level is needed
# check if instructions have been spoken already 
# check user input and send to sound engine
# check user input and check for validation
# check for user success or failure
# if success, got to next level
# if failure, retry level
