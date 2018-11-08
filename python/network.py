# 
# network.py
# 

import socket
import OSC

# Message format=> 0:objectID, 1:state, 2:preset 3:param1, 4:param2, n:paramN ...

class Network(object):
    def __init__(self):
        self._connectServer()
        self._connectClient()
        self._msg = OSC.OSCMessage()
        self._msg.setAddress("/play")
                
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
            print ('Plug : IP = ', ip,  'inPort = ', inPort,  'Buffer Size =', self.buffer_size)
            return self.my_socket, self.buffer_size
        except:
            print ('Not connected')

    def _connectClient(self):
        # Init OSC Client
        self.client = OSC.OSCClient()
        outPort = 9002
        self.client.connect(("192.168.4.1", outPort))
        print (self.client)

    def receiveOsc(self):
        raw_data = self.my_socket.recv(self.buffer_size)
        return OSC.decodeOSC(raw_data)

    def OscMessage(self):
        msg = OSC.OSCMessage()
        msg.setAddress("/play")
        return (msg)

    def sendOsc(self, msg) :
        print ("sending data: ", msg)
        try:
            self.client.send(msg)
            msg.clearData();
        except Exception as e:
            print ("Send Error")
            print ("message not sent:", msg)
            print (e)
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

