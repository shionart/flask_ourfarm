# Dependencies
from flask import Flask, render_template, request, make_response, abort, redirect, url_for, jsonify, session, flash
import json
import time
from datetime import datetime
from statistics import mean
import math
from functools import wraps
from MySQLdb import cursors, connect
import mysql.connector
from flask_cors import CORS, cross_origin
import socket

# import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

main = Flask(__name__)
cors = CORS(main)

scheduler = BackgroundScheduler()

main.secret_key="081213342244"
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)