from functools import wraps
from flask import session, redirect,url_for

def login_required(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id:
            return fun(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper