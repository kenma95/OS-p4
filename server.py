import socket
import threading
import os
import shutil

class Disk:
	"""Simulation class of Cluster Disk"""
	def __init__(self,n_blocks, blocksize):
		self.n_blocks = n_blocks
		self.blocksize = blocksize

		relation = {}
		disk_map = "."*n_blocks
		print "Block size is " + blocksize
		print "Number of blocks is " + n_blocks


def folder_init():
	if not os.path.exists(".storage"):
    	os.makedirs(".storage")
	else:
		shutil.rmtree('/.storage')
		os.makedirs(".storage")

def get_thread_id():
	return "[thread" + thread.get_ident() +"] "


def store(line,s):
   	phrase_list = line.split()
   	if len(phrase_list) < 3:
   		print get_thread_id()+"ERROR: WRONG FORMAT"
   	file_name = phrase_list[1]
   	file_size = phrase_list[2]
   	if os.path.exists(".storage/"+file_name):
   		print get_thread_id()+"ERROR: FILE EXISTS"
   	f = open(file_name,'w')
   	size_count = 0
   	#TODO: cluster sim
   	#===================
   	#
   	while (size_count< file_size):
   		buf = c.recv(1024)
   		size_count += len(buf)
   		f.write(buf)
   		if (size_count < file_size):
   			f.write("\n")
   	f.close()
   	c.send("ACK");
   	print get_thread_id()+"Sent ACK"

def session(c, addr):
	line = c.recv(1024)

	while line:
   		print get_thread_id() + "Rcvd: " + line
	   		if line.startswith("STORE "):
	   			store(line,c)
	   		if line.startswith("DIR"):
	   			dir_(line,c)

	   	line = c.recv(1024)
	c.close()				#Disconnect if no more byte recv
	print get_thread_id() + "Client closed its socket....terminating"




def dir_(line,c):
	file_list = os.listdir(".storage")
	c.send(len(file_list))
	print get_thread_id()+"Sent "+len(file_list)
	if not file_list.empty():
		file_list.sort()
		for item in file_list:
			c.send(item)
			print item


def main():

	folder_init()
	d = Disk(128,4096)
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	port = 8765
	s.bind(("",port))        # Bind to the port
	print "Listening on port "+port

	s.listen(5)
	while True:
		c, addr = s.accept()     # Establish connection with client.
		print "Received incoming connection from "+addr
	   	c.send('Server:Connected successful')
		#new thread here
		thread = threading.Thread(target=session, args=(c, addr))
		thread.start()	






if __name__ == '__main__': 
    main()
