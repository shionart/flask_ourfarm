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


main = Flask(__name__)
cors = CORS(main)

main.secret_key="081213342244"
# non-route function
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

    # DB_connect
def connect_db():
    conn = connect(host = "localhost", user="root", passwd="", db="db_sister", cursorclass=cursors.DictCursor)
    return conn

#Cek login atau tidak
def login_required(f):
    @wraps(f)
    def login_handler(*args,**kwargs):
        if 'email_user' in session:
            return f(*args, **kwargs)
        else :
            flash("Please Login First!", "alert-warning")
            return redirect(url_for('login'))
    return login_handler

#  ======= CRUD TABLE SENSOR =========
# ------insert to table sensor------
# @main.route('/inserttabel/<suhu>/<lembap>/<sm>/<rel>')
def insert_to_table(suhu,lembap,sm,rel,id_arduino,nama):
    conn = connect_db()
    baca_suhu=suhu
    baca_lembap=lembap
    try:
        if math.isnan(suhu) or math.isnan(lembap) :
            suhu=100
            lembap=100
        cek = conn.cursor()
        cursor = conn.cursor()
        query = "INSERT INTO sensor (suhu, kelembapan, soil_moist, relay, id_arduino) VALUES (%s, %s, %s, %s, %s)"
        tuple = (suhu, lembap, sm, rel, id_arduino)
        try:
            print("Eksekusi insert to table")
            cursor.execute("INSERT INTO sensor (suhu, kelembapan, soil_moist, relay, id_arduino) VALUES (%s, %s, %s, %s, %s)",[suhu, lembap, sm, rel, id_arduino])
            # Auto Add Arduino
            cek_control = read_control_id(id_arduino)
            if cek_control == None :
                print("Eksekusi insert to control")
                cek.execute("INSERT INTO control (id_arduino, nama) VALUES(%s,%s)",[id_arduino,nama])
            # Auto Add selesai
            conn.commit()
        except Exception as error:
            print("error {}".format(error))
            conn.rollback()
        print("Data berhasil dimasukkan")
        print("Data DHT: {}, {}, data sm: {}, data id_arduino:{}".format(baca_suhu,baca_lembap,sm,id_arduino))
    except Error as error:
        print("Gagal memasukkan data {}".format(error))
    finally:
        if (conn):
            cursor.close()
            conn.close()
            print("MySql ditutup")
    return "selesai"

# -----baca tabel Sensor-----
def read_sensor(id_arduino):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensor WHERE id_arduino=%s ORDER BY time DESC",[id_arduino])
    data = cur.fetchall()
    sensor = get_sensor(data)
    top_data = read_top(sensor)
    curr_data = sensor[0]
    return sensor, curr_data, top_data

# Fungsi biar ga mentahan dari db
def get_sensor(data):
    li = []
    for dat in data:
        di = {}
        waktu = dat['time']
        tanggal = waktu.strftime("%Y/%m/%d")
        jam = waktu.strftime("%H:%M:%S")
        di['tanggal'] = tanggal
        di['jam'] = jam
        di['suhu'] = dat['suhu']
        di['lembap'] = dat['kelembapan']
        di['sm'] = dat['soil_moist']
        di['relay'] = dat['relay']
        di['id']=dat['id']
        li.append(di)
    return li

# fungsi untuk ngambil data perbandingan
#@main.route('/yesterday',methods=["GET"])
def read_yesterday(id_arduino):
    conn = connect_db()
    cur = conn.cursor()
    #ini tambahan
    try:
        cur.execute("SELECT * FROM sensor WHERE DATE(time) = DATE(NOW() - INTERVAL 3 DAY) order by id desc")
        data = cur.fetchall()
        sensor = get_sensor(data)
        y_suhu, y_lembap, y_sm = mean_yesterday(sensor)
    except:
        y_suhu = 0
        y_lembap = 0
        y_sm = 0
    #tambah end
    sensor,curr_data,bar = read_sensor(id_arduino)
    #tambahan - edit
    if y_suhu != 0:
        suhu_yes=((curr_data['suhu']-y_suhu)/y_suhu)
        suhu_yes = suhu_yes * 100
    else:
        suhu_yes = 0
    if y_lembap != 0:
        lembap_yes=((curr_data['lembap']-y_lembap)/y_lembap)
        lembap_yes = lembap_yes * 100
    else:
        lembap_yes = 0
    if y_sm != 0:
        sm_yes = ((curr_data['sm']-y_sm)/y_sm)
        sm_yes = sm_yes * 100
    else:
        sm_yes = 0
    # tambah -edit end
    sign = lambda x: (1, 0)[x <= 0]
    yesterday = dict()
    yesterday['suhu'] = {'nilai':float(round(suhu_yes,2)),'sign':sign(suhu_yes)}
    yesterday['lembap'] = {'nilai':float(round(lembap_yes,2)), 'sign':sign(lembap_yes)}
    yesterday['sm'] = {'nilai':float(round(sm_yes,2)), 'sign':sign(sm_yes)}
    #return jsonify({'suhu':suhu_yes,'lembap':lembap_yes,'sm':sm_yes})
    return yesterday

def mean_yesterday(sensors):
    list_suhu = []
    list_lembap = []
    list_sm = []
    for sensor in sensors:
        list_suhu.append(sensor['suhu'])
        list_lembap.append(sensor['lembap'])
        list_sm.append(sensor['sm'])
    mean_suhu = mean(list_suhu)
    mean_lembap = mean(list_lembap)
    mean_sm = mean(list_sm)
    return mean_suhu,mean_lembap,mean_sm

def read_top(data):
    top = data[:10]
    top = top[::-1]
    ret = {}
    li_suhu = []
    li_lembap = []
    li_sm = []
    li_relay = []
    li_cahaya = []
    for i in top:
       li_suhu.append(i['suhu'])
       li_lembap.append(i['lembap'])
       li_sm.append(i['sm'])
       li_relay.append(i['relay'])
    ret = {
           'suhu':li_suhu,
           'lembap':li_lembap,
           'sm':li_sm,
           'relay':li_relay
          }
    return ret


# ========CRUD TABLE CONTROL===========

# --------Insert to table control------
# @main.route('/insertperintah/<perintah>/<id_arduino>')
def insert_to_control(perintah,id_arduino,status):
    """
    docstring
    Function update control
    """
    conn=connect_db()
    cur=conn.cursor()
    try:
        cur.execute("UPDATE control SET perintah=%s, status=%s WHERE id_arduino=%s",[perintah,status,id_arduino])
        conn.commit()
        print("Data control berhasil diupdate!")
    except Error as error:
        conn.rollback()
        print("gagal update data {}".format(error))
    finally:
        if (conn):
            cur.close()
            conn.close()
            print("MySql ditutup")
    return "selesai"

# -----cek perintah node x-----
def read_control(id_arduino):
    conn = connect_db()
    cur= conn.cursor()
    cur.execute("SELECT * FROM control WHERE id_arduino=%s",[id_arduino])
    data_perintah= cur.fetchone()
    # isi = data_perintah['perintah']
    return data_perintah

def read_control_id(id_arduino):
    conn = connect_db()
    cur= conn.cursor()
    cur.execute("SELECT id_arduino FROM control WHERE id_arduino=%s",[id_arduino])
    data_perintah= cur.fetchone()
    # isi = data_perintah['perintah']
    return data_perintah

# ------baca semua nodes-------
def read_nodes():
    """
    docstring
    Baca udah berapa node yang connect
    """
    conn = connect_db()    
    cur = conn.cursor()
    cur.execute("SELECT * from control")
    nodes = cur.fetchall()
    return nodes

#  -----baca satu node--------
def read_node(id):
    """
    docstring
    Baca udah berapa node yang connect
    """
    conn = connect_db()    
    cur = conn.cursor()
    cur.execute("SELECT perintah, status FROM control WHERE id_arduino=%s",[id])
    node= cur.fetchone()
    return node
