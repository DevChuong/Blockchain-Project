import socket
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask import jsonify
import sqlite3
import json
import random

app = Flask(__name__)
api = Api(app)

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)



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

def update_performed_task(db_conn, Task, Trainee_ID):
    cur = db_conn.cursor()
    cur.execute("UPDATE traineeRecord SET Finished_Task = ? WHERE Trainee_ID = ?", (Task, Trainee_ID,))

    db_conn.commit()
    return 1


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
            linkPath = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\Washington.db"
            dbConnection = database_connection(linkPath)
            result_query_login = login_DB_module(dbConnection,userName.decode('utf-8'),passWord.decode('utf-8'))
            if result_query_login is None:
                with socketConnection:
                    data_send = str.encode("Fail to login. Please check your info again !")
                    socketConnection.send(data_send)
            ID_Returned = result_query_login[0]
            Name_Returned = getName_DB_EmployeeList(dbConnection, ID_Returned)
            user_Name = Name_Returned[0]
            with socketConnection:
                data = "Hello, " + user_Name
                data_send = data.encode()
                socketConnection.send(data_send)

                flag = "Succeed"
                data_send = flag.encode()
                socketConnection.send(data_send)

                choice = socketConnection.recv(1024).decode('utf-8')
                print(choice)

                if choice == "1":
                    print("a")
                elif choice == "2" :
                    received_category_result = socketConnection.recv(1024).decode('utf-8')
                    print(received_category_result)
                    #Call CRYPTO API HERE
                    update_status = update_performed_task(dbConnection, received_category_result, ID_Returned)
                    if update_status == 1:
                        print("Update task successfully")
                    data = str.encode("Data stored successfully !")
                    with socketConnection:
                        socketConnection.send(data)
                elif choice == "3":
                    print("c")
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




