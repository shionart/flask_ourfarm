from MySQLdb import cursors, connect
from dotenv import load_dotenv
import os

load_dotenv()

# import mysql.connector

def connect_db():

    conn = connect(host =os.getenv('DB_HOST'), port =int(os.getenv('DB_PORT')) , user= os.getenv('DB_USER') , passwd=os.getenv('DB_PASSWORD'), db=os.getenv('DB_SCHEMA'), cursorclass=cursors.DictCursor)
    # conn = connect(host = "localhost",port=3306 , user="root", passwd="140692", db="db_sister", cursorclass=cursors.DictCursor)

    # curr = conn.cursor()
    return conn
