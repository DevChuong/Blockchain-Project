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

        if choice == 1:
            print("Enter QR Code : ")
            inputQrCode = input()
            sentQrCode = inputQrCode.encode()
            s.send(sentQrCode)
            recordReceived = s.recv(1024).decode('utf-8')
            print(recordReceived)
        if choice == 2:
            print("Finish the following tasks : ")
            print("1/ What is the name of diabate in Vietnamese ?")
            answer1 = input()
            print("2/ How to measure the blood pressure ?")
            answer2 = input()
            print("3/ In what situation you can tell a man is cancer ?")
            answer3 = input()
            totalAnswer = answer1+","+answer2+","+answer3
            print("You have the chance to self-rate yourself, make it carefully : ")
            selfRating = input()
            send_totalAnswer = totalAnswer.encode()
            s.send(send_totalAnswer)                # now sending trainee finished tasks
            send_selfRating = selfRating.encode()
            s.send(send_selfRating)                 # now sending trainee self rating

            data_received = s.recv(1024).decode('utf-8')
            print(data_received)

        if choice == 3:
            input_qr_code = int(input("Enter your qr code : "))
            sent_qrCode = str(input_qr_code)
            s.send(sent_qrCode.encode())

            print("Trainee record for trainee record's QR Code "+sent_qrCode)
            record_received = s.recv(1024).decode('utf-8')
            print(record_received)
        if choice == 4:
            QR_Code = int(s.recv(1024).decode('utf-8'))
            print(QR_Code)


#print('Received : ', repr(data.decode('utf-8')))
