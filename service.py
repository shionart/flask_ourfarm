from repository import *


#Cek login atau tidak
def login_required(f):
    @wraps(f)
    def login_handler(*args,**kwargs):
        if 'email' in session:
            return f(*args, **kwargs)
        else :
            flash("Please Login First!", "alert-warning")
            return redirect(url_for('login'))
    return login_handler

def cek_auth(email,password):
    """
    cek email & password sama & ada atau tidak
    """
    auth=read_user(email)
    if auth==None:
        return "Akun Tidak ditemukan"
    elif password!=auth['password']:
        return "Password Tidak Sesuai"
    else:
        session['email'] = request.form['email']
        return True
    
def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))