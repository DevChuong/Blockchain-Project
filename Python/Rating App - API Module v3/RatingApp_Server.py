import socket
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import smtplib, ssl
import sqlite3
import json
import requests #requests is used for storing data in encryption API module
import random
import hashlib

from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pss
from Cryptodome.Hash import SHA256

from Cryptodome import Random
from Cryptodome.Cipher import PKCS1_OAEP
import base64
app = Flask(__name__)
api = Api(app)

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

import functools
import operator

def see_record(db_conn, qr_code, date):

    cur = db_conn.cursor()
    cur.execute("select * from traineeRecord where QR_Code=? and Date =?", (qr_code,date,))

    rows = cur.fetchall()
    print("check rows = ",rows)
    for row in rows:
        return row

def SHA256_Hash_Module(hashed_record):
    result = hashlib.sha256(hashed_record.encode())
    return result.hexdigest()

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
        print("we have row as ",row)
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
def querying_qr(db_conn,date):
    status = "signed"
    cur = db_conn.cursor()
    cur.execute("select QR_Code from traineeRecord where Signing_Status =? and Date =?",(status,date,))
    rows = cur.fetchall()
    return rows

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
    cur.execute("select QR_Code from traineeRecord where ID_Supervisor = ? and Signing_Status = ?",(assessID,sign_status,))
    rows = cur.fetchall()
    return rows
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
def digitalSigned(ID, signature):

    newID = ID
    # int -> str
    newID = str(newID)
    key = RSA.import_key(open('Key Storage\Badcc\publicKey.pem').read())
    h = SHA256.new(newID.encode('utf-8'))
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
            userName = socketConnection.recv(1024).decode('utf-8')
            passWord = socketConnection.recv(2014).decode('utf-8')
            ##
            ##
            print("-----------------")
            print(userName)
            print(passWord)
            print("-----------------")
            linkPath = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\RatingApp.db"
            dbConnection = database_connection(linkPath)
            result_query_login = login_DB_module(dbConnection,userName,passWord)
            print("type of result query login is ",type(result_query_login))
            print(result_query_login)
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
                    # now update getDate()
                    received_date = socketConnection.recv(1024).decode('utf-8')
                    return_qr = querying_qr(dbConnection,received_date)
                    return_qr = json.dumps(return_qr)
                    print(return_qr)
                    return_qr_send = return_qr.encode()
                    socketConnection.send(return_qr_send)
                    received_qr_code = int(socketConnection.recv(1024).decode('utf-8'))
                    print("qr_code = ", received_qr_code)
                    print("date = ", received_date)
                    condition1 = "condition1"
                    received_record = requests.get("http://127.0.0.1:5000/user/"+condition1+"?QR_Code=" + str(received_qr_code) + "&Date=" + received_date)
                    resultRecord = received_record.content
                    sentRecord = resultRecord.decode('utf-8')
                    print("sentRecord = ", sentRecord)
                    a = json.loads(sentRecord)
                    print(a[0])
                    print(a[1])
                    print(a[2])
                    print(a[3])
                    print(a[4])
                    print(a[5])
                    print(a[6])
                    print(a[7])
                    print(a[8])
                    print(a[9])
                    print(a[10])
                    with socketConnection:
                        a[0] = str(a[0])
                        a[0] = a[0].encode()
                        socketConnection.send(a[0])
                        a[1] = str(a[1])
                        a[1] = a[1].encode()
                        socketConnection.send(a[1])
                        check1 = socketConnection.recv(1024).decode('utf-8')
                        if check1 == "check":
                            a[2] = a[2].encode()
                            socketConnection.send(a[2])
                            a[3] = a[3].encode()
                            socketConnection.send(a[3])
                            check2 = socketConnection.recv(1024).decode('utf-8')
                            if check2 == "check":
                                a[4] = a[4].encode()
                                socketConnection.send(a[4])
                                a[5] = str(a[5])
                                a[5] = a[5].encode()
                                socketConnection.send(a[5])
                                check3 = socketConnection.recv(1024).decode('utf-8')
                                if check3 == "check":
                                    a[6] = a[6].encode()
                                    socketConnection.send(a[6])
                                    a[7] = a[7].encode()
                                    socketConnection.send(a[7])
                                    check4 = socketConnection.recv(1024).decode('utf-8')
                                    if check4 == "check":
                                        a[8] = a[8].encode()
                                        socketConnection.send(a[8])
                                        a[9] = a[9].encode()
                                        socketConnection.send(a[9])
                elif choice == "2" :
                    QR_Code = random.randrange(1, 99999)
                    print(type(QR_Code))
                    received_finishedTask = socketConnection.recv(1024).decode('utf-8')
                    print("finished task = ", received_finishedTask)                    #receive finish task
                    received_selfRating = socketConnection.recv(1024).decode('utf-8')
                    print("self rating = ",received_selfRating)                         #receive self rating
                    received_supervisorID = socketConnection.recv(1024).decode('utf-8')
                    print("supervisor id = ", received_supervisorID)                    #receive supervisor ID
                    received_date = socketConnection.recv(1024).decode('utf-8')
                    print("date = ", received_date)
                    QR_Code = str(QR_Code)
                    socketConnection.send(QR_Code.encode())
                    # receive date
                    # those were unencrypted
                    #### "&Date="+str(received_date)+
                    statusSigning = "unsigned"
                    condition2 = "condition2"
                    execute_update_task = requests.put('http://127.0.0.1:5000/user/' +
                                                       condition2 + '?Trainee_ID=' +
                                                       str(ID_Returned) + '&Finished_Task='
                                                       + received_finishedTask + '&Self_Rating=' +
                                                       received_selfRating + '&ID_Supervisor=' +
                                                       str(received_supervisorID) + '&Date=' +
                                                       str(received_date) + '&QR_Code=' +
                                                       str(QR_Code) + '&Signing_Status=' + str(statusSigning))
                    print("//check/")
                    resultStatus = execute_update_task.content
                    print(resultStatus)
                    print(type(resultStatus))
                    decodedResult = resultStatus.decode('utf-8')
                    v2 = int(decodedResult)
                    print(type(v2))
                    if v2 == 200:
                        sentData = "Data updated successfully"
                        data = sentData.encode()
                        with socketConnection:
                            socketConnection.send(data)
                elif choice == "3":
                    received_date = socketConnection.recv(1024).decode('utf-8')
                    received_qr_code = int(socketConnection.recv(1024).decode('utf-8'))
                    print("qr_code = ", received_qr_code)
                    print("date = ", received_date)
                    condition1 = "condition1"
                    received_record = requests.get('http://127.0.0.1:5000/user/' + condition1 + '?QR_Code=' + str(
                        received_qr_code) + '&Date=' + received_date)
                    resultRecord = received_record.content
                    sentRecord = resultRecord.decode('utf-8')
                    print("sentRecord = ", sentRecord)
                    a = json.loads(sentRecord)
                    print(a[0])
                    print(a[1])
                    print(a[2])
                    print(a[3])
                    print(a[4])
                    print(a[5])
                    print(a[6])
                    print(a[7])
                    print(a[8])
                    print(a[9])
                    print(a[10])
                    a[0] = str(a[0])
                    a[0] = a[0].encode()
                    socketConnection.send(a[0])
                    a[1] = str(a[1])
                    a[1] = a[1].encode()
                    socketConnection.send(a[1])
                    check1 = socketConnection.recv(1024).decode('utf-8')
                    if check1 == "check":
                        a[2] = a[2].encode()
                        socketConnection.send(a[2])
                        a[3] = a[3].encode()
                        socketConnection.send(a[3])
                        check2 = socketConnection.recv(1024).decode('utf-8')
                        if check2 == "check":
                            a[4] = a[4].encode()
                            socketConnection.send(a[4])
                            a[5] = str(a[5])
                            a[5] = a[5].encode()
                            socketConnection.send(a[5])
                            check3 = socketConnection.recv(1024).decode('utf-8')
                            if check3 == "check":
                                a[6] = a[6].encode()
                                socketConnection.send(a[6])
                                a[7] = a[7].encode()
                                socketConnection.send(a[7])
                                check4 = socketConnection.recv(1024).decode('utf-8')
                                if check4 == "check":
                                    a[8] = a[8].encode()
                                    socketConnection.send(a[8])
                                    a[9] = a[9].encode()
                                    socketConnection.send(a[9])
                                    port = 587  # For starttls
                                    smtp_server = "smtp.gmail.com"

                                    check_12 = socketConnection.recv(1024).decode('utf-8')
                                    if check_12 == "check":

                                        check_trigger = "check"
                                        socketConnection.send(check_trigger.encode())
                                        sender_email = socketConnection.recv(1024).decode('utf-8')
                                        receiver_email = socketConnection.recv(1024).decode('utf-8')

                                        check_trigger_1 = "check"
                                        socketConnection.send(check_trigger_1.encode())
                                        check_forSending = socketConnection.recv(1024).decode('utf-8')
                                        if check_forSending == "check":
                                            check_ = "check"
                                            check_ = check_.encode()
                                            socketConnection.send(check_)  # send to trigger
                                            received_decrypted_record = socketConnection.recv(1024).decode('utf-8')
                                            print("received decrypted record = ", received_decrypted_record)
                                            received_password = socketConnection.recv(1024).decode('utf-8')  # receive to trigger
                                            password = received_password
                                            print("Password = ", password)
                                            received_decrypted_record= list(received_decrypted_record.split(","))
                                            received_decrypted_record = str(received_decrypted_record)
                                            message = """\
                                            

                                            """ + received_decrypted_record
                                            context = ssl.create_default_context()
                                            with smtplib.SMTP(smtp_server, port) as server:
                                                server.ehlo()  # Can be omitted
                                                server.starttls(context=context)
                                                server.ehlo()  # Can be omitted
                                                server.login(sender_email, password)
                                                server.sendmail(sender_email, receiver_email, message)
                                            email_status = "Email sent successfully"
                                            socketConnection.send(email_status.encode())

                elif choice == "4":
                    str_ID_Returned = str(ID_Returned)
                    socketConnection.send(str_ID_Returned.encode())
                    sign_status = "unsigned"
                    record_list = searchingRecord(dbConnection,ID_Returned,sign_status)
                    record_dumps = json.dumps(record_list)
                    print(record_dumps)
                    print(type(record_dumps))
                    socketConnection.send(record_dumps.encode())
                    received_assessQR = int(socketConnection.recv(1024).decode('utf-8'))
                    print(received_assessQR)
                    assessRecord = querying_record(dbConnection,received_assessQR)
                    print(assessRecord)
                    print("//")
                    print(type(assessRecord))

                    r = json.dumps(assessRecord)
                    print("<print type r>")
                    print(type(r))
                    print(r)

                    socketConnection.send(r.encode())
                    ##
                    trigger = "trigger"
                    socketConnection.send(trigger.encode())
                    e1 = socketConnection.recv(1024).decode('utf-8')
                    e2 = socketConnection.recv(1024).decode('utf-8')
                    socketConnection.send(trigger.encode())

                    ## receive rating and feedback
                    received_rating = socketConnection.recv(1024).decode('utf-8')
                    e3 = received_rating
                    received_feedback = socketConnection.recv(1024).decode('utf-8')
                    e4 = received_feedback
                    print("e1 = ",e1)
                    print("e2 = ",e2)
                    print("e3 = ",e3)
                    print("e4 = ",e4)
                    record_hashing =  e1+","+e2+","+e3+","+e4
                    # add the hash in here
                    hashedRecord = SHA256_Hash_Module(record_hashing) # all raw data has been hashed

                    ## digital signature
                    signatureReceived = socketConnection.recv(1024)
                    signStatusUpdated = digitalSigned(ID_Returned,signatureReceived)
                    # get those data to be updated in database API
                    condition4 = "condition4"
                    assessment_update = requests.put('http://127.0.0.1:5000/user/' + condition4 +
                                                     '?QR_Code=' + str(received_assessQR) +
                                                     '&Finished_Task=' + str(e1) +
                                                     '&Self_Rating=' + str(e2) +
                                                     '&Supervisor_Rating=' + str(e3) +
                                                     '&Supervisor_FeedBack=' + str(e4) +
                                                     '&Signing_Status=' + str(signStatusUpdated) +
                                                     '&Record_Hashing=' + hashedRecord)
                    resultStatus = assessment_update.content
                    decodedResult = resultStatus.decode('utf-8')
                    v2 = int(decodedResult)
                    print(type(v2))
                    if v2 == 200:
                        sentData = "Assessment updated successfully"
                        data = sentData.encode()
                        with socketConnection:
                            socketConnection.send(data)

                elif choice == "5":
                    check_condition = socketConnection.recv(1024).decode('utf-8')
                    trigger = "trigger"
                    print("check_condition = ",check_condition)
                    socketConnection.send(trigger.encode())
                    data1 = socketConnection.recv(1024).decode('utf-8')
                    data2 = socketConnection.recv(1024).decode('utf-8')
                    print("data1 = ",data1)
                    print("data2 = ",data2)
                    if check_condition == "employee":
                        response = requests.get('http://127.0.0.1:5000/user/'
                                                +check_condition+
                                                '?ID_Employee='+str(data1)+
                                                '&Employee_Name='+data2)  # check employee
                        a = response.content
                        b = a.decode('utf-8')
                        print("b = ",b)
                        b = b.replace('"', '')
                        socketConnection.send(b.encode())
                    elif check_condition == "hash":
                        response = requests.get('http://127.0.0.1:5000/user/'
                                                +check_condition+'?QR_Code='+
                                                str(data1)+'&Trainee_ID='+
                                                str(data2))  # check hash
                        a = response.content
                        b = a.decode('utf-8')
                        b = b.replace('"', '')
                        socketConnection.send(b.encode())

