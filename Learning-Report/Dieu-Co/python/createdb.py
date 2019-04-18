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


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys=ON")
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "D:\\sqlite3\db\data1.db"
    sql_create_employees_table = """ CREATE TABLE IF NOT EXISTS employees (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        DOB text NOT NULL,
                                        role text NOT NULL,
                                        pub_key text NOT NULL
                                    ); """

    sql_create_trainee_records_table = """CREATE TABLE IF NOT EXISTS trainee_records (
                                    qr_code text PRIMARY KEY,
                                    trainee_id integer NOT NULL,
                                    finished_task text NOT NULL,
                                    self_rating text NOT NULL,
                                    sup_id integer NOT NULL,
                                    sup_rating text,
                                    feedback text,
                                    signing_status text,
                                    FOREIGN KEY (sup_id) REFERENCES employees (id),                                    
                                    FOREIGN KEY (trainee_id) REFERENCES employees (id)
                                );"""
    sql_create_evaluation_form_table = """CREATE TABLE IF NOT EXISTS evaluation_form (
                                    sup_id integer NOT NULL,
                                    rating text,
                                    efeedback text,
                                    eqr_code text NOT NULL,
                                    FOREIGN KEY (eqr_code) REFERENCES trainee_records (qr_code),
                                    FOREIGN KEY(sup_id) REFERENCES employees (id)
                                );"""
    # create a database connection
    conn = create_connection(database)
    conn.execute("PRAGMA foreign_keys = on")
    if conn is not None:
        # create employees table
        create_table(conn, sql_create_employees_table)
        # create trainee_records table
        create_table(conn, sql_create_trainee_records_table)
        # create evaluation form table
        create_table(conn, sql_create_evaluation_form_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
