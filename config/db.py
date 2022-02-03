from MySQLdb import cursors, connect
# import mysql.connector

def connect_db():

    conn = connect(host = "localhost",port=3306 , user="root", passwd="dragonica025", db="db_sister", cursorclass=cursors.DictCursor)

    # curr = conn.cursor()
    return conn
