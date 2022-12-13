from MySQLdb import cursors, connect
from dotenv import load_dotenv
import os

# import mysql.connector

def connect_db():

    conn = connect(host =os.getenv('DB_HOST'), port =int(os.getenv('DB_PORT')) , user= os.getenv('DB_USER') , passwd=os.getenv('DB_PASSWORD'), db=os.getenv('DB_SCHEMA'), cursorclass=cursors.DictCursor)

    return conn
