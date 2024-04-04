import os
import shutil
import socket
import struct

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
LIST    -   print current list of files /
RETR    -   retrieve/get file(s) /
DELE    -   delete file(s) 
STOR    -   upload data at the server site -
HELP    -   returns available commands for the client /
QUIT    -   close socket
"""

FTP_COMMANDS = """
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
LIST    -   print current list of files 
RETR    -   retrieve/get file(s)
DELE    -   delete file(s) 
STOR    -   upload data at the server site 
HELP    -   returns available commands for the client
QUIT    -   close socket
"""

HOST = "127.0.0.1"
PORT = 21



def startClient():
    isLoggedIn = False
    hasPasv = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        if s.recv(1024).decode('utf-8') == '220':
            while True:
                userInput = input("Enter command: ")
                cmd = userInput.split(" ")[0]
                #print(cmd_split)
                if not isLoggedIn:
                    match cmd:
                        case 'USER':
                            s.sendall(userInput.encode('utf-8'))
                            if s.recv(1024).decode('utf-8').split(" ")[0] == '331':
                                password = input("Please input user password: ")
                                message = "PASS " + password
                                s.send(message.encode('utf-8'))
                                if s.recv(1024).decode('utf-8').split(" ")[0] == '230':
                                    isLoggedIn = True
                                    print("Logged in Successfully!")
                        case 'QUIT':
                            s.close()
                            break
                        case 'HELP':
                            print(FTP_COMMANDS)
                        case _:
                            print("Invalid command!")
                elif isLoggedIn and not hasPasv:
                    match cmd:
                        case 'PWD':
                            s.sendall('PWD'.encode('utf-8'))
                            print("Current Working Directory:\n")
                            print(" ".join(s.recv(4096).decode('utf-8').split(" ")[1:]))
                        case 'CWD':
                            print("TODO")
                        case 'CDUP':
                            print("TODO")
                        case 'MKDIR':
                            print("TODO")
                        case 'QUIT':
                            s.close()
                            break
                        case 'HELP':
                            print(FTP_COMMANDS)
                        case 'PASV':
                            s.send('PASV'.encode('utf-8'))
                            a1, a2, a3, a4, p1, p2 = s.recv(1024).decode('utf-8').split(' ')[-1][1:-2].split(',')
                            data_add = f'{a1}.{a2}.{a3}.{a4}'
                            data_port = int(p1) * 256 + int(p2)
                            print(f'{data_add} {type(data_add)} : {data_port} {type(data_port)}')
                            transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            try:
                                transfer_socket.connect((data_add, data_port))
                            except Exception as e:
                                print('Error in establishing passive conncetion\n')
                                print(e)
                            else:
                                print("Passive connection established.")
                                hasPasv = True
                        case _:
                            print("Invalid command!")
                elif isLoggedIn and hasPasv:
                    match cmd:
                        case 'LIST':
                            s.send('LIST'.encode('utf-8'))
                            print(transfer_socket.recv(4096).decode('utf-8'))
                            transfer_socket.close()
                            hasPasv = False
                        case 'RETR':
                            filename = userInput.split(" ")[1]
                            print(filename)
                            s.send(("RETR " + filename).encode('utf-8'))
                            res = s.recv(1024).decode('utf-8')
                            res_code = res.split(" ")[0]
                            if res_code == '150':
                                print("Receiving...")
                                file = open(filename, "wb")
                                while True:
                                    data = transfer_socket.recv(1024)
                                    file.write(data)
                                    if len(data) < 1024:
                                        file.close()
                                        break
                                print(s.recv(1024).decode('utf-8'))
                            elif res_code == '550':
                                print(" ".join(res.split(" ")[1:]))
                            transfer_socket.close()
                            hasPasv = False
                        case 'STOR':
                            filename = userInput.split(" ")[1]
                            print(filename)
                            s.send(("STOR " + filename).encode('utf-8'))
                            res = s.recv(1024).decode('utf-8')
                            res_code = res.split(" ")[0]
                            if res_code == '150':
                                file = open(filename, "rb")
                                content = file.read()
                                for i in range(0, len(content), 1024):
                                    data = content[i: i+1024]
                                    transfer_socket.send(data)
                                file.close()
                            print(s.recv(1024).decode('utf-8'))
                            transfer_socket.close()
                            hasPasv = False
                        case _:
                            print("Invalid command!")
                
                

def main():
    startClient()

if __name__ == "__main__":
    main()
