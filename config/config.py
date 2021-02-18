from flask import Flask
from flask_cors import CORS
import socket

# from apscheduler.schedulers.background import BackgroundScheduler

main = Flask(__name__,template_folder='../templates', static_folder='../static')
cors = CORS(main)

# scheduler = BackgroundScheduler()

main.secret_key="081213342244"
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)