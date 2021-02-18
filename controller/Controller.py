from functools import wraps
from flask import session, flash, redirect, url_for

def login_required(f):
    @wraps(f)
    def login_handler(*args,**kwargs):
        if 'email' in session:
            return f(*args, **kwargs)
        else :
            flash("Please Login First!", "alert-warning")
            return redirect(url_for('login'))
    return login_handler

