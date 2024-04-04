import os
import shutil
import socket

""" 
List of FTP Commands
USER    -   specify username /
PASS    -   specify password /
PWD     -   print current working directory /
CWD     -   change current working directory -
CDUP    -   Change users current working directory to the immediate parent of the CWD -
MKD     -   make directory -
RMD     -   remove directory -
PASV    -   client initiates control connection to server. Requests server port to connect to
            for transmitting data. FTP server specifies the port to use in the reply. -
LIST    -   print current list of files
RETR    -   retrieve/get file(s)
DELE    -   delete file(s)
STOR    -   upload data at the server site
HELP    -   returns available commands for the client
TYPE    -   transfer mode (ASCII/Binary)
MODE    -   set the transfer mode (Stream, Block, Compressed)
STRU    -   set file transfer structure
QUIT    -   close socket
"""

users = {
    'john' : 1234,
    'jane' : 5678,
    'joe' : 'qwerty' 
}

HOST = "127.0.0.1"
PORT = 21

active_user = ""

def startServer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print('Server listening on port 3000...')
        conn, addr = s.accept()
        with conn:
            print(f"Connected with {addr}")
            conn.send("220".encode('utf-8'))
            while True:
                try:
                    print(transfer_socket.getsockname())
                except:
                    print("None")
                userInput = conn.recv(1024).decode('utf-8')
                cmd = userInput.split(" ")[0]
                
                match cmd:
                    case "USER":
                        current_user = userInput.split(" ")[1]
                        print(current_user)
                        conn.send("331 User name okay, please provide password".encode('utf-8'))
                        req = conn.recv(1024).decode('utf-8').split(" ")
                        cmd = req[0]
                        if cmd == "PASS":
                            userpass = req[1]
                            print(userpass)
                        if current_user in users.keys():
                            if str(users[current_user]) == userpass:
                                conn.send("230 User logged in, proceed".encode('utf-8'))
                                print('Sent')
                            else:
                                conn.send("430 Invalid username or password".encode('utf-8'))
                        else:
                            conn.send("430 Invalid username or password".encode('utf-8'))
                    case "PWD":
                        fin_list = ""
                        currdir = os.getcwd()
                        print(currdir)
                        conn.sendall(("257 " + currdir).encode("utf-8"))
                    case "PASV":
                        transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        transfer_socket.bind((HOST, 0))
                        print(transfer_socket.getsockname()[1])
                        a1, a2, a3, a4 = transfer_socket.getsockname()[0].split(".")
                        p1 = int(int(transfer_socket.getsockname()[1])/256)
                        p2 = int(transfer_socket.getsockname()[1])%256
                        msg = f'227 Entering Passive Mode ({a1},{a2},{a3},{a4},{p1},{p2}).'
                        conn.send(msg.encode('utf-8'))
                        transfer_socket.listen(1)
                        transfer_conn, transfer_addr = transfer_socket.accept()
                    case "LIST":
                        fin_list = ""
                        currdir = os.getcwd()
                        for file in os.listdir(currdir):
                            path = os.path.join(currdir, file)
                            if os.path.isfile(path):
                                size = os.path.getsize(path)
                                fin_list += f'{file}: {size} bytes\r\n'
                        transfer_conn.sendall(fin_list.encode('utf-8'))
                        transfer_conn.close()
                    case "RETR":
                        filename = " ".join(userInput.split(" ")[1:])
                        print(filename)
                        currdir = os.getcwd()
                        if filename in os.listdir(currdir):
                            print("FILEFOUND")
                            conn.send(f'150 Opening BINARY mode data connection for {filename} (1024 bytes).'.encode('utf-8'))
                            file = open(filename, "rb")
                            content = file.read()
                            for i in range(0, len(content), 1024):
                                data = content[i: i+1024]
                                transfer_conn.send(data)
                            conn.send(f'226 Transfer Complete.'.encode('utf-8'))
                        else:
                            conn.send(f'550 Requested action not taken. File unavailable (e.g. file not found, no access)'.encode('utf-8'))
                            transfer_conn.close()

                
def main():
    startServer()

if __name__ == "__main__":
    main()