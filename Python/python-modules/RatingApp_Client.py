import socket
import json
import getpass
from datetime import date
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pss
from Cryptodome.Hash import SHA256
from Cryptodome.Cipher import PKCS1_OAEP
import base64
s = socket.socket()
print("Socket successfully created")

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Enter user name : ")
    userName = input()
    sentUserName = str.encode(userName)
    s.sendall(sentUserName)

    print("Enter password : ")
    passwordLogin = input()
    sentPasswordLogin = str.encode(passwordLogin)
    s.send(sentPasswordLogin)

    data = s.recv(1024).decode('utf-8')
    #b = json.loads(data)
    print(data)

    data_login_status = s.recv(1024).decode('utf-8')
    if data_login_status == "Succeed":
        print("-------Dash Board-------")
        print("1/ See Profile")
        print("2/ Perform Tasks")
        print("3/ Share Profile")
        print("4/ Make assessment (Supervisor only)")
        print("5/ Check employee - hashing")
        choice = int(input("Enter the choice number [1-2-3-4-5] : "))
        if choice != 1 and choice != 2 and choice != 3 and choice != 4 and choice != 5:
            print("Your choice is invalid. Must be in range from 1 to 5")
        else :
            data_send = str(choice)
            s.send(data_send.encode())
        if choice == 1:
            print("Enter date : ")
            print("(For example : yy-mm-dd as 2019-05-08)")
            date_search = input()
            sentDate = date_search.encode()
            s.send(sentDate)
            print("Enter QR Code : ")
            inputQrCode = input()
            sentQrCode = inputQrCode.encode()
            s.send(sentQrCode)
            print("-------------------------------")
            print("Your record : ")
            see_record_qr_code = s.recv(1024).decode('utf-8')
            print("QR Code : ",see_record_qr_code)
            see_record_trainee_id = s.recv(1024).decode('utf-8')
            print(" Trainee ID : ",see_record_trainee_id)
            check1 = "check"
            s.send(check1.encode())
            see_record_trainee_task = s.recv(1024).decode('utf-8')
            see_record_trainee_rating = s.recv(1024).decode('utf-8')
            private_key = RSA.import_key(open("Key Storage\Moore\privateKey.pem").read())
            encryptor = PKCS1_OAEP.new(private_key)

            encode_x2 = see_record_trainee_task.encode('utf-8')
            decoded_encrypted_msg2 = base64.b64decode(encode_x2)
            decoded_decrypted_msg2 = encryptor.decrypt(decoded_encrypted_msg2)
            print(" Trainee task answers : ",decoded_decrypted_msg2.decode('utf-8'))
            encode_x2 = see_record_trainee_rating.encode('utf-8')
            decoded_encrypted_msg2 = base64.b64decode(encode_x2)
            decoded_decrypted_msg2 = encryptor.decrypt(decoded_encrypted_msg2)
            print(" Trainee's rating : ",decoded_decrypted_msg2.decode('utf-8'))
            check2 = "check"
            s.send(check2.encode())
            see_record_date = s.recv(1024).decode('utf-8')
            print(" Date trainee performed his task : ",see_record_date)
            see_record_supervisor_id = s.recv(1024).decode('utf-8')
            print(" ID of supervisor who assessed the trainee : ",see_record_supervisor_id)
            check3 = "check"
            s.send(check3.encode())
            see_record_supervisor_rating = s.recv(1024).decode('utf-8')
            encode_x2 = see_record_supervisor_rating.encode('utf-8')
            decoded_encrypted_msg2 = base64.b64decode(encode_x2)
            decoded_decrypted_msg2 = encryptor.decrypt(decoded_encrypted_msg2)
            print(" Supervisor's rating : ",decoded_decrypted_msg2.decode('utf-8'))
            see_record_supervisor_feedback = s.recv(1024).decode('utf-8')
            encode_x2 = see_record_supervisor_feedback.encode('utf-8')
            decoded_encrypted_msg2 = base64.b64decode(encode_x2)
            decoded_decrypted_msg2 = encryptor.decrypt(decoded_encrypted_msg2)
            print(" Supervisor's feedback : ",decoded_decrypted_msg2.decode('utf-8'))
            check4 = "check"
            s.send(check4.encode())
            see_record_signing = s.recv(1024).decode('utf-8')
            print(" The signing status of this record : ",see_record_signing)
            see_record_hashing = s.recv(1024).decode('utf-8')
            print(" The hash of whole record : ",see_record_hashing)
        if choice == 2:
            print("Finish the following tasks : ")
            print("1/ 1 + 1 = ?")
            answer1 = input()
            print("2/ Why Doctor Strange gave Thanos the Time Stone ?")
            answer2 = input()
            print("3/ What is your name in Chinese ?")
            answer3 = input()
            totalAnswer = answer1+","+answer2+","+answer3 #totalAnswer = Finished_Task
            send_totalAnswer = totalAnswer.encode()
            s.send(send_totalAnswer)            #send finished_task
            print("You have the chance to self-rate yourself, make it carefully : ")
            selfRating = input() #Self_Rating
            send_selfRating = selfRating.encode()
            s.send(send_selfRating)             #send self rating
            print("Input supervisor ID : ")
            ID_Supervisor = input()
            send_supervisorID = ID_Supervisor.encode()
            s.send(send_supervisorID)           #send supervisor ID
            #now get the actual date from system
            today = date.today()
            date_string = str(today)
            send_date = date_string.encode()
            s.send(send_date)                   #send date
            data_received = s.recv(1024).decode('utf-8')
            print(data_received)
        if choice == 3:
            print("Enter date : ")
            print("(For example : yy-mm-dd as 2019-05-08)")
            date_search = input()
            sentDate = date_search.encode()
            s.send(sentDate)    # send
            print("Enter QR Code : ")
            inputQrCode = input()
            sentQrCode = inputQrCode.encode()
            s.send(sentQrCode)  # send
            print("(This option went through input sender and receiver email")
            print("     users are advised to type in their password only)")
            print("Input your email password : ")
            password = getpass.getpass() # this is available to use in command prompt only
            #password = input() this was used in pycharm
            password = password.encode()
            print("Password = ",password)
            checkOption3 = s.recv(1024).decode('utf-8') # receive
            if checkOption3 == "check":
                s.send(password)  # send
        if choice == 4:
            assess_supervisorID = int(input("Enter your ID : "))
            str_assessSupervisorID = str(assess_supervisorID)
            s.send(str_assessSupervisorID.encode())
            print("Trainee record that has not been signed by supervisor : ")
            receivedList = s.recv(1024).decode('utf-8') # this returns a list of record with the condition of Signing_Status = "unsigned"
            print(receivedList)
            assessRecord = int(input("Enter trainee QR code : "))
            str_record = str(assessRecord)
            s.send(str_record.encode())
            receivedRecord = s.recv(1024).decode('utf-8')
            x = json.loads(receivedRecord)
            print(type(x))
            private_key = RSA.import_key(open("Key Storage\Badcc\privateKey.pem").read())
            encryptor = PKCS1_OAEP.new(private_key)
            encode_x0 = x[0].encode('utf-8')
            decoded_encrypted_msg1 = base64.b64decode(encode_x0)
            decoded_decrypted_msg1 = encryptor.decrypt(decoded_encrypted_msg1)
            print("Your decrypted message = ", decoded_decrypted_msg1.decode('utf-8'))
            e1 = decoded_decrypted_msg1.decode('utf-8')
            encode_x1 = x[1].encode('utf-8')
            decoded_encrypted_msg2 = base64.b64decode(encode_x1)
            decoded_decrypted_msg2 = encryptor.decrypt(decoded_encrypted_msg2)
            print("Your decrypted message = ", decoded_decrypted_msg2.decode('utf-8'))
            e2 = decoded_decrypted_msg2.decode('utf-8')
            ## now start to evaluate the form
            supervisorRating = input("Input your rating : ").encode()
            feedBack = input("Input your feedback : ").encode()
            trigger = s.recv(1024).decode('utf-8')
            if trigger == "trigger":
                s.send(e1.encode())
                s.send(e2.encode())
                trigger = s.recv(1024).decode('utf-8')
                if trigger == "trigger":
                    s.send(supervisorRating)
                    s.send(feedBack)
            # int -> str
            assess_supervisorID = str(str_assessSupervisorID)
            key = RSA.import_key(open('Key Storage\Badcc\privateKey.pem').read())  # c # get the private key.
            h = SHA256.new(assess_supervisorID.encode('utf-8'))  # hash the message #c
            signature = pss.new(key).sign(h)  # sign the message. #c
            #now send signature
            s.send(signature)
            assessmentUpdated = s.recv(1024).decode('utf-8')
            print(assessmentUpdated)
        if choice == 5:
            print("Check employee [1] - check hashing [2] : ")
            check_option = input()
            if check_option == "1":
                check_condition = "employee"
                ID_Employee = input("Input ID employee : ")
                Employee_Name = input("Input employee name : ")
                s.send(check_condition.encode())
                trigger = s.recv(1024).decode('utf-8')
                if trigger == "trigger":
                    s.send(ID_Employee.encode())
                    s.send(Employee_Name.encode())
                    print("Employee result : ")
                    result = s.recv(1024).decode('utf-8')
                    result = int(result)
                    if result == 1:
                        print("Available employee.")
                    elif result ==0:
                        print("Invalid employee.")
            elif check_option == "2":
                check_condition = "hash"
                QR_Code = input("Input QR code : ")
                Trainee_ID = input("Input trainee ID : ")
                s.send(check_condition.encode())
                trigger = s.recv(1024).decode('utf-8')
                if trigger == "trigger":
                    s.send(QR_Code.encode())
                    s.send(Trainee_ID.encode())
                    print("Hashing result : ")
                    result = s.recv(1024).decode('utf-8')
                    print(result)
#print('Received : ', repr(data.decode('utf-8')))