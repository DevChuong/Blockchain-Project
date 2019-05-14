import sqlite3

from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

import functools
import operator

def convertTuple(tup):
    str = functools.reduce(operator.add, (tup))
    return str

def find_hash(conn,qr_code,trainee_id):
    cur = conn.cursor()
    cur.execute("select Record_Hashing from traineeRecord where QR_Code=? and Trainee_ID=?", (qr_code,trainee_id,))

    rows = cur.fetchall()
    
    for row in rows:
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
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

class User(Resource):

    def get(self, name): # name = QR
        parser = reqparse.RequestParser()
        if name=="employee":
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
api.add_resource(User, '/user/<string:name>')
if __name__ == "__main__":
    app.run(debug=True)