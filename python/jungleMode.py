# 
# jungleMode.py
# 

import logging
import time
import socket

class Jungle(object):

    def __init__(self, net):
        self.net = net
        self._instrument = [ {"active": 0, "maxPreset": 5, "currentPreset": 0} for i in range(0, 4) ]
        self._msg = net.oscMessage("play")

    def run(self):        
        try:
            data = self.net.receiveOsc()
            logging.debug(data)
        except socket.error:
            pass
        else:
            if "params" in data[0]:
                self.net.sendParams(data, self._instrument)
            elif "state" in data[0]:
                self.net.sendState(data, self._instrument)
            elif "presetChange" in data[0] :
                objId = int(data[0][8])
                self._instrument[objId]["currentPreset"] = (self._instrument[objId]["currentPreset"] + 1) % self._instrument[objId]["maxPreset"]
                logging.debug("Preset is now " + str(self._instrument[objId]["currentPreset"]))
            elif "battery" in data[0]:
                localtime = time.asctime(time.localtime(time.time()))
                logging.debug(localtime + " : battery: " + str(data[2]) + "%")
               