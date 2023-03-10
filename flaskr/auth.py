import functools
import json
from bson import ObjectId

import pymongo

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

from flaskr.MongoEncoder import MongoJSONEncoder

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                id = db.CustomerMaster.insert_one({
                    "email": username,
                    "password":generate_password_hash(password),
                }).inserted_id
            except pymongo.errors.DuplicateKeyError:
                error = f"User {username} is already registered."
            except pymongo.errors.WriteError:
                error = f"Failed to register the user."
            else:
                flash(u'User Registered Successfully!','info')
                return redirect(url_for("auth.login"))

        flash(error,'error')

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user_bson = db.CustomerMaster.find_one({"email": username})
        if user_bson is None:
            error = 'Incorrect username.'
        else :
            data_json = MongoJSONEncoder().encode(dict(user_bson))
            user = json.loads(data_json)
            #print(user)

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['_id']
            return redirect(url_for('dashboard'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().CustomerMaster.find_one({"_id": ObjectId(user_id)})

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view