from MySQLdb import cursors, connect
import mysql.connector

def connect_db():
    conn = connect(host = "localhost", user="root", passwd="password", db="db_sister", cursorclass=cursors.DictCursor)
    # curr = conn.cursor()
    return conn