from flask import Flask
from flask_restful import Api, Resource, reqparse
import socket

import sqlite3
from sqlite3 import Error

app = Flask(__name__)
api = Api(app)

data_return = ''

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def see_record(db_conn, qr_code, date):

    cur = db_conn.cursor()
    cur.execute("select * from traineeRecord where QR_Code=? and Date =?", (qr_code,date,))

    rows = cur.fetchall()
    print("check rows = ",rows)
    for row in rows:
        print(row)
    return row

class User(Resource):
    def get(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("Date")
        args = parser.parse_args()
        print("name = ",name)
        print("args = ",args["Date"])
        database = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\RatingApp.db"
        db_conn = create_connection(database)
        a = see_record(db_conn, name, args["Date"])

        if a != '':
            return a, 200
        return "No data returned", 404
api.add_resource(User, "/user/<string:name>")

app.run(debug=True)