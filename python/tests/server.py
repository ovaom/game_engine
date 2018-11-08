import socket
from OSC import decodeOSC

ip = '192.168.4.1'
port = 9001
buffer_size = 1024
do_loop = True

# Connect
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    my_socket.bind((ip, port))
    my_socket.setblocking(0)
    my_socket.settimeout(0.002)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer_size)
    print 'Plug : IP = ', ip,  'Port = ', port,  'Buffer Size =', buffer_size
except:
    print 'No connected'

# If connected
while do_loop:
    try:
        raw_data = my_socket.recv(buffer_size)
        data = decodeOSC(raw_data)
        print(data)
    except socket.error:
        pass