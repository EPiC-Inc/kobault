from urllib.parse import urljoin, urlparse

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import UserMixin, current_user, login_user
from tinydb import where
from werkzeug.security import check_password_hash, generate_password_hash

# This is to prevent data races or other multithreading stupidity
from app import user_db, User

# This module is for authentication

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET", "POST"])
def login():
    next = request.args.get('next', url_for('main.index'))

    if request.method == "GET":
        return render_template('_core/login.html', next=next)
    # Get form data
    user_id = request.form.get('user_id')
    password = request.form.get('password')

    if not (user_id and password):
        flash("Please make sure all fields are filled out", category='warning')
        return redirect(url_for('auth.login'))

    user_exists = user_db.get(where('user_id') == user_id)
    print(user_exists)
    if not user_exists:
        flash("User ID not found", category='warning')
        return redirect(url_for('auth.login'))
    
    #ANCHOR - actual login
    if check_password_hash(user_exists['password'], password):
        to_login = User(user_exists["user_id"])
        print(to_login)
        print(current_user)
        login_user(to_login, remember=True)

        return redirect(next)
    else:
        flash("Invalid password", category='warning')
        return redirect(url_for('auth.login'))

@auth.route('/signup', methods=["GET", "POST"])
def signup():
    next = request.args.get('next', url_for('main.index'))

    if request.method == "GET":
        return render_template('_core/signup.html')
    # Get form data
    user_id = request.form.get('user_id')
    user_name = request.form.get('user_name')
    password = request.form.get('password')

    #TODO - verify user id and password
    if not (user_id and user_name and password):
        flash("Please make sure all fields are filled out", category='warning')
        return redirect(url_for('auth.signup'))

    user_exists = user_db.search(where('user_id') == user_id)
    if user_exists:
        flash("User ID already exists", category='warning')
        # Make sure duplicate users can't exist lol
        return redirect(url_for('auth.signup'))

    user_db.insert({
        "user_id": user_id,
        "user_name": user_name,
        "password": generate_password_hash(password, method='sha256'),
        "characters": [],
        "campaigns": [],
    })

    return redirect(next)

@auth.route('/logout')
def logout():
    return 'Logout'
