from MySQLdb import cursors, connect
import mysql.connector

def connect_db():
<<<<<<< HEAD
    conn = connect(host = "localhost", user="root", passwd="password", db="db_sister", cursorclass=cursors.DictCursor)
=======
    conn = connect(host = "localhost", user="root", passwd="dragonica025", db="db_sister", cursorclass=cursors.DictCursor)
>>>>>>> 19b48acd42595c7b5ab03967e7c6e61061f822d1
    # curr = conn.cursor()
    return conn
