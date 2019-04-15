import sqlite3
from sqlite3 import Error


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


# -----------------------------------------------------------------------------------

def employees(conn, info):
    sql = '''
        INSERT INTO employees
        (id,name,DOB,role,pub_key)
        VALUES(?,?,?,?,?)
        '''
    cur = conn.cursor()
    cur.execute(sql, info)
    return cur.lastrowid


# -----------------------------------------------------------------------------------

def trainee_records(conn, info):
    sql = '''
        INSERT INTO trainee_records
        (qr_code,trainee_id,finished_task,self_rating,sup_id,sup_rating,feedback,signing_status)
        VALUES(?,?,?,?,?,?,?,?)
        '''
    cur = conn.cursor()
    cur.execute(sql, info)
    return cur.lastrowid


# -----------------------------------------------------------------------------------

def add_employee():
    path = "D:\\sqlite3\db\data1.db"
    connect = create_connection(path)
    error = 1
    while error == 1:
        id = input("input Employee ID: ")
        try:
            val = int(id)
            print("success input ID: ", val)
            error = 0
            break
        except ValueError:
            print("TD neetd to be numbers ! ")
    name = input("input Employee name: ")
    DOB = input("input Employee DOB: ")
    error = 1
    while error == 1:
        role = input("input Employee role: ")
        if role == "trainee" or role == "supervisor":
            print("success input role: ", role)
            error = 0
            break
        else:
            print("Role need to be trainee or supervisor only ! ")

    public_key = input("input Employee public key: ")
    with connect:
        try:
            list = (id, name, DOB, role, public_key)
            trainee_records(connect, list)
        except Error as e:
            print(e)
            print("fail to add employee")


# -----------------------------------------------------------------------------------

def add_record():
    path = "D:\\sqlite3\db\data1.db"
    connect = create_connection(path)
    error = 1
    qr_code = input("input record QR CODE: ")
    while error == 1:
        id = input("input your ID(trainee): ")
        try:
            val = int(id)
            print("success input ID: ", val)
            error = 0
            break
        except ValueError:
            print("TD neetd to be numbers ! ")
    finished_task = input("input your finished tasks: ")
    self_rating = input("rate your tasks: ")
    with connect:
        try:
            list = (id, finished_task, self_rating, "NULL", "NULL", "NULL", "NULL", "NULL")
            trainee_records(connect, list)
        except Error as e:
            print(e)
            print("fail to add record")


# -----------------------------------------------------------------------------------

def load_record():
    path = "D:\\sqlite3\db\data1.db"
    connect = create_connection(path)
    cur = connect.cursor()
    cur.execute("select * from trainee_records")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    return row


# -----------------------------------------------------------------------------------

def load_employee():
    path = "D:\\sqlite3\db\data1.db"
    connect = create_connection(path)
    cur = connect.cursor()
    cur.execute("select * from employees")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    return row


# -----------------------------------------------------------------------------------

def main():
    run = 1
    while run == 1:
        code = input("input code: ")
        if code == "1":
            add_employee()
        elif code == "2":
            load_employee()
        elif code == "3":
            add_record()
        elif code == "4":
            load_record()
        else:
            print("wrong code")


# -----------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
