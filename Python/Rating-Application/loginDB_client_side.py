import socket
import json
s = socket.socket()
print("Socket successfully created")

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Enter user name : ")
    ID = input()
    sentID = str.encode(ID)
    s.sendall(sentID)

    print("Enter password : ")
    Name = input()
    sentName = str.encode(Name)
    s.send(sentName)

    data = s.recv(1024).decode('utf-8')
    #b = json.loads(data)
    print(data)

    data_login_status = s.recv(1024).decode('utf-8')
    if data_login_status == "Succeed":
        print("-------Dash Board-------")
        print("1/ See Profile")
        print("2/ Perform Tasks")
        print("3/ Share Profile")
        print("4/ Get QR Code")
        choice = int(input("Enter the choice number [1-2-3-4] : "))

        if choice != 1 and choice != 2 and choice != 3 and choice != 4:
            print("Your choice is invalid. Must be in range from 1 to 4")
        else :
            data_send = str(choice)
            s.send(data_send.encode())
        if choice == 2:
            print("Q.1/ Which is your category ?")
            print("1 - Anathesia")
            print("2 - Cancer")
            print("3 - Lung")
            selected_category = int(input("Select your category : "))
            if selected_category == 1:
                answer = "Anathesia"
                data_send = answer.encode()
                s.send(data_send)
            elif selected_category == 2:
                answer = "Cancer"
                data_send = answer.encode()
                s.send(data_send)
            else:
                answer = "Lung"
                data_send = answer.encode()
                s.send(data_send)

            data_received = s.recv(1024).decode('utf-8')
            print(data_received)

        if choice == 4:
            QR_Code = int(s.recv(1024).decode('utf-8'))
            print(QR_Code)


#print('Received : ', repr(data.decode('utf-8')))
