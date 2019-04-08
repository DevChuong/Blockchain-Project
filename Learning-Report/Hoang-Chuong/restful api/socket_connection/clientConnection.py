import socket
import json
s = socket.socket()
print("Socket successfully created")

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Enter ID : ")
    ID = input()
    sentID = str.encode(ID)
    s.sendall(sentID)

    data = s.recv(1024)
    #b = json.loads(data)
    #print(b)
print('Received : ', repr(data.decode('utf-8')))
