import socket
import sqlite3
from sqlite3 import Error
import os
import functools
import operator
import json
import pickle
def convertTuple(tup):
    str = functools.reduce(operator.add, (tup))
    return str
HOST = '127.0.0.1'
PORT = 9696
def create_connection(db_file):

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None
def find_hash(conn,qr_code,trainee_id):
    cur = conn.cursor()
    cur.execute("select Record_Hashing from traineeRecord where QR_Code=? and Trainee_ID=?", (qr_code,trainee_id,))

    rows = cur.fetchall()
    for row in rows:
        print(row)
    return row

def find_employee(conn,id_employee,employee_name):

    cur = conn.cursor()
    cur.execute("select * from employeeList where ID_Employee=? and Employee_Name=?", (id_employee, employee_name,))
    rows = cur.fetchall()
    print(rows)
    if not rows:
        return 0 # there is no employee
    if rows:
        return 1 # there is a employee

    # return 1 or 0

def check_hash(conn,QR_Code):
    cur = conn.cursor()
    cur.execute("select Record_Hashing from traineeRecord where QR_Code = ?",(QR_Code,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    return row

def ListenAgain():
    socket.listen()
    connection, addr = socket.accept()
    with connection:
        print('Connected by :', addr)
        while True:
            data_receive = connection.recv(1024).decode('utf-8')
            print(data_receive)

            print("//")
            if not data_receive:
                continue
            if data_receive == "Get_Hash":
                with connection:
                    connection.send(data_receive.encode())

                    Trainee_ID = connection.recv(1024).decode('utf-8')  # receive Trainee ID
                    print(Trainee_ID)

                    QR_Code = connection.recv(1024).decode('utf-8')  # receive QR Code
                    print(QR_Code)

                    ##

                    # now you have QR code and Trainee ID, use them to get the hash
                    linkpath = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\RatingApp.db"
                    conn = create_connection(linkpath)
                    return_hash = find_hash(conn, QR_Code, Trainee_ID)
                    print(return_hash)  # tuple
                    return_hash = convertTuple(return_hash)
                    print(return_hash)
                    print(type(return_hash))

                    data_send = return_hash.encode()  # put your hash in here
                    print(data_send)
                    with connection:
                        connection.send(data_send)
                        ListenAgain()
            elif data_receive == "Get_employee":
                with connection:
                    connection.send(data_receive.encode())

                    ID_Employee = connection.recv(1024).decode('utf-8')  # receive ID Employee
                    print(ID_Employee)

                    Employee_Name = connection.recv(1024).decode('utf-8')  # receive Employee name
                    print(Employee_Name)

                    # now you have QR code and Trainee ID, use them to get the hash
                    linkpath = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\RatingApp.db"
                    conn = create_connection(linkpath)
                    return_employee = find_employee(conn, ID_Employee, Employee_Name)
                    return_employee = str(return_employee)
                    with connection:
                        connection.send(return_employee.encode())
                        ListenAgain()

            elif data_receive == "Get_checkHash":
                with connection:
                    connection.send(data_receive.encode())

                    QR_Code = connection.recv(1024).decode('utf-8')
                    linkpath = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\RatingApp.db"
                    conn = create_connection(linkpath)
                    hash_returned = check_hash(conn,QR_Code)

                    hash_returned = convertTuple(hash_returned)
                    with connection:
                        connection.send(hash_returned.encode())
                        ListenAgain()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
    socket.bind((HOST, PORT))
    print("Đang lắng nghe các kết nối ...")
    socket.listen()
    connection, addr = socket.accept()
    with connection:
        print('Connected by :', addr)
        while True:
            data_receive = connection.recv(1024).decode('utf-8')
            print(data_receive)

            print("//")
            if not data_receive:
                continue
            if data_receive == "Get_Hash":
                with connection:
                    connection.send(data_receive.encode())

                    Trainee_ID = connection.recv(1024).decode('utf-8')  # receive Trainee ID
                    print(Trainee_ID)

                    QR_Code = connection.recv(1024).decode('utf-8')  # receive QR Code
                    print(QR_Code)

                    ##

                    # now you have QR code and Trainee ID, use them to get the hash
                    linkpath = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\RatingApp.db"
                    conn = create_connection(linkpath)
                    return_hash = find_hash(conn, QR_Code, Trainee_ID)
                    print(return_hash)  # tuple
                    return_hash = convertTuple(return_hash)
                    print(return_hash)
                    print(type(return_hash))

                    data_send = return_hash.encode()  # put your hash in here
                    print(data_send)
                    with connection:
                        connection.send(data_send)
                        ListenAgain()
            elif data_receive == "Get_employee":
                with connection:
                    connection.send(data_receive.encode())

                    ID_Employee = connection.recv(1024).decode('utf-8')  # receive ID Employee
                    print(ID_Employee)

                    Employee_Name = connection.recv(1024).decode('utf-8')  # receive Employee name
                    print(Employee_Name)

                    # now you have QR code and Trainee ID, use them to get the hash
                    linkpath = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\RatingApp.db"
                    conn = create_connection(linkpath)
                    return_employee = find_employee(conn, ID_Employee, Employee_Name)
                    return_employee = str(return_employee)
                    with connection:
                        connection.send(return_employee.encode())
                        ListenAgain()
            elif data_receive == "Get_checkHash":
                with connection:
                    connection.send(data_receive.encode())

                    QR_Code = connection.recv(1024).decode('utf-8')
                    linkpath = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\RatingApp.db"
                    conn = create_connection(linkpath)
                    hash_returned = check_hash(conn, QR_Code)

                    hash_returned = convertTuple(hash_returned)
                    with connection:
                        connection.send(hash_returned.encode())
                        ListenAgain()
os.system("pause")