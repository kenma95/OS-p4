Project 4 Readme v1.0
Author: Yunang Chen, Ruiqi Ma

-Please run the code in Python 2.7.x environment.

-The code can be tested with netcat terminal. In netcat interface, the command will send to server as ctrl+D key is pressed. "Enter" key will send one more newline character and there is a error of "UNDEFINING COMMAND" if the command is sent via "Enter" key.

-If running in the client, a "recv" call must be followed by after the command is sent. Note that for "STORE" command the "recv" call is after the file_content.

-