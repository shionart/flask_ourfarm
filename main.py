from flask import Flask, render_template, request, make_response, abort, redirect, url_for, jsonify, session, flash
import json
main = Flask(__name__)

main.secret_key="081213342244"
#routine statis
@main.route('/')
def hello_world():
    # mengambil data dari methode GET
    get = request.args.get('get')
    if get:
        return render_template('index.html',isi=get)

    return render_template('index.html')
    
    # return render_template('laman di dalam folder template', variabeldikirim=isi)

@main.route('/parsing/<isi>')
def parsing(isi):
    return render_template('index.html',isi=isi)

# get data dari form post
@main.route('/login', methods=['GET', 'POST'])
def login():
    # Sudah login
    if 'email_user' in session:
        isi="Kamu telah login sebagai :"+ session['email_user']
        return redirect(url_for('hello_world', get=isi))   
        # Untuk redirect, value ke 2 bukan yg di dalem html, tapi metode get.
        # Jadi kalo render_html itu isi=xxx karena di html variabel nya isi
        # Tapi kalo redirect itu parameter_get = xxxx karena munculnya bakalan /?parameter_get=xxxx
    # proses login
    if request.method=='POST':
        isi="Kamu telah login sebagai :"+ request.form['email']
        session['email_user'] = request.form['email']
        flash("Logged in!", 'alert-success')
        return redirect(url_for('hello_world', isi=isi))   
    # belum login
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('email_user', None)
    flash("Logged Out!", 'alert-success')
    return redirect(url_for('hello_world', get="Telah logout"))

@main.route('/halo')
def halo():
    return 'samlekom'

#routing dynamic
@main.route('/dinamis/<variabel>')
def dinamis(variabel):
    return 'samlekom dinamis 1 %s' % variabel

@main.route('/dinamis2/<int:variabel>')
def dinamis2(variabel):
    return 'samlekom dinamis 2 %d' % variabel


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

if __name__ == "__main__":
    main.run(host='0.0.0.0',port='5000',debug=True, threaded=True)