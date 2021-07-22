from flask import render_template, request, session, redirect, url_for, flash
from controller.Controller import login_required
from config.config import ip_address
from model.User import User



class UserController(object):
    """
    Controller untuk model/tale User
    """
    def __init__(self, **kwargs):
        """
        User Controller
        --------
        Parameters(sunnah) :
            - email
            - password
            - id_user
        """
        if len(kwargs)>0:
            self.user = User(email=kwargs.pop("email", None),
            password=kwargs.pop("password", None), 
            id_user=kwargs.pop("id_user", None))
        else:
            self.user = User()
    
    def cek_auth(self):
        """
        cek email & password sama & ada atau tidak
        """
        usr = self.user
        auth=usr.read_user()
        if auth==None:
            return "Akun Tidak ditemukan"
        elif usr.password!=auth['password']:
            return "Password Tidak Sesuai"
        else:
            session['email'] = request.form['email']
            session['iduser'] = str(auth['id_user'])
            return True

    
    def index(self):
        # mengambil data dari methode GET
        # get = request.args.get('get')
        # if get:
        #     return render_template('home.html',isi=get)
        # else :
        #     return render_template('home',isi="Ini Index Kosongan")
        usr= self.user
        usr.email = session['email']
        raspi = usr.read_user()
        id_user = raspi['id_user']
        return render_template('home.html', ip=ip_address, id_user=id_user)

        # return render_template('laman di dalam folder template', variabeldikirim=isi)

    def login(self):
        # Sudah login
        if 'email' in session:
            return redirect(url_for('index'))
            # Untuk redirect, value ke 2 bukan yg di dalem html, tapi metode get.
            # Jadi kalo render_html itu isi=xxx karena di html variabel nya isi
            # Tapi kalo redirect itu parameter_get = xxxx karena munculnya bakalan /?parameter_get=xxxx
        # proses login
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            usr = self.user
            usr.email = email
            usr.password = password
            message = self.cek_auth()
            if message == True:
                flash("Logged in as {}!".format(email), 'alert-success')
                return redirect(url_for('index'))
            else:
                flash(message, "alert-warning")
                return redirect(url_for('login'))
        # belum login
        return render_template('login.html')

    def logout(self):
        session.pop('email', None)
        session.pop('iduser', None)
        flash("Logged Out!", 'alert-success')
        return redirect(url_for('login'))

    def register(self):
        return render_template('register.html')

    
    def post_raspi(self):
        if "password" in request.form:
            try:
                email = str(request.form['email'])
                password = str(request.form['password'])
                self.user=User(email=email, password=password)
                self.user.cu_user()
                flash("Berhasil registrasi, silahkan login!", "alert-success")
                return redirect(url_for('login'))
            except Exception as error:
                flash("Error:{}".format(error), "alert-warning")
                return redirect(url_for('register'))
        if 'id_user' in request.form:
            try:
                email = str(request.form['email'])
                id_user = str(request.form['id_user'])
                self.user=User(email=email, id_user=id_user)
                self.user.cu_user()
                return "id_user updated : {}".format(id_user)
            except Exception as e:
                return "error : {}".format(e)


    