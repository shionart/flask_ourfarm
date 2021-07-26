from flask import Flask
from flask_cors import CORS
import socket
import platform

main = Flask(__name__,template_folder='../templates', static_folder='../static')
cors = CORS(main)

# scheduler = BackgroundScheduler()

main.secret_key="081213342244"
# main.config
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
os = platform.system()
# Please do connect your internet while setting up this at first time
if os =="Linux":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()

