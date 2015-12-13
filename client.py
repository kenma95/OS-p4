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
	re = s.recv(1024)
	print re
s.close                     # Close the socket when done
