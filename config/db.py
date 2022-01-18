from MySQLdb import cursors, connect
# import mysql.connector

def connect_db():

    conn = connect(host = "192.168.1.50",port=3306 , user="user", passwd="password", db="db_sister", cursorclass=cursors.DictCursor)

    # curr = conn.cursor()
    return conn
