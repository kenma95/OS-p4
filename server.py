import socket
import threading

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = 8765
s.bind(("",8765))        # Bind to the port

s.listen(5)
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Server: Got connection from', addr
   c.send('Server:Connected successful')
   s.recv(1024)
   print "processing"

   c.close()                # Close the connection
