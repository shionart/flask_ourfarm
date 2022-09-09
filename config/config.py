from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
import socket
import platform
import logging
import os

load_dotenv()

main = Flask(__name__,template_folder='../templates', static_folder='../static')
cors = CORS(main)

# scheduler = BackgroundScheduler()

# main.secret_key="081213342244"
main.secret_key=os.getenv('SECRET_KEY')
# main.env="development" #buat # adjust as appropriate
main.env=os.getenv('ENV')
# main.debug=True
main.debug=os.getenv('DEBUG')
# main.config.from_envvar('env')
# main.config
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
ops = platform.system()
# Please do connect your internet while setting up this at first time
if ops =="Linux":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80)) #how to get local ip_address without connect to internet
    ip_address = s.getsockname()[0]
    s.close()

