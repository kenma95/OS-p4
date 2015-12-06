#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name

s.connect(("45.63.120.174", 8765))
print "Client: Connect Sucessful"
print s.recv(1024)
f = open ("cmmd.txt",'r')
for line in f:
	s.send(line)
s.close                     # Close the socket when done
