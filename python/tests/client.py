import OSC
import time

# Init OSC
client = OSC.OSCClient()
client.connect(("192.168.4.1", 9002))
msg = OSC.OSCMessage()
msg.setAddress("/play")
print client

for i in range(30):
    time.sleep(1)

    msg.append(3) # objectID
    msg.append(0) # state
    # msg.append(0) # preset
    # msg.append(0) # param 1
    # msg.append(0)
    # msg.append(0)
    # msg.append(0)

    
    try:
        client.send(msg)
        msg.clearData();
    except Exception as e:
        print "Connection refused"
        print e
        msg.clearData();