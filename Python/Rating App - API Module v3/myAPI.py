HOST = '127.0.0.1'
PORT = 9696
import json
import sqlite3

from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)
def create_connection(db_file):

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def check_hash(hash1,hash2):
    if hash1 == hash2:
        return 1
    else:
        return 0

import socket

class User(Resource):

    def get(self, name): # the name object is the condition that be chosen for hash check or employee check
        parser = reqparse.RequestParser()
        if name=="check":
            parser.add_argument("ID_Employee")
            parser.add_argument("Employee_Name")
            args = parser.parse_args()
            Trainee_ID = args["ID_Employee"]
            Employee_Name = args["Employee_Name"]
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((HOST, PORT))

                data_send = str.encode('Get_employee')
                sock.sendall(data_send)
                data_receive = sock.recv(1024).decode('utf-8')
                if data_receive == 'Get_employee':
                    send_Trainee_ID = str.encode(Trainee_ID)
                    sock.send(send_Trainee_ID)

                    send_Employee_Name = str.encode(Employee_Name)

                    sock.sendall(send_Employee_Name)

                    data_receive = sock.recv(1024).decode('utf-8')
                    print(data_receive)

                    employee_result = data_receive
                if employee_result != '':
                    employee_result = int(employee_result)
                    print(type(employee_result))
                    return employee_result
                return 0, 404

        elif name=="hash":
                parser.add_argument("Trainee_ID")
                parser.add_argument("QR_Code")
                args = parser.parse_args()
                Trainee_ID = args["Trainee_ID"]
                QR_Code = args["QR_Code"]
                print(Trainee_ID)
                print(QR_Code)
                _hashing = ''
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((HOST, PORT))

                    data_send = str.encode('Get_Hash')
                    sock.sendall(data_send)
                    data_receive = sock.recv(1024).decode('utf-8')
                    if data_receive == 'Get_Hash':

                    #    send_name = str.encode(name)
                     #   sock.send(send_name)

                        send_Trainee_ID = str.encode(Trainee_ID)

                     #   check_received = sock.recv(1024).decode('utf-8')

                        sock.sendall(send_Trainee_ID)
                        send_QR_Code = str.encode(QR_Code)
                        sock.sendall(send_QR_Code)

                        data_receive = sock.recv(1024).decode('utf-8')  # receive the hash in here
                        print(data_receive)

                        _hashing = data_receive
                        print(_hashing)
                        print(type(_hashing))

                    if _hashing != '':

                        return _hashing, 200  # send the hash to client request
                    return 0, 404
        elif name=="checkHash":
            parser.add_argument("QR_Code")
            parser.add_argument("Record_Hashing")
            args = parser.parse_args()

            QR_Code = args["QR_Code"]
            Record_Hashing = args["Record_Hashing"]

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((HOST, PORT))

                data_send = str.encode('Get_checkHash')
                sock.sendall(data_send)
                data_receive = sock.recv(1024).decode('utf-8')
                if data_receive == 'Get_checkHash':
                    sock.sendall(QR_Code.encode())
                    data_receive = sock.recv(1024).decode('utf-8')
                    result = check_hash(Record_Hashing,data_receive)
                    print(result)
                if result != '':
                    return str(result), 200

                return 0, 404

api.add_resource(User, '/user/<string:name>')

if __name__ == "__main__":
    app.run(debug=True)