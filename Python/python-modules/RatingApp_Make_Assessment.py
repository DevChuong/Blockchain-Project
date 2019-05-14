from flask import Flask
from flask_restful import Api, Resource, reqparse
import sqlite3
import functools
import operator
import base64
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
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


def add_info(conn,a,b,c,d,e,f,g):

    cur = conn.cursor()
    cur.execute("update traineeRecord set Finished_Task = ? , Self_Rating = ? , Supervisor_Rating = ? , Supervisor_FeedBack = ? , Signing_Status = ? , Record_Hashing = ? where QR_Code = ?" ,(a,b,c,d,e,f,g,))
    return 1

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def return_supervisor_ID(db_conn, QR_Code):
    cur = db_conn.cursor()
    cur.execute("select Trainee_ID from traineeRecord where QR_Code = ?", (QR_Code,))
    rows = cur.fetchall()
    for row in rows:
        return row

def return_publicKey(db_conn, ID):
    cur = db_conn.cursor()
    cur.execute("SELECT Public_Key FROM employeeList WHERE ID_Employee = ?", (ID,))

    rows = cur.fetchall()

    for row in rows:
        return row

def convertTuple(tup):
    str = functools.reduce(operator.add, (tup))
    return str

def encryption_module(info,publicKey):
    public_key = RSA.import_key(open(publicKey).read())
    encryptor = PKCS1_OAEP.new(public_key)
    encoded_info = info.encode('utf-8')
    encrypted_info = encryptor.encrypt(encoded_info)
    stored_encrypted_info= base64.b64encode(encrypted_info)
    result = stored_encrypted_info.decode('utf-8')
    return result

# connect to the SQlite databases
connection = sqlite3.connect("C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\RatingApp.db")
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
            "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\RatingApp.db")
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
        parser.add_argument("Supervisor_Rating")
        parser.add_argument("Supervisor_FeedBack")
        parser.add_argument("Signing_Status")
        parser.add_argument("Record_Hashing")
        args = parser.parse_args()

        linkpath = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\RatingApp.db"
        conn = create_connection(linkpath)
        with conn:
            ##
            print(name) # 69145
            print(type(name))
            Trainee_ID = return_supervisor_ID(conn,name)     # return result is always in tuple type.
            print(Trainee_ID) # (2001,) in tuple form, must convert to string.
            print(type(Trainee_ID))
            Trainee_ID = convertTuple(Trainee_ID)       # 2001
            publicKey = return_publicKey(conn,Trainee_ID)
            toStringPublicKey = convertTuple(publicKey)
            print(toStringPublicKey)
            encrypted_finished_task = encryption_module(args["Finished_Task"],toStringPublicKey)
            encrypted_self_rating = encryption_module(args["Self_Rating"],toStringPublicKey)
            encrypted_supervisor_rating = encryption_module(args["Supervisor_Rating"],toStringPublicKey)
            encrypted_feedback = encryption_module(args["Supervisor_FeedBack"],toStringPublicKey)

            result = add_info(conn, encrypted_finished_task, encrypted_self_rating, encrypted_supervisor_rating, encrypted_feedback,args["Signing_Status"], args["Record_Hashing"], name)
            if result == 1:
                return 200
api.add_resource(User, "/user/<string:name>")

app.run(debug=True)

