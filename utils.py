from functools import wraps
from flask import session, flash, url_for, redirect


def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))

    return inner