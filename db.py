import sqlite3
from sqlite3 import Error
from datetime import datetime


def create_connection(db_file):
    """ Create a database connection named 'db_file' """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("SQL connection successful") 
    except Error as e:
        print(f"SQL Error>: '{e}")

    return conn


def create_table(conn, db_table):
    """ Create table name 'db_table' with connection 'conn' """

    try:
        c = conn.cursor()
        c.execute(db_table)
    except Error as e:
        print(f"SQL Error>: {e}")


def add_record(conn, data):
    """ Add new record 'data' to the table with connection 'conn' """

    query = """ INSERT INTO person(serial_num,fname,lname,birth_date,
                identification_num,street,city,postcode_num,phone_num,
                note,date_created)
                VALUES(?,?,?,?,?,?,?,?,?,?,?) """
    data.append(str(datetime.now().strftime("%d/%m/%y %H:%M%S.%f")))
    c = conn.cursor()
    c.execute(query, data)
    conn.commit()


def update_record(conn, data):
    """ Update an existing record with new data 'data'
                by 'serial_num' with connection 'conn' """

    query = """ UPDATE person
                SET serial_num = ?,
                    fname = ?,
                    lname = ?,
                    birth_date = ?,
                    identification_num = ?,
                    street = ?,
                    city = ?,
                    postcode_num = ?,
                    phone_num = ?,
                    note = ?
                WHERE serial_num = ? """
    c = conn.cursor()
    c.execute(query, data)
    conn.commit()


def delete_record(conn, id):
    """ Delete an existing record by id 'id'
        with connection 'conn' """
    
    query = "DELETE from person WHERE id=?"
    c = conn.cursor()
    c.execute(query, (id,))
    conn.commit()


def delete_all_records(conn):
    """ Delete all records from table person
        with connection 'conn' """
    
    query = "DELETE FROM person"
    c = conn.cursor()
    c.execute(query)
    conn.commit()


def load_all_records(conn):
    """ Return all data from table person
        with connection 'conn' """
    
    query = "SELECT * FROM person"
    c = conn.cursor()
    c.execute(query)
    
    loaded_data = c.fetchall()
    return loaded_data


def load_exact_record(conn, id):
    """ Return record by id 'id' from table person
        with connection 'conn' """
    
    query = "SELECT * FROM person WHERE id=?"
    c = conn.cursor()
    c.execute(query, id)
    
    loaded_data = c.fetchall()
    return loaded_data


def get_last_record(conn):
    """ Return last record from table 'person'
        with connection 'conn' """

    query = """ SELECT * FROM person
                ORDER BY id DESC 
                LIMIT 1 """
    c = conn.cursor()
    c.execute(query)

    record = c.fetchall()
    if not record:
        return ["", "0"]
    return record[0]    # return only record
    


# db_file = "table.db"
# now = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")

table_person = """ CREATE TABLE IF NOT EXISTS person (
                    id INTEGER PRIMARY KEY,
                    serial_num CHARACTER(5) NOT NULL,
                    fname CHARACTER(30) NOT NULL,
                    lname CHARACTER(30) NOT NULL,
                    birth_date CHARACTER(10) NOT NULL,
                    identification_num CHARACTER(20) NOT NULL,
                    street CHARACTER(30) NOT NULL,
                    city CHARACTER(30) NOT NULL,
                    postcode_num CHARACTER(5) NOT NULL,
                    phone_num CHARACTER(10) NOT NULL,
                    note text,
                    date_created CHARACTER(22)
                ); """