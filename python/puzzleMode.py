#
# puzzleMode.py
#

import socket
import json
from pydub import AudioSegment
from pydub.playback import play

class Puzzle(object):
    def __init__(self,):
        self.levelNum = 0
        self.totalLevels = 1
        self.step = "begin"
        self.params = {
                    "data": []
                }
        self._instrument = [ {"active": 0, "maxPreset": 5, "currentPreset": 0} for i in range(0, 4) ]
        self._importJSON();

    def _importJSON(self):
        print "importing json"
        jsonFile = open("/home/pi/Documents/ovaom/python/assets/puzzle.json", "r")
        fileAsString = jsonFile.read()
        self.puzzleData = json.loads(fileAsString)
        self.totalLevels = len(self.puzzleData)
        print "json imported"

    def run(self, net):
        if self.step == "begin":
            self._speakInstructions()
            self.step = "play"
        if self.step == "play":
            self._play(net)

    def _speakInstructions(self):
        print "------------------------------------------"
        print"Puzzle numero " + str(self.levelNum + 1)
        print"Ecoute dabord le modele"
        print" *modele* "
        print"A toi de jouer maintenant!"
        s1 = AudioSegment.from_file("assets/audio/" + str(self.levelNum + 1) + "/puzzle.mp3", format="mp3")
        s2 = AudioSegment.from_file("assets/audio/ecoute_le_modele.mp3", format="mp3")
        s3 = AudioSegment.from_file("assets/audio/a_toi_de_jouer.mp3", format="mp3")
        play(s1)
        play(s2)
        play(s3)

    def _play(self, net):
        try:
            data = net.receiveOsc()
        except socket.error:
            pass
        else:
            if "params" in data[0]:
                # print data[2]
                net.sendParams(data, self._instrument)
                self.params = {
                    "objectId": int(data[0][8]),
                    "data": data[2:]
                }
            elif "state" in data[0]:
                net.sendState(data, self._instrument)
            elif "presetChange" in data[0]:
                self._validateLevel()

    def _validateLevel(self):
        fails = 0
        answer = self.puzzleData[self.levelNum]
        if answer[0]["objectId"] != self.params["objectId"]:
            print("wrong object")
            self._failure()
            return
        if len(answer[0]["values"]) != len(self.params["data"]):
            print("Validation Error: number of parameters does not match JSON file")
            self._failure()
            return 
        for i in range(len(answer[0]["values"])):
            min = answer[0]["values"][i] - answer[0]["tolerance"][i]
            max = answer[0]["values"][i] + answer[0]["tolerance"][i]
            if min <= self.params["data"][i] <= max:
                print "param " + str(i) + " is ok!"
                pass
            else:
                print "fail: " + str(self.params["data"][i]) + " not between " + str(min) + " and " + str(max)
                fails += 1
        if fails:
            self._failure()
        else:
            self._success()
            
    def _failure(self):
        print "FAIL: play failure audio" 
        self.step = "begin"

    def _success(self):
        print "SUCCESS: play success audio" 
        self.levelNum = (self.levelNum + 1) % self.totalLevels
        self.step = "begin"
