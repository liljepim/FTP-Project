import os
import shutil
import socket

""" 
List of FTP Commands
USER    -   specify username
PASS    -   specify password
PWD     -   print current working directory
CWD     -   change current working directory
CDUP    -   Change users current working directory to the immediate parent of the CWD
MKD     -   make directory
RMD     -   remove directory
PASV    -   client initiates control connection to server. Requests server port to connect to
            for transmitting data. FTP server specifies the port to use in the reply.
LIST    -   

"""