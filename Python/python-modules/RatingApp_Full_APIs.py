from flask import Flask
from flask_restful import Api, Resource, reqparse
import sqlite3
import functools
import operator
import base64
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
app = Flask(__name__)
api = Api(app)
from sqlite3 import Error
import json
def convertTuple(tup):
    str = functools.reduce(operator.add, (tup))
    return str
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

### func 1 ###
def see_record(db_conn, qr_code, date):

    cur = db_conn.cursor()
    cur.execute("select * from traineeRecord where QR_Code=? and Date =?", (qr_code,date,))

    rows = cur.fetchall()
    print("check rows = ",rows)
    for row in rows:
        print(row)
    return row
### ###

### func 2 ###
def add_info(conn, a, b, c, d, e, f, g):
    cur = conn.cursor()
    cur.execute(
        "insert into traineeRecord (Finished_Task,Self_Rating,ID_Supervisor,Date,QR_Code,Signing_Status,Trainee_ID) values(?,?,?,?,?,?,?)",
        (a, b, c, d, e, f, g,))
    return 1

def return_publicKey(db_conn, ID):
    cur = db_conn.cursor()
    cur.execute("SELECT Public_Key FROM employeeList WHERE ID_Employee = ?", (ID,))
    rows = cur.fetchall()
    for row in rows:
        return row
def encryption_module(info,publicKey):
    public_key = RSA.import_key(open(publicKey).read())
    encryptor = PKCS1_OAEP.new(public_key)
    encoded_info = info.encode('utf-8')
    encrypted_info = encryptor.encrypt(encoded_info)
    stored_encrypted_info= base64.b64encode(encrypted_info)
    result = stored_encrypted_info.decode('utf-8')
    return result
####

### func 4
def return_supervisor_ID(db_conn, QR_Code):
    cur = db_conn.cursor()
    cur.execute("select Trainee_ID from traineeRecord where QR_Code = ?", (QR_Code,))
    rows = cur.fetchall()
    for row in rows:
        return row
def add_info_2(conn,a,b,c,d,e,f,g):

    cur = conn.cursor()
    cur.execute("update traineeRecord set Finished_Task = ? , Self_Rating = ? , Supervisor_Rating = ? , Supervisor_FeedBack = ? , Signing_Status = ? , Record_Hashing = ? where QR_Code = ?" ,(a,b,c,d,e,f,g,))
    return 1
####

### func 5 ##
def find_hash(conn, qr_code, trainee_id):
    cur = conn.cursor()
    cur.execute("select Record_Hashing from traineeRecord where QR_Code=? and Trainee_ID=?", (qr_code, trainee_id,))

    rows = cur.fetchall()

    for row in rows:
        return row


def find_employee(conn, id_employee, employee_name):
    cur = conn.cursor()
    cur.execute("select * from employeeList where ID_Employee=? and Employee_Name=?", (id_employee, employee_name,))
    rows = cur.fetchall()
    print(rows)
    if not rows:
        return 0  # there is no employee
    if rows:
        return 1  # there is a employee
####
class User(Resource):
    def get(self, name): #name is the required condition.
        parser = reqparse.RequestParser()
        if name == "condition1":
            parser.add_argument("QR_Code")
            parser.add_argument("Date")
            args = parser.parse_args()
            QR_Code = args["QR_Code"]
            Date = args["Date"]
            linkpath = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\RatingApp.db"
            conn = create_connection(linkpath)
            a = see_record(conn, QR_Code, Date)

            if a != '':
                return a, 200
            return 0, 404

        elif name=="employee":
            parser.add_argument("ID_Employee")
            parser.add_argument("Employee_Name")
            args = parser.parse_args()
            ID_Employee = args["ID_Employee"]
            Employee_Name = args["Employee_Name"]
            print(ID_Employee)
            print(Employee_Name)
            linkpath = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\RatingApp.db"
            conn = create_connection(linkpath)
            return_employee = find_employee(conn, ID_Employee, Employee_Name)
            return_employee = str(return_employee)

            if return_employee != '':
                employee_result = int(return_employee)
                print(type(employee_result))
                return employee_result
            return 0

        elif name=="hash":
                parser.add_argument("QR_Code")
                parser.add_argument("Trainee_ID")
                args = parser.parse_args()
                Trainee_ID = args["Trainee_ID"]
                QR_Code = args["QR_Code"]
                linkpath = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\RatingApp.db"
                conn = create_connection(linkpath)
                return_hash = find_hash(conn, QR_Code, Trainee_ID)
                return_hash = convertTuple(return_hash)
                print(return_hash)
                if return_hash != '':
                    return return_hash, 200  # send the hash to client request
                return 0, 404
    def put(self, name):
        parser = reqparse.RequestParser()
        if name == "condition2":
            parser.add_argument("Trainee_ID")
            parser.add_argument("Finished_Task")
            parser.add_argument("Self_Rating")
            parser.add_argument("ID_Supervisor")
            parser.add_argument("Date")
            parser.add_argument("QR_Code")
            parser.add_argument("Signing_Status")
            args = parser.parse_args()
            Trainee_ID = args["Trainee_ID"]
            print(Trainee_ID)
            Finished_Task = args["Finished_Task"]
            Self_Rating = args["Self_Rating"]
            ID_Supervisor = args["ID_Supervisor"]
            Date = args["Date"]
            QR_Code = args["QR_Code"]
            Signing_Status = args["Signing_Status"]
            linkpath = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\RatingApp.db"
            conn = create_connection(linkpath)
            with conn:
                querying_publicKey = return_publicKey(conn, ID_Supervisor)  #
                toString_publicKey = convertTuple(querying_publicKey)
                encrypted_finished_task = encryption_module(Finished_Task, toString_publicKey)
                encrypted_self_rating = encryption_module(Self_Rating, toString_publicKey)
                ##
                result = add_info(conn, encrypted_finished_task, encrypted_self_rating, ID_Supervisor,Date, QR_Code, Signing_Status, Trainee_ID)
                print(result)
                if result == 1:
                    return 200
        elif name == "condition4":
            parser.add_argument("QR_Code")
            parser.add_argument("Finished_Task")
            parser.add_argument("Self_Rating")
            parser.add_argument("Supervisor_Rating")
            parser.add_argument("Supervisor_FeedBack")
            parser.add_argument("Signing_Status")
            parser.add_argument("Record_Hashing")
            args = parser.parse_args()
            QR_Code = args["QR_Code"]
            Finished_Task = args["Finished_Task"]
            Self_Rating = args["Self_Rating"]
            Supervisor_Rating = args["Supervisor_Rating"]
            Supervisor_Feedback = args["Supervisor_FeedBack"]
            Signing_Status = args["Signing_Status"]
            Record_Hashing = args["Record_Hashing"]
            linkpath = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\RatingApp.db"
            conn = create_connection(linkpath)
            with conn:
                Trainee_ID = return_supervisor_ID(conn, QR_Code)  # return result is always in tuple type.
                Trainee_ID = convertTuple(Trainee_ID)  # 2001
                publicKey = return_publicKey(conn, Trainee_ID)
                toStringPublicKey = convertTuple(publicKey)

                encrypted_finished_task = encryption_module(Finished_Task, toStringPublicKey)
                encrypted_self_rating = encryption_module(Self_Rating, toStringPublicKey)
                encrypted_supervisor_rating = encryption_module(Supervisor_Rating, toStringPublicKey)
                encrypted_feedback = encryption_module(Supervisor_Feedback, toStringPublicKey)

                result = add_info_2(conn, encrypted_finished_task, encrypted_self_rating, encrypted_supervisor_rating,
                                  encrypted_feedback, Signing_Status, Record_Hashing, QR_Code)
                if result == 1:
                    return 200

api.add_resource(User, "/user/<string:name>")
if __name__ == "__main__":
    app.run(debug=True)