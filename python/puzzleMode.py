#
# puzzleMode.py
#

import socket
import json
from pydub import AudioSegment
from pydub.playback import play
from AudioPlay import AudioPlay

ASSETS_FOLDER = "/home/pi/Documents/ovaom/python/assets"

# Steps
START           = 0
INSTRUCTIONS    = 1
PLAYLEVEL       = 2

class Puzzle(object):
    
    def __init__(self, net, gpio):
        self.net = net
        self.gpio = gpio
        self.levelNum = 0
        self.totalLevels = 1
        self.step = START
        self.params = {
                    "data": []
        }
        self._instrument = [ {"active": 0, "maxPreset": 5, "currentPreset": 0} for i in range(0, 4) ]
        self._importJSON();
        self._audio = AudioPlay()

    def _importJSON(self):
        jsonFile = open("/home/pi/Documents/ovaom/python/assets/puzzle.json", "r")
        fileAsString = jsonFile.read()
        self.puzzleData = json.loads(fileAsString)
        self.totalLevels = len(self.puzzleData)

    def run(self):
        self.__getGPIO__()
        if self.step == START:
            self._playStart()
        if self.step == INSTRUCTIONS:            
            self._playInstructions()
        if self.step == PLAYLEVEL:
            self._playGame()

    def __getGPIO__(self):
        input = False
        if self.gpio.repeatButton():
            self.step = INSTRUCTIONS
            input = True
        if self.gpio.skipButton():
            self.levelNum = (self.levelNum + 1) % self.totalLevels
            self.step = START
            input = True
        return input


# *****************************************************************************
#   Game states : playStart, playInstructions, playGame :
# *****************************************************************************

    def _playStart(self):
        self.net.sendDspOFF()            
        print "------------------------------------------"
        print"Puzzle numero " + str(self.levelNum + 1)
        self._audio.playback(ASSETS_FOLDER + "/audio/" + str(self.levelNum + 1) + "/puzzle.wav")
        while self._audio.isBusy():
            if self.__getGPIO__():
                self._audio.stop()
                return
        self.net.sendDspON()
        self.step = INSTRUCTIONS
        self._playInstructions()

    def _playInstructions(self):
        self.net.sendDspOFF()
        self._audio.playback("/home/pi/Documents/ovaom/python/assets/audio/ecoute_le_modele.wav")
        while self._audio.isBusy():
            if self.__getGPIO__():
                self._audio.stop()
                return
        self._audio.playback("/home/pi/Documents/ovaom/python/assets/audio/a_toi_de_jouer.wav")
        while self._audio.isBusy():
            if self.__getGPIO__():
                self._audio.stop()
                return
        self.net.sendDspON()
        self.step = PLAYLEVEL
        self._playGame()

    def _playGame(self):
        try:
            data = self.net.receiveOsc()
        except socket.error:
            pass
        else:
            if "params" in data[0]:
                print data
                self.net.sendParams(data, self._instrument)
                self.params = {
                    "objectId": int(data[0][8]),
                    "data": data[2:]
                }
            elif "state" in data[0]:
                self.net.sendState(data, self._instrument)
            elif "presetChange" in data[0]:
                self._validateLevel()

# *****************************************************************************
#   Level validation
# *****************************************************************************

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
        self.step = PLAYLEVEL
        self._playGame()
        

    def _success(self):
        print "SUCCESS: play success audio" 
        self.levelNum = (self.levelNum + 1) % self.totalLevels
        self.step = START
        self._playStart()
