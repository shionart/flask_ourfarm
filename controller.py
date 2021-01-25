from service import *
from model.Control import *

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
    raspi = read_user(session['email'])
    id_user= raspi['id_user']
    return render_template('home.html', ip=ip_address, id_user=id_user)
    
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

# get data dari form post
@main.route('/login', methods=['GET', 'POST'])
def login():
    # Sudah login
    if 'email' in session:
        return redirect(url_for('index'))   
        # Untuk redirect, value ke 2 bukan yg di dalem html, tapi metode get.
        # Jadi kalo render_html itu isi=xxx karena di html variabel nya isi
        # Tapi kalo redirect itu parameter_get = xxxx karena munculnya bakalan /?parameter_get=xxxx
    # proses login
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        message = cek_auth(email,password)
        if message==True:
            flash("Logged in as {}!".format(email), 'alert-success')
            return redirect(url_for('index'))
        else:
            flash(message,"alert-warning")
            return redirect(url_for('login'))
    # belum login
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    session.pop('email', None)
    flash("Logged Out!", 'alert-success')
    return redirect(url_for('login'))

@main.route('/register', methods=['GET'])
def register():
    return render_template('register.html')
    

# -------------------------------------------------------------
# ---------------------API POST--------------------------------
# -------------------------------------------------------------

#API POST data ke RASPI
@main.route('/post_raspi',methods=["POST"])
def post_raspi():
    if "password" in request.form:
        try:
            email=str(request.form['email'])
            password=str(request.form['password'])
            cu_user(email,password,None)        
            flash("Berhasil registrasi, silahkan login!", "alert-success")
            return redirect(url_for('login'))
        except Exception as error:
            flash("Error:{}".format(error), "alert-warning")
            return redirect(url_for('register'))
    elif 'id_user' in request.form:
        try:
            email=str(request.form['email'])
            id_user=str(request.form['id_user'])
            cu_user(email,None,id_user)
            return "id_user updated : {}".format(id_user)
        except Exception as e:
            return "error : {}".format(e)
    
# Api input data dari arduino
@main.route('/input',methods=["POST"])
def input_data():
    suhu = 0.0
    lembap = 0.0
    sm = 0.0
    rel = 0
    id_arduino =0
# perintah arduino
    try:
        if request.method == "POST":
            suhu = float(request.form["suhu"])
            lembap = float(request.form["lembap"])
            sm = float(request.form["sm"])
            rel = int(request.form["relay"])
            id_arduino = str(request.form["id_arduino"])
            insert_to_sensor(suhu,lembap,sm,rel,id_arduino)
            return "suhu : {}, kelembapan : {}, soil moisture : {}, relay : {}, id : {}".format(suhu ,lembap, sm, rel, id_arduino)
    except Exception as e:
        return "error {}".format(e)


# -------------------------------------------------------------
# ---------------------API GET---------------------------------
# -------------------------------------------------------------

# Api ambil data dari db
@main.route('/get/<id>',methods=["GET"])
def get_data_api(id):
    sensor, curr_data, bar_data = read_sensor(id)
    yesterday = read_yesterday(id)
    # Outputnya berupa bundle sensor, data terbaru & kemaren, bardata(Top data)
    return jsonify({'sensor':sensor,'curr_data':curr_data,'bar_data':bar_data, 'yesterday':yesterday})

# Api ambil list arduino
@main.route('/get_control',methods=["GET"])
def get_data_control():
    nodes = read_controls()
    # Outputnya berupa bundle sensor, data terbaru & kemaren, bardata(Top data)
    return jsonify({'nodes':nodes})

# Api ambil data control node N
@main.route('/api_control/<id>',methods=["GET","POST"])
def api_data_node(id):
    if(request.method=="GET"):
        node = read_control(id)
        # Outputnya berupa bundle sensor, data terbaru & kemaren, bardata(Top data)
        return node
    elif (request.method=="POST"):
        try:
            perintah = str(request.form["perintah"])
            status = str(request.form["status"])
            nama = str(request.form["nama"])
            insert_to_control(perintah,id,status,nama)
            return "perintah: {}, status: {}, id: {}, nama:{}".format(perintah, status, id,nama)
        except Exception as e:
            return "error route {}".format(e)

@main.route('/object',methods=["GET"])
def testoo():
    """
    docstring
    """
    c = Control()
    listControl = c.read_controls()
    return jsonify(listControl)

