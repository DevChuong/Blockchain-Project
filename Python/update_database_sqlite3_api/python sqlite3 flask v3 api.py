from flask import Flask
from flask_restful import Api, Resource, reqparse
import sqlite3
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

def add_info(conn,project):
    sql = ''' UPDATE traineeRecord SET supervisor_rating = ?, feedback = ? WHERE qr_code = ? '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# connect to the SQlite databases
connection = sqlite3.connect("C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\Merely.db")
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
            "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\Merely.db")
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
        parser.add_argument("supervisor_rating")
        parser.add_argument("feedback")
        args = parser.parse_args()
        linkpath = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\Merely.db"
        conn = create_connection(linkpath)
        with conn:
            info = (args["supervisor_rating"],args["feedback"],name)
            add_info(conn, info)


api.add_resource(User, "/user/<string:name>")

app.run(debug=True)