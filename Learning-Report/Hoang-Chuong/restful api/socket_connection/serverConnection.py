import socket
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask import jsonify
import sqlite3
import json

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

def SearchUserByInput(db_conn, priority):

    cur = db_conn.cursor()
    cur.execute("select * from tracks where TrackID=?", (priority,))

    rows = cur.fetchall()
    for row in rows:
        print(row)
        return row

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("Server is now listening for a client.")
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            database = "C:\\Users\HoangChuong\Documents\Sqlite3\sqlite-tools-win32-x86-3270200\sqlite-tools-win32-x86-3270200\db\chinook.db"
            db_conn = database_connection(database)
            with conn:
                conn.sendall(str.encode(json.dumps(SearchUserByInput(db_conn, data.decode('utf-8')))))

