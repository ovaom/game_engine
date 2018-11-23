#
# puzzleMode.py
#

import socket
import json
from pydub import AudioSegment
from pydub.playback import play

ASSETS_FOLDER = "/home/pi/Documents/ovaom/python/assets"

class Puzzle(object):
    def __init__(self, gpio):
        self.gpio = gpio
        self.levelNum = 0
        self.totalLevels = 1
        self.step = "begin"
        self.params = {
                    "data": []
        }
        self._instrument = [ {"active": 0, "maxPreset": 5, "currentPreset": 0} for i in range(0, 4) ]
        self._importJSON();

    def _importJSON(self):
        jsonFile = open("/home/pi/Documents/ovaom/python/assets/puzzle.json", "r")
        fileAsString = jsonFile.read()
        self.puzzleData = json.loads(fileAsString)
        self.totalLevels = len(self.puzzleData)

    def run(self, net):
        self._readGpio()
        if self.step == "begin":
            net.sendDspOFF()            
            print "------------------------------------------"
            print"Puzzle numero " + str(self.levelNum + 1)
            play(AudioSegment.from_file(ASSETS_FOLDER + "/audio/" + str(self.levelNum + 1) + "/puzzle.mp3", format="mp3"))
            self.step = "instructions"
            net.sendDspON()
        if self.step == "instructions":
            net.sendDspOFF()
            play(AudioSegment.from_file(ASSETS_FOLDER + "/audio/ecoute_le_modele.mp3", format="mp3"))
            play(AudioSegment.from_file(ASSETS_FOLDER + "/audio/a_toi_de_jouer.mp3", format="mp3"))
            self.step = "play"
            net.sendDspON()
        if self.step == "play":
            self._play(net)

    def _readGpio(self):
        if self.gpio.repeatButton():
            self.step = "instructions"
        if self.gpio.skipButton():
            self.levelNum = (self.levelNum + 1) % self.totalLevels
            self.step = "begin"

    def _play(self, net):
        try:
            data = net.receiveOsc()
        except socket.error:
            pass
        else:
            if "params" in data[0]:
                print data
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
        self.step = "play"

    def _success(self):
        print "SUCCESS: play success audio" 
        self.levelNum = (self.levelNum + 1) % self.totalLevels
        self.step = "begin"
