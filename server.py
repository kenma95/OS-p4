import socket
import threading
import os
import shutil
import disk
def folder_init():
    if not os.path.exists(".storage"):
        os.makedirs(".storage")
    else:
        shutil.rmtree('.storage')
        os.makedirs(".storage")

def get_thread_id():
    return "[thread" + str(threading.current_thread().ident) + "] "

def read(line,c,disk):
    phrase_list = line.split()
    if len(phrase_list) < 4:
        print get_thread_id() + "Sent: ERROR: WRONG FORMAT"
        c.send("ERROR: WRONG FORMAT")
    file_name = phrase_list[1]
    file_offset = int(phrase_list[2])
    file_len = int(phrase_list[3])
    if not os.path.exists(".storage/" + file_name):
        print get_thread_id + "Sent: ERROR: NO SUCH FILE"
        c.send("ERROR: NO SUCH FILE")
    else:
        f = open(".storage/" + file_name, 'r')
        file_size = os.path.getsize(".storage/" + file_name)
        if file_size < (file_offset + file_len):
            print get_thread_id() + "ERROR: INVALID BYTE RANGE"
        f.seek(file_offset,0)
        to_read = f.read(file_len)
        to_read = "ACK" + str(file_len)+"\n" + to_read
        c.send(to_read)
        print get_thread_id() + "Sent: "+to_read
    #simulation

def dir_(c):
    file_list = os.listdir(".storage")
    to_return = (str(len(file_list)))
    print get_thread_id() + "Sent " + str(len(file_list)) +"\n"
    if file_list:
        file_list.sort()
        for item in file_list:
            to_return += (item) +"\n"
            print item
    c.send(to_return)



def delete(line,c,disk):
    phrase_list = line.split()
    if len(phrase_list) < 2:
        print get_thread_id() + "ERROR: WRONG FORMAT"
        c.send("ERROR: WRONG FORMAT")
    file_name =  phrase_list[1]
    if not os.path.exists(".storage/" + file_name):
        print get_thread_id + "Sent: ERROR: NO SUCH FILE"
        c.send("ERROR: NO SUCH FILE")
    else:
        os.remove(file_name)
        print get_thread_id() + "Deleted " + file_name + " file 'A' (deallocated 7 blocks)"
        c.send("Deleted " + file_name + " file 'A' (deallocated 7 blocks)")
    return


def store(line, c,disk):
    phrase_list = line.split()
    if len(phrase_list) < 3:
        print get_thread_id() + "ERROR: WRONG FORMAT"
        c.send("ERROR: WRONG FORMAT")
        return
    file_name = phrase_list[1]
    file_size = int(phrase_list[2])      

    
    file_id, block, cluster = disk.store(file_name,file_size)
    if file_id is None:
        print get_thread_id() + "ERROR: INSUFFICIENT DISK SPACE"
        c.send("ERROR: ERROR: INSUFFICIENT DISK SPACE")
        return
    
    if os.path.exists(".storage/" + file_name):
        c.send("ERROR: FILE EXISTS")
        print get_thread_id() + "ERROR: FILE EXISTS"
        return
    f = open(".storage/" + file_name, 'w')
    c.send("ACK")
    print get_thread_id() +"Sent: ACK"
    size_count = 0
    while (size_count<file_size):
        to_add = c.recv(1024)
        size_count += len(to_add)
        f.write(to_add)
 


    f.close()
    # c.send("ACK");
    return


def session(c, addr,disk):
    try:
        while 1:
            line = c.recv(1024)
            if len(line) == 0:  #nothing receive, connection over
                break
            print get_thread_id() + " Rcvd: " + line
            if line.startswith("STORE "):
                store(line,c,disk)
            elif line.startswith("DIR"):
                dir_(c,disk)
            elif line.startswith("READ "):
                read(line,c)
            elif line.startswith("DEL "):
                delete(line,c)
            else:
                print "ERROR: UNDEFINED COMMAND"
                break

            #buffer, lines = readlines(buffer, c)

        # Disconnect if no more byte recv
        c.close()
        print get_thread_id() + "Client closed its socket....terminating"
    except KeyboardInterrupt:
        return


def main():
    folder_init()
    d = disk.Disk(128, 4096)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 8765
    s.bind(("", port))  # Bind to the port
    print "Listening on port " + str(port)
    s.listen(5)

    while True:
        try:
            c, addr = s.accept()  # Establish connection with client.
            print "Received incoming connection from " + str(addr)
            c.send('Server:Connected successful')
            # new thread here
            thread = threading.Thread(target=session, args=(c, addr,d))
            thread.start()
        except KeyboardInterrupt:
            exit()


if __name__ == '__main__':
    main()
