import socket
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask import jsonify
import sqlite3
import json
import requests #requests is used for storing data in encryption API module
import random
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256

from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
import base64
app = Flask(__name__)
api = Api(app)

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

import functools
import operator


def convertTuple(tup):
    str = functools.reduce(operator.add, (tup))
    return str

def database_connection(db_file):
    try:
        db_conn = sqlite3.connect(db_file) # create a connection variable
        return db_conn  # return the connection variable to be used
    except Error as e:
        print(e)
    return None

def insert_QRCode_traineeRecord(db_conn, QR_Code, Trainee_ID):
    cur = db_conn.cursor()
    cur.execute("INSERT INTO traineeRecord (QR_Code, Trainee_ID, Finished_Task, Self_Rating, Date) VALUES (?,?,'a','b','2-3-2')", (QR_Code, Trainee_ID,))
    db_conn.commit()
    return 1;

def login_DB_module(db_conn,userName,passWord):
    cur = db_conn.cursor()
    cur.execute("SELECT ID_Employee FROM loginDB WHERE User_Name=? AND Pass_Word=?", (userName,passWord,))
    rows = cur.fetchall()
    for row in rows:
        return row

def getName_DB_EmployeeList(db_conn, ID):
    cur = db_conn.cursor()
    cur.execute("SELECT Employee_Name FROM employeeList WHERE ID_Employee = ?", (ID,))

    rows = cur.fetchall()

    for row in rows:
        return row
def querying_traineeID(db_conn,qr_code):
    cur = db_conn.cursor()
    cur.execute("select Trainee_ID from traineeRecord where QR_Code = ?",(qr_code,))
    rows = cur.fetchall()
    for row in rows:
        return row

def querying_record(db_conn,qr_code):
    cur = db_conn.cursor()
    cur.execute("SELECT Finished_Task, Self_Rating from traineeRecord where QR_Code = ?",(qr_code,))
    rows = cur.fetchall()
    for row in rows:
        return row

def return_publicKey(db_conn, ID):
    cur = db_conn.cursor()
    cur.execute("SELECT Public_Key FROM employeeList WHERE ID_Employee = ?", (ID,))

    rows = cur.fetchall()

    for row in rows:
        return row

def searchingRecord(db_conn,assessID,sign_status):
    cur = db_conn.cursor()
    cur.execute("select * from traineeRecord where ID_Supervisor = ? and Signing_Status = ?",(assessID,sign_status,))
    rows = cur.fetchall()
    for row in rows:
        return row
def updateAgain(db_conn,finishedTask,selfRating,qr_code):
    cur = db_conn.cursor()
    cur.execute("update traineeRecord set Finished_Task = ? , Self_Rating = ? where QR_Code = ?",(finishedTask,selfRating,qr_code,))
    db_conn.commit()
    return 1
def updateAgainV2(db_conn,finishedTask,selfRating,supervisorRating,supervisorFeedback,signingStatus,qr_code):
    cur = db_conn.cursor()
    cur.execute("update traineeRecord set Finished_Task = ? , Self_Rating = ? , Supervisor_Rating = ? , Supervisor_FeedBack = ? , Signing_Status = ? where QR_Code = ?",(finishedTask,selfRating,supervisorRating,supervisorFeedback,signingStatus,qr_code))
    db_conn.commit()
    return 1
def digitalSigned(Form):
    key = RSA.import_key(open('Key Storage\Badcc\privateKey.pem').read())  # get the private key.
    h = SHA256.new(Form.encode('utf-8'))  # hash the message
    print("Your hashed message : ", h)
    signature = pss.new(key).sign(h)  # sign the message.
    print("Your signature : ", signature)
    print(type(signature))

    newMessage = Form
    key = RSA.import_key(open('Key Storage\Badcc\publicKey.pem').read())
    h = SHA256.new(newMessage.encode('utf-8'))
    verifier = pss.new(key)  # verify the messages.
    signed = "signed"
    try:
        verifier.verify(h, signature)
        return signed
    except (ValueError, TypeError):
        print("The signature is not authentic.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("Server is now listening for a client.")
    s.listen()
    socketConnection, addr = s.accept()
    with socketConnection:
        print('Connected by', addr)
        while True:
            userName = socketConnection.recv(1024)
            passWord = socketConnection.recv(2014)
            print("-----------------")
            print(userName.decode('utf-8'))
            print(passWord.decode('utf-8'))
            print("-----------------")
            linkPath = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\King.db"
            dbConnection = database_connection(linkPath)
            result_query_login = login_DB_module(dbConnection,userName.decode('utf-8'),passWord.decode('utf-8'))
            if result_query_login is None:
                with socketConnection:
                    data_send = str.encode("Fail to login. Please check your info again !")
                    socketConnection.send(data_send)
            ID_Returned = result_query_login[0]
            print(ID_Returned)
            Name_Returned = getName_DB_EmployeeList(dbConnection, ID_Returned)
            user_Name = Name_Returned[0]
            with socketConnection:
                data = "Hello, " + user_Name
                data_send = data.encode()
                socketConnection.send(data_send)

                flag = "Succeed"
                data_send = flag.encode()
                socketConnection.send(data_send)

                choice = socketConnection.recv(1024).decode('utf-8') # waiting for client choosing choice
                print(choice)

                if choice == "1":
                    received_qr_code = int(socketConnection.recv(1024).decode('utf-8'))
                    received_record = requests.get("http://127.0.0.1:5000/user/"+str(received_qr_code))
                    print(type(received_record))

                    resultRecord = received_record.content
                    print(type(resultRecord))
                    sentRecord = resultRecord.decode('utf-8')
                    print(type(sentRecord))
                    ##
                    x = json.loads(sentRecord)
                    print(type(x))
                    num = x[2]
                    print(type(num))
                    print(num)
                    ##
                    with socketConnection:
                        sentRecordv2 = sentRecord.encode()
                        socketConnection.send(sentRecordv2)
                elif choice == "2" :
                    QR_Code = random.randrange(1, 99999)
                    #insert_QRCode_traineeRecord(dbConnection, QR_Code, ID_Returned)
                    ##
                    received_finishedTask = socketConnection.recv(1024).decode('utf-8')
                    print("finished task = ", received_finishedTask)

                    received_selfRating = socketConnection.recv(1024).decode('utf-8')
                    print("self rating = ",received_selfRating) # received self rating # received finished tasks
                    ####
                    received_supervisorID = socketConnection.recv(1024).decode('utf-8')
                    print("supervisor id = ", received_supervisorID)

                    querying_publicKey = return_publicKey(dbConnection,received_supervisorID)
                    toString_publicKey = convertTuple(querying_publicKey)
                    print(toString_publicKey)
                    public_key = RSA.import_key(open(toString_publicKey).read())

                    encryptor = PKCS1_OAEP.new(public_key)
                    encoded_FT = received_finishedTask.encode('utf-8')
                    encoded_SF = received_selfRating.encode('utf-8')

                    encrypted_FN = encryptor.encrypt(encoded_FT)
                    encrypted_finishedTasks_stored = base64.b64encode(encrypted_FN)
                    r1 = encrypted_finishedTasks_stored.decode('utf-8')
                    print(r1)
                    encrypted_SF = encryptor.encrypt(encoded_SF)
                    encrypted_selfRating_stored = base64.b64encode(encrypted_SF) #byte
                    r2 = encrypted_selfRating_stored.decode('utf-8')   # decode : byte -> string (r1)
                    print(r2)
                    ####
                    statusSigning = "unsigned"
                    execute_update_task = requests.put("http://127.0.0.1:5000/user/"+str(ID_Returned)+"?Finished_Task="+str(r1)+"&Self_Rating="+str(r2)+"&ID_Supervisor="+str(received_supervisorID)+"&QR_Code="+str(QR_Code)+"&Signing_Status="+str(statusSigning))
                    print("//check/")
                    resultStatus = execute_update_task.content
                    decodedResult = resultStatus.decode('utf-8')
                    v2 = int(decodedResult)
                    print(type(v2))
                    if v2 == 200:
                        announceUpdated = updateAgain(dbConnection,r1,r2,QR_Code)
                        if announceUpdated == 1:
                            sentData = "Data updated successfully"
                            data = sentData.encode()
                            with socketConnection:
                                socketConnection.send(data)
                    ##
                elif choice == "3":
                    # now receiving qr code for querying database.
                    received_qr_code = int(socketConnection.recv(1024).decode('utf-8'))
                    record_result = querying_record(dbConnection,received_qr_code)
                    record_sent = json.dumps(record_result)
                    print("Record = "+record_sent)
                    with socketConnection:
                        socketConnection.send(record_sent.encode())

                elif choice == "4":
                    received_assessID = int(socketConnection.recv(1024).decode('utf-8'))

                    sign_status = "unsigned"
                    record_list = searchingRecord(dbConnection,received_assessID,sign_status)

                    record_dumps = json.dumps(record_list)

                    print(record_dumps)
                    print(type(record_dumps))

                    socketConnection.send(record_dumps.encode())

                    received_assessQR = int(socketConnection.recv(1024).decode('utf-8'))

                    print(received_assessQR)

                    assessRecord = querying_record(dbConnection,received_assessQR)
                    print("//")
                    print(assessRecord)
                    print("//")
                    print(type(assessRecord))

                    r = json.dumps(assessRecord)
                    print(type(r))
                    x = json.loads(r)

                    private_key = RSA.import_key(open("Key Storage\Badcc\privateKey.pem").read())
                    encryptor = PKCS1_OAEP.new(private_key)

                    encode_x0 = x[0].encode('utf-8')
                    decoded_encrypted_msg1 = base64.b64decode(encode_x0)
                    decoded_decrypted_msg1 = encryptor.decrypt(decoded_encrypted_msg1)

                    print("Your decrypted message = ", decoded_decrypted_msg1.decode('utf-8'))
                    e1 = decoded_decrypted_msg1.decode('utf-8')
                    ##
                    encode_x1 = x[1].encode('utf-8')
                    decoded_encrypted_msg2 = base64.b64decode(encode_x1)
                    decoded_decrypted_msg2 = encryptor.decrypt(decoded_encrypted_msg2)

                    print("Your decrypted message = ", decoded_decrypted_msg2.decode('utf-8'))
                    e2 = decoded_decrypted_msg2.decode('utf-8')
                    ##
                    ## now send result back to supervisor
                    socketConnection.send(e1.encode())
                    socketConnection.send(e2.encode())
                    ## receive rating and feedback
                    received_rating = socketConnection.recv(1024).decode('utf-8')
                    received_feedback = socketConnection.recv(1024).decode('utf-8')

                    # encode process
                    encoded_x1 = e1.encode()
                    encoded_x2 = e2.encode()
                    encoded_x3 = received_rating.encode()
                    encoded_x4 = received_feedback.encode()

                    forSigningOnly = received_rating+","+received_feedback


                    signStatusUpdated = digitalSigned((forSigningOnly))

                    Trainee_ID_queried = querying_traineeID(dbConnection,received_assessQR)
                    print("Look at this ",Trainee_ID_queried)
                    print(type(Trainee_ID_queried))
                    Trainee_ID_queried = convertTuple(Trainee_ID_queried)
                    querying_publicKey = return_publicKey(dbConnection, Trainee_ID_queried)
                    toString_publicKey = convertTuple(querying_publicKey)
                    print(toString_publicKey)
                    public_key = RSA.import_key(open(toString_publicKey).read())

                    encryptor = PKCS1_OAEP.new(public_key)

                    encrypted_FN = encryptor.encrypt(encoded_x1)
                    encrypted_finishedTasks_stored = base64.b64encode(encrypted_FN)
                    b1 = encrypted_finishedTasks_stored.decode('utf-8') # finished task

                    encrypted_FN = encryptor.encrypt(encoded_x2)
                    encrypted_finishedTasks_stored = base64.b64encode(encrypted_FN)
                    b2 = encrypted_finishedTasks_stored.decode('utf-8') # self rating

                    encrypted_FN = encryptor.encrypt(encoded_x3)
                    encrypted_finishedTasks_stored = base64.b64encode(encrypted_FN)
                    b3 = encrypted_finishedTasks_stored.decode('utf-8') # rating

                    encrypted_FN = encryptor.encrypt(encoded_x4)
                    encrypted_finishedTasks_stored = base64.b64encode(encrypted_FN)
                    b4 = encrypted_finishedTasks_stored.decode('utf-8') # feed back

                    # these were encrypted data
                    print(b1)
                    print(b2)
                    print(b3)
                    print(b4)

                    # get those data to be updated in database API
                    assessment_update = requests.put("http://127.0.0.1:5000/user/"+str(received_assessQR)+"?Finished_Task="+str(b1)+"&Self_Rating="+str(b2)+"&Supervisor_Rating="+str(b3)+"&Supervisor_FeedBack="+str(b4)+"&Signing_Status="+str(signStatusUpdated))
                    resultStatus = assessment_update.content
                    decodedResult = resultStatus.decode('utf-8')
                    v2 = int(decodedResult)
                    print(type(v2))
                    if v2 == 200:
                        announceUpdated = updateAgainV2(dbConnection,b1,b2,b3,b4,signStatusUpdated, received_assessQR)
                        if announceUpdated == 1:
                            sentData = "Assessment updated successfully"
                            data = sentData.encode()
                            with socketConnection:
                                socketConnection.send(data)