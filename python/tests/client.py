import OSC
import time

# Init OSC
client = OSC.OSCClient()
client.connect(("192.168.4.1", 9001))
msg = OSC.OSCMessage()
msg.setAddress("/callback")
print client

for i in range(30):
    time.sleep(1)
    msg.append("wrongCallback")
    try:
        client.send(msg)
        msg.clearData();
    except Exception as e:
        print "Connection refused"
        print e