#!/usr/bin/python           # This is client.py file

import socket  # Import socket module

s = socket.socket()  # Create a socket object
host = socket.gethostname()  # Get local machine name

s.connect(("localhost", 8765))

print "Client: Connect Sucessful"
print s.recv(1024)
# f = open("cmmd.txt", 'r')
# for line in f:
#     if not line.startswith("END"):
#         s.send(line)
#     else:
#         re = s.recv(1024)
#         print re
# f.close()
f = open('garrido-sm.jpg', 'rb')
data = f.read()
f.close()
s.sendall('STORE j.jpg 18917\n')
s.sendall(data)
s.recv(1024)
s.close()  # Close the socket when done
