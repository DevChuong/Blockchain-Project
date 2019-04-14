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


def employees(conn, info):
    sql = '''
        INSERT INTO employeeList
        (id,name,DOB,role,public_key)
        VALUES(?,?,?,?,?)
        '''
    cur = conn.cursor()
    cur.execute(sql, info)
    return cur.lastrowid


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
            print("That's not an int!")
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
            print("Role need to be trainee or supervisor only")

    public_key = input("input Employee public key: ")
    with connect:
        list = (id, name, DOB, role, public_key)
        employees(connect, list)


#def load_employee()
#    path = "D:\\sqlite3\db\data1.db"
 #   connect = create_connection(path)
 #  with connect:


def main():
    add_employee()


if __name__ == '__main__':
    main()
