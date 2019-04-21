import socket
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask import jsonify
import sqlite3
import json
import requests #requests is used for storing data in encryption API module
import random
from Crypto.PublicKey import RSA
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

                    resultRecord = received_record.content
                    sentRecord = resultRecord.decode('utf-8')
                    with socketConnection:
                        sentRecordv2 = sentRecord.encode()
                        socketConnection.send(sentRecordv2)
                elif choice == "2" :
                    ##
                    received_finishedTask = socketConnection.recv(1024).decode('utf-8')
                    print(received_finishedTask)# received finished tasks

                    received_selfRating = socketConnection.recv(1024).decode('utf-8')
                    print(received_selfRating) # received self rating
                    ####
                    public_key = RSA.import_key(open("Key Storage\Prospect\publicKey.pem").read())

                    encryptor = PKCS1_OAEP.new(public_key)
                    encoded_FT = received_finishedTask.encode('utf-8')
                    encoded_SF = received_selfRating.encode('utf-8')

                    encrypted_FN = encryptor.encrypt(encoded_FT)
                    encrypted_finishedTasks_stored = base64.b64encode(encrypted_FN)
                    r1 = encrypted_finishedTasks_stored.decode('utf-8')

                    encrypted_SF = encryptor.encrypt(encoded_SF)
                    encrypted_selfRating_stored = base64.b64encode(encrypted_SF)
                    r2 = encrypted_selfRating_stored.decode('utf-8')
                    ####
                    execute_update_task = requests.put("http://127.0.0.1:5000/user/"+str(ID_Returned)+"?Finished_Task="+r1+"&Self_Rating="+r2)
                    print("//check/")
                    resultStatus = execute_update_task.content
                    decodedResult = resultStatus.decode('utf-8')
                    v2 = int(decodedResult)
                    print(type(v2))
                    if v2 == 200:
                        data = str.encode("Data stored successfully !")
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
                else:
                    QR_Code = random.randrange(1, 99999)
                    data_send = str(QR_Code).encode()
                    with socketConnection:
                        socketConnection.send(data_send)
                    print(ID_Returned)
                    insert_status = insert_QRCode_traineeRecord(dbConnection, QR_Code, ID_Returned)
                    if insert_status == 1:
                        print("Insert successfully")
                    else :
                        print("Fail to insert a new row")




