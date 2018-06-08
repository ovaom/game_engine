import socket
import OSC
import re

ip = '192.168.4.1'
inPort = 9001
buffer_size = 1024

soundObject = [ {"active": 0, "plateau": False, "maxPreset": 5, "currentPreset": 0} for i in range(0, 4) ]
objectOnBoard = [False, False, False, False]

def sendOsc(msg) :
    print "sending data: ", msg
    try:
        client.send(msg)
        msg.clearData();
    except Exception as e:
        print "Send Error"
        print "message not sent:", msg
        print e
        msg.clearData();

# Connect server
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    my_socket.bind((ip, inPort))
    my_socket.setblocking(0)
    my_socket.settimeout(0.002)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer_size)
    print 'Plug : IP = ', ip,  'inPort = ', inPort,  'Buffer Size =', buffer_size
except:
    print 'Not connected'

# Init OSC Client
client = OSC.OSCClient()
outPort = 9002
client.connect(("192.168.4.1", outPort))
print client

msg = OSC.OSCMessage()
msg.setAddress("/play")

#  Message format=> 0:objectID, 1:state, 2:preset 3:param1, 4:param2, n:paramN ...

# If connected
while True:
    try:
        raw_data = my_socket.recv(buffer_size)
        data = OSC.decodeOSC(raw_data)
        # print(data)
        
        if "plateau" in data[0] :
            k = 0
            for i in range(2,6):
                objectOnBoard[k] = data[i]
                k += 1
            print (objectOnBoard)

        elif "params" in data[0] :
            objId = int(data[0][8])
            msg.append(objId)
            msg.append(soundObject[objId]["active"])
            msg.append(soundObject[objId]["currentPreset"])
            for i in range(2, len(data)) :
                msg.append(data[i])
            sendOsc(msg)

        elif "presetChange" in data[0] :
            objId = int(data[0][8])
            soundObject[objId]["currentPreset"] = (soundObject[objId]["currentPreset"] + 1) % soundObject[objId]["maxPreset"]
            print ("Preset is now " + str(soundObject[objId]["currentPreset"]))

        elif "state" in data[0] :
            objId = int(data[0][8])
            if (objectOnBoard[objId]) :
                soundObject[objId]["active"] = 1
            else:
                soundObject[objId]["active"] = data[2]
            msg.append(objId)
            msg.append(soundObject[objId]["active"])
            sendOsc(msg)

    except socket.error:
        pass

