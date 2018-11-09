#
# puzzleMode.py
#

import socket
import json
# from pydub import AudioSegment
# from pydub.playback import play

class Puzzle(object):
    def __init__(self,):
        self.levelNum = 1
        self.step = "begin"
        self.params = None
        self._instrument = [ {"active": 0, "maxPreset": 5, "currentPreset": 0} for i in range(0, 4) ]
        self._importJSON();

    def _importJSON(self):
        jsonFile = open("/home/pi/Documents/ovaom/python/assets/puzzle.json", "r")
        fileAsString = jsonFile.read()
        self.puzzleData = json.loads(fileAsString)
        print (self.puzzleData["1"][0]["values"])
        print self.puzzleData

    def run(self, net):
        if self.step == "begin":
            self._speakInstructions()
            self.step = "play"
        if self.step == "play":
            self._play(net)

    def _speakInstructions(self):
        print("play audio instructions for the level")
        print("puzzle numero x")
        print("ecoute le modele")
        print("modele")
        print("a toi de jouer")

    def _play(self, net):
        try:
            data = net.receiveOsc()
            print(data)
        except socket.error:
            pass
        else:
            if "params" in data[0]:
                net.sendParams(data, self._instrument)
                self.params = {
                    "objectId": int(data[0][8]),
                    "data": data[2:]
                }
            elif "state" in data[0]:
                net.sendState(data, self._instrument)
            elif "presetChange" in data[0] :
                print ("validation = check answer")                
                self._validateLvl()

    def _validateLvl(self):
        print (self.params)
        # print(values)

        if self.puzzleData[str(self.levelNum)][0]["objectId"] != self.params["objectId"]:
            print("wrong object")
        # if len(values) != len(self.puzzleData[str(self.levelNum)]["successConditions"][0]["values"]):
        #     print("Validation Error: number of parameters does not match JSON file")
            
            




        if self.params == 0:
            print ("play success audio")
            self.levelNum += 1
            self.step = "begin"
        else:
            print("play failure audio")
            self.step = "begin"


# class Level(object):
#     def __init__(self, level):
#         self.level = level 
#         #parse json file for variables
#         self.successCondition = 1;

#     def speakInstructions(self):
#         print("play audio instructions for the level")
#         print("puzzle numero x")
#         print("ecoute le modele")
#         print("modele")
#         print("a toi de jouer")




# Check the current level
# check if loading a new level is needed
# check if instructions have been spoken already 
# check user input and send to sound engine
# check user input and check for validation
# check for user success or failure
# if success, got to next level
# if failure, retry level
