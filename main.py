

from function import *




# Routing
@main.route('/')
@login_required
def index():
    # mengambil data dari methode GET
    # get = request.args.get('get')
    # if get:
    #     return render_template('home.html',isi=get)
    # else :
    #     return render_template('home',isi="Ini Index Kosongan")
    return render_template('home.html', ip=ip_address)
    
    # return render_template('laman di dalam folder template', variabeldikirim=isi)


@main.route('/dashboard/<id>')
@login_required
def dashboard(id):
    info = read_control(id)
    return render_template('dashboard.html', info=info )

@main.route('/control/<id>')
@login_required
def control(id):
    perintah = read_control(id)
    # return perintah
    return render_template('control.html', data=perintah )

@main.route('/control')
@login_required
def list_control():
    response = render_template('list_nodes.html')
    return response


# Api ambil data dari db
@main.route('/get/<id>',methods=["GET"])
def get_data_api(id):
    sensor, curr_data, bar_data = read_sensor(id)
    yesterday = read_yesterday(id)
    # Outputnya berupa bundle sensor, data terbaru & kemaren, bardata(Top data)
    return jsonify({'sensor':sensor,'curr_data':curr_data,'bar_data':bar_data, 'yesterday':yesterday})

@main.route('/get_control',methods=["GET"])
def get_data_control():
    nodes = read_nodes()
    # Outputnya berupa bundle sensor, data terbaru & kemaren, bardata(Top data)
    return jsonify({'nodes':nodes})

@main.route('/get_control/<id>',methods=["GET","POST"])
def get_data_node(id):
    node = read_node(id)
    # Outputnya berupa bundle sensor, data terbaru & kemaren, bardata(Top data)
    return node

# Api input data dari arduino
@main.route('/input',methods=["POST"])
def input_data():
    suhu = 0.0
    lembap = 0.0
    sm = 0.0
    rel = 0
    id_arduino =0
    nama="default"
# perintah arduino
    try:
        if request.method == "POST":
            suhu = float(request.form["suhu"])
            lembap = float(request.form["lembap"])
            sm = float(request.form["sm"])
            rel = int(request.form["relay"])
            id_arduino = str(request.form["id_arduino"])
            nama = str(request.form["nama"])
            insert_to_table(suhu,lembap,sm,rel,id_arduino,nama)
            return "suhu : {}, kelembapan : {}, soil moisture : {}, relay : {}, id : {}".format(suhu ,lembap, sm, rel, id_arduino)
    except Exception as e:
        return "error {}".format(e)

@main.route('/input_control',methods=["POST"])
def input_control():
    perintah = 0
    id_arduino = 0
    status = 0
# perintah arduino
    try:
        if request.method == "POST":
            perintah = int(request.form["perintah"])
            id_arduino = str(request.form["id_arduino"])
        insert_to_control(perintah,id_arduino,status)
        return "perintah : {}, id_arduino : {}, status:{}".format(perintah, id_arduino,status)
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
    sensor = get_sensor(data)
    return jsonify({'sensor':sensor})

if __name__ == "__main__":
    main.run(host='0.0.0.0',port='5000',debug=True, threaded=True)