#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name

s.connect(("localhost", 8765))

print "Client: Connect Sucessful"
print s.recv(1024)
f = open ("cmmd.txt",'r')
for line in f:
	s.send(line)
	if  line.startswith("STORE") or  line.startswith("DIR") or \
	line.startswith("READ") or  line.startswith("DEL"):
		re = s.recv(1024)
		print re
s.close                     # Close the socket when done
