from flask import Flask
from flask_restful import Api, Resource, reqparse
import sqlite3
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

from sqlite3 import Error
import json

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def add_info(conn,a,b,c,d,e,f):

    cur = conn.cursor()
    cur.execute("insert into traineeRecord (Finished_Task,Self_Rating,ID_Supervisor,QR_Code,Signing_Status,Trainee_ID) values(?,?,?,?,?,?)" ,(a,b,c,d,e,f,))
    return 1

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# connect to the SQlite databases
connection = sqlite3.connect("C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\King.db")
connection.row_factory = dict_factory
app = Flask(__name__)
api = Api(app)
cursor1 = connection.cursor()
cursor1.execute("select name from sqlite_master where name='traineeRecord';")
a = cursor1.fetchall()
print("///")
for table_name in a:
        # table_name = table_name[0]
        print(table_name['name'])

        conn = sqlite3.connect(
            "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\King.db")
        conn.row_factory = dict_factory

        cur1 = conn.cursor()

        cur1.execute("SELECT * FROM " + table_name['name'])

        # fetch all or one we'll go for all.

        results = cur1.fetchall()

        print(json.dumps(results))

        # generate and save JSON files with the table name for each of the database tables
        with open(table_name['name'] + '.json', 'a') as the_file:
            the_file.write(format(results).replace(" u'", "'").replace("'", "\""))
print("///")
print("now in users")
class User(Resource):
    def get(self, name):
        for user in results:
            if (name == user["qr_code"]):
                return user, 200
        return "GET : User not found", 404

    def put(selfself,name):
        parser = reqparse.RequestParser()
        parser.add_argument("Finished_Task")
        parser.add_argument("Self_Rating")
        parser.add_argument("ID_Supervisor")
        parser.add_argument("QR_Code")
        parser.add_argument("Signing_Status")
        args = parser.parse_args()
        linkpath = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\King.db"
        conn = create_connection(linkpath)
        with conn:
            ##
            result = add_info(conn, args["Finished_Task"], args["Self_Rating"], args["ID_Supervisor"], args["QR_Code"], args["Signing_Status"], name)
            if result == 1:
                return 200
api.add_resource(User, "/user/<string:name>")

app.run(debug=True)

