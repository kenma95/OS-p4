import socket
import threading
import os
import shutil



def folder_init():
	if not os.path.exists(".storage"):
    	os.makedirs(".storage")
	else:
		shutil.rmtree('/.storage')
		os.makedirs(".storage")




def store(line,s):
   	phrase_list = line.split()
   	if len(phrase_list) < 3:
   		print "ERROR: WRONG FORMAT"
   	file_name = phrase_list[1]
   	file_size = phrase_list[2]
   	if os.path.exists(".storage/"+file_name):
   		print "ERROR: FILE EXISTS"
   	f = open(file_name,'w')
   	size_count =0
   	#TODO: cluster sim
   	#===================
   	#
   	while (size_count< file_size):
   		buf = s.recv(1024)
   		size_count += len(buf)
   		f.write(buf)
   		if (size_count < file_size):
   			f.write("\n")
   	f.close()
   	s.send("ACK");
   	print "Sent ACK"





def dir_(line,s):
	file_list = os.listdir(".storage")
	s.send(len(file_list))
	print "Sent "+len(file_list)
	if not file_list.empty():
		file_list.sort()
		for item in file_list:
			s.send(item)
			print item




s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = 8765
s.bind(("",8765))        # Bind to the port

s.listen(5)
while True:
	c, addr = s.accept()     # Establish connection with client.
	#new thread here
   	print 'Server: Got connection from', addr
   	c.send('Server:Connected successful')

	line = s.recv(1024)
   	print "Rcvd: " + line
   	if line.startswith("STORE "):
   		store(line,s)
   	if line.startswith("DIR"):
   		dir_(line,s)


   


   c.close()                # Close the connection
