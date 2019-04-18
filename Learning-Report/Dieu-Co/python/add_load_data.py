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
        conn.execute("PRAGMA foreign_keys = on")
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

def evaluation_form(conn, info):
    sql = '''
        INSERT INTO evaluation_form
        (sup_id,rating,efeedback,eqr_code)
        VALUES(?,?,?,?)
        '''
    cur = conn.cursor()
    cur.execute(sql, info)
    return cur.lastrowid


# -----------------------------------------------------------------------------------

def update_trainee_records(conn, info):
    sql = ''' UPDATE trainee_records
        SET sup_id = ?,
        sup_rating = ?,
        feedback = ?,
        signing_status = ?
        WHERE qr_code = ?
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
            employees(connect, list)
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
            print("TD need to be numbers ! ")
    finished_task = input("input your finished tasks: ")
    self_rating = input("rate your tasks: ")
    sup_id = 0
    with connect:
        try:
            list = (qr_code, id, finished_task, self_rating, sup_id, "NULL", "NULL", "NULL")
            trainee_records(connect, list)
        except Error as e:
            print(e)
            print("fail to add record")


# -----------------------------------------------------------------------------------

def add_evaluation_form():
    path = "D:\\sqlite3\db\data1.db"
    connect = create_connection(path)
    error = 1
    while error == 1:
        qr_code = input("input the record QR code: ")
        try:
            cur = connect.cursor()
            cur.execute("select * from trainee_records WHERE qr_code = ?", [qr_code])
            row2s = cur.fetchall()
            for row2 in row2s:
                print("--------------------------------------------")
                print(row2)
                print("--------------------------------------------")

            error = 0
            break
        except Error as e:
            print(e)
            print("Fail to find the record")
    sup_id = input("input your ID(supervisor): ")
    rating = input("input your rating: ")
    efeedback = input("input your feedback: ")
    with connect:
        try:
            list = (sup_id, rating, efeedback, qr_code)
            evaluation_form(connect, list)
            signing_status = "SIGNED"
            list2 = (sup_id, rating, efeedback, signing_status, qr_code)
            update_trainee_records(connect, list2)
        except Error as e:
            print(e)
            print("fail to add evaluation form")


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

def load_evaluation_form():
    path = "D:\\sqlite3\db\data1.db"
    connect = create_connection(path)
    cur = connect.cursor()
    cur.execute("select * from evaluation_form")
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
        print("----------------------------\n"
              "Code Options:\n"
              "1 => ADD employee\n"
              "2 => SEE employee list\n"
              "3 => ADD record\n"
              "4 => SEE record list\n"
              "5 => RATE a record\n"
              "6 => SEE evaluation form\n"
              "----------------------------\n")
        code = input("input code: ")
        if code == "1":
            add_employee()
        elif code == "2":
            load_employee()
        elif code == "3":
            add_record()
        elif code == "4":
            load_record()
        elif code == "5":
            add_evaluation_form()
        elif code == "6":
            load_evaluation_form()
        else:
            print("wrong code")


# -----------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
