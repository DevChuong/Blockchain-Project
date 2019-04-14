from flask import Flask
from flask_restful import Api, Resource, reqparse
import socket

import sqlite3
from sqlite3 import Error

app = Flask(__name__)
api = Api(app)

data_return = ''

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

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def retrieve_ciphered_id(db_conn, priority):

    cur = db_conn.cursor()
    cur.execute("select * from traineeRecord where qr_code=?", (priority,))

    rows = cur.fetchall()
    for row in rows:
        print(row)
        return row

class User(Resource):
    def get(self, name):


            #################
        database = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\Merely.db"
        db_conn = create_connection(database)
        a = retrieve_ciphered_id(db_conn, name)

        if a != '':
            return a, 200
        return "No data returned", 404
api.add_resource(User, "/user/<string:name>")

app.run(debug=True)
