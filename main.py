from flask import Flask, render_template, request, make_response, abort, redirect, url_for, jsonify, session, flash
import json
import time
from datetime import datetime
from statistics import mean

from functools import wraps
from MySQLdb import cursors, connect
import mysql.connector
from flask_cors import CORS, cross_origin

main = Flask(__name__)
cors = CORS(main)

main.secret_key="081213342244"

# non-route function

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

# inset to table
# @main.route('/inserttabel/<suhu>/<lembap>/<sm>/<rel>')
def insert_to_table(suhu,lembap,sm,rel):
    conn = connect_db()
    try:
        
        cursor = conn.cursor()
        query = "INSERT INTO sensor (suhu, kelembapan, soil_moist, relay) VALUES (%s, %s, %s, %s)"

        tuple = (suhu, lembap, sm, rel)
        try:
            cursor.execute(query,tuple)
            conn.commit()
        except:
            conn.rollback()
        print("Data berhasil dimasukkan")

    except Error as error:
        print("Gagal memasukkan data {}".format(error))

    finally:
        if (conn):
            cursor.close()
            conn.close()
            print("MySql ditutup")
    # return "selesai"


#baca tabel general
def read_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * from sensor order by id desc")
    data = cur.fetchall()
    sensor = get_data(data)
    top_data = read_top(sensor)
    curr_data = sensor[0]
    return sensor, curr_data, top_data

# Fungsi biar ga mentahan dari db
def get_data(data):
    li = []
    for dat in data:
        di = {}
        waktu = dat['time']
        tanggal = waktu.strftime("%d/%m/%Y")
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
def read_yesterday():
    conn = connect_db()
    cur = conn.cursor()
    #ini tambahan
    try:
        cur.execute("SELECT * FROM sensor WHERE DATE(time) = DATE(NOW() - INTERVAL 3 DAY) order by id desc")
        data = cur.fetchall()
        sensor = get_data(data)
        y_suhu, y_lembap, y_sm = mean_yesterday(sensor)
    except:
        y_suhu = 0
        y_lembap = 0
        y_sm = 0
    #tambah end
    sensor,curr_data,bar = read_table()
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


# Routing
@main.route('/')
@login_required
def index():
    # mengambil data dari methode GET
    get = request.args.get('get')
    if get:
        return render_template('base/master.html',isi=get)
    else :
        return render_template('base/master.html',isi="Ini Index Kosongan")

    return render_template('base/master.html')
    
    # return render_template('laman di dalam folder template', variabeldikirim=isi)
@main.route('/dashboard/<id>')
@login_required
def dashboard(id):
    return render_template('dashboard.html', id=id )

@main.route('/control/<id>')
@login_required
def control(id):
    return render_template('control.html', id=id )

@main.route('/get',methods=["GET"])
def get_data_api():
    sensor, curr_data, bar_data = read_table()
    yesterday = read_yesterday()
    return jsonify({'sensor':sensor,'curr_data':curr_data,'bar_data':bar_data, 'yesterday':yesterday})

@main.route('/input',methods=["POST"])
def input_data():
    suhu = 0.0
    lembap = 0.0
    sm = 0.0
    rel = 0
# perintah arduino
    try:
        if request.method == "POST":
            suhu = float(request.form["suhu"])
            lembap = float(request.form["lembap"])
            sm = float(request.form["sm"])
            rel = int(request.form["relay"])
        insert_to_table(suhu,lembap,sm,rel)
        return "suhu : {}, kelembapan : {}, soil moisture : {}, relay : {}".format(suhu ,lembap, sm, rel)
    except Exception as e:
        return "error {}".format(e)


# get data dari form post
@main.route('/login', methods=['GET', 'POST'])
def login():
    # Sudah login
    if 'email_user' in session:
        isi="Kamu telah login sebagai :"+ session['email_user']
        return redirect(url_for('index', get=isi))   
        # Untuk redirect, value ke 2 bukan yg di dalem html, tapi metode get.
        # Jadi kalo render_html itu isi=xxx karena di html variabel nya isi
        # Tapi kalo redirect itu parameter_get = xxxx karena munculnya bakalan /?parameter_get=xxxx
    # proses login
    if request.method=='POST':
        isi="Kamu telah login sebagai :"+ request.form['email']
        session['email_user'] = request.form['email']
        flash("Logged in!", 'alert-success')
        return redirect(url_for('index', get=isi))   
    # belum login
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    session.pop('email_user', None)
    flash("Logged Out!", 'alert-success')
    return redirect(url_for('login'))



# Cookies
@main.route('/cookies', methods=['POST'])
def kuki():
    if request.method == 'POST' :
        # return request.form['email']
        resp = make_response(redirect('/')) #membuat response object
        # return resp
        resp.set_cookie('email', request.form['email']) #response object mengisi value cookie nya(respObj->cookie)
        resp.set_cookie('theme', request.form['theme'])
        # return "sukses"
         
    return resp #mengembalikan respObj beserta atribut yg menempel (kuki)

@main.route('/cekkuki')
def getKuki():
    test = request.cookies
    if not test :
        test = "kosong"

    return test

#routing dynamic
@main.route('/dinamis/<variabel>')
def dinamis(variabel):
    return 'samlekom dinamis 1 %s' % variabel

@main.route('/dinamis2/<int:variabel>')
def dinamis2(variabel):
    return 'samlekom dinamis 2 %d' % variabel


@main.route('/bacatabel')
def connectDB():
    conn = connect_db()
    read = conn.cursor
    query = "SELECT * from sensor order by id desc"
    read.execute(query)
    data = read.fetchall()
    sensor = get_data(data)
    return jsonify({'sensor':sensor})

if __name__ == "__main__":
    main.run(host='0.0.0.0',port='5000',debug=True, threaded=True)