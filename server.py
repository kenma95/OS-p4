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
		print "Block size is " + str(blocksize)
		print "Number of blocks is " + str(n_blocks)


def readlines(buffer,c, recv_buffer=4096, delim='\n'):
	data = c.recv(recv_buffer)
	buffer += data
	lines = buffer.split('\n')
	if buffer and buffer[-1] == '\n':		#check last command's integrity
		buffer =lines.pop()
	else:
		buffer = ''
			
	return buffer, lines



def folder_init():
	if not os.path.exists(".storage"):
		os.makedirs(".storage")
	else:
		shutil.rmtree('.storage')
		os.makedirs(".storage")

def get_thread_id():
	return "[thread" + str(threading.current_thread() )+"] "


def store(line_index,c,lines):
	print lines
	command = lines[line_index]
   	phrase_list = command.split()
   	if len(phrase_list) < 3:
   		print get_thread_id()+"ERROR: WRONG FORMAT"
   	file_name = phrase_list[1]
   	file_size = int(phrase_list[2])

   	if os.path.exists(".storage/"+file_name):
   		print get_thread_id()+"ERROR: FILE EXISTS"
   	f = open(".storage/"+file_name,'w')
   	size_count = 0
   	next_command_index =line_index
   	while size_count < file_size:
   		next_command_index +=1
   		remain = file_size -size_count
   		if remain > len(lines[next_command_index]):			#incoming line, or \n
   			to_add = lines[next_command_index] + '\n'

   		elif remain <= len(lines[next_command_index]):
   			to_add = lines[next_command_index][0:remain]

   		f.writelines(to_add)
   		size_count += len(to_add)

   	#TODO: cluster sim
   	#===================
   	#
   	
   	f.close()
   	#c.send("ACK");
   	print "Sent ACK"
   	return next_command_index


def session(c, addr):
	buffer = ''
	buffer, lines =readlines(buffer,c)
	skip = -1

	while buffer or lines:
		for i in range(0,len(lines)):
			if i <= skip:
				continue
			elif lines[i].startswith("STORE "):
				skip = store(i,c,lines)
			elif lines[i].startswith("DIR"):
	   			dir_(c)
	   		else:
	   			print "ERROR: UNDEFINED COMMAND"

	   	buffer, lines =readlines(buffer,c)


					#Disconnect if no more byte recv
	c.close()
	print get_thread_id() + "Client closed its socket....terminating"





def dir_(c):
	file_list = os.listdir(".storage")
	#c.send(len(file_list))
	print get_thread_id()+"Sent "+str(len(file_list))
	if file_list:
		file_list.sort()
		for item in file_list:
			#c.send(item)
			print item





def main():

	folder_init()
	d = Disk(128,4096)
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	port = 8765
	s.bind(("",port))        # Bind to the port
	print "Listening on port "+str(port)

	s.listen(5)
	while True:
		c, addr = s.accept()     # Establish connection with client.
		print "Received incoming connection from "+str(addr)
	   	c.send('Server:Connected successful')
		#new thread here
		thread = threading.Thread(target=session, args=(c, addr))
		thread.start()	



if __name__ == '__main__': 
    main()
