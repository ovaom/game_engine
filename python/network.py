# 
# network.py
# 

import logging
import socket
import OSC
import time

# Message format=> 0:objectID, 1:state, 2:preset 3:param1, 4:param2, n:paramN ...

class Network(object):
    def __init__(self):
        self._connectServer()
        self._connectClient()
        self._connectWavClient()
        self._msg = OSC.OSCMessage()        
        self._mDspOn = OSC.OSCMessage()
        self._mDspOff = OSC.OSCMessage()
        self._msg.setAddress("/play")
        self._mDspOn.setAddress("/dspOn")
        self._mDspOff.setAddress("/dspOff")

    def _connectServer(self):    
        ip = '192.168.4.1'
        inPort = 9001
        self.buffer_size = 1024
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.my_socket.bind((ip, inPort))
            self.my_socket.setblocking(0)
            self.my_socket.settimeout(0.002)
            self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.buffer_size)
            logging.info("OSCServer : IP = %s inPort = %d Buffer Size = %d", ip, inPort, self.buffer_size)
        except Exception as e:
            logging.info("Server connection error:\n" + str(e))

    def _connectClient(self):
        # Init OSC Client
        self._client = OSC.OSCClient()
        outPort = 9002
        self._client.connect(("192.168.4.1", outPort))
        logging.info(self._client)

    def _connectWavClient(self):
        self._wavClient = OSC.OSCClient()
        outPort = 9003
        self._wavClient.connect(("192.168.4.1", outPort))
        logging.info(self._wavClient)

    def receiveOsc(self):
        raw_data = self.my_socket.recv(self.buffer_size)
        return OSC.decodeOSC(raw_data)

    def oscMessage(self, address):
        msg = OSC.OSCMessage()
        msg.setAddress("/play")
        return (msg)

    def sendOsc(self, msg) :
        # logging.debug("sending data: %s", msg)
        try:
            self._client.send(msg)
            msg.clearData();
        except Exception as e:
            # logging.debug("Send Error! message not sent:\n" + str(msg) + str(e))
            msg.clearData();
    
    def sendOscWavPlayback(self, msg):
        # logging.debug("sending wav playback data: %s", msg)
        try:
            self._wavClient.send(msg)
            msg.clearData();
        except Exception as e:
            # logging.debug("Send Error! message not sent:\n" + str(msg) + str(e))
            msg.clearData();  
                 
    def sendParams(self, data, instrument):
        objId = int(data[0][8])
        self._msg.append(objId)
        self._msg.append(instrument[objId]["active"])
        self._msg.append(instrument[objId]["currentPreset"])
        for i in range(2, len(data)) :
            self._msg.append(data[i])
        self.sendOsc(self._msg)

    def sendState(self, data, instrument):
        objId = int(data[0][8])
        instrument[objId]["active"] = data[2]
        self._msg.append(objId)
        self._msg.append(instrument[objId]["active"])
        self.sendOsc(self._msg)

    def sendObjectNotConnected(self, objectId):
        self._msg.append(objectId)
        self._msg.append(0) # 0 = object is inactive
        self.sendOsc(self._msg)
