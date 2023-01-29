from bcrypt import gensalt, hashpw
from flask import Blueprint, flash, redirect, render_template, request, url_for
from tinydb import where

# This is to prevent data races or other multithreading stupidity
from app import user_db

# This module is for authentication

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('_core/login.html')
    # Get form data
    user_id = request.form.get('user_id')
    password = request.form.get('password')

    #TODO - verify user id and password
    if not (user_id and password):
        flash("Please make sure all fields are filled out", category='warning')
        return redirect(url_for('auth.login'))
    
    return redirect(url_for('main.index'))

@auth.route('/signup', methods=["GET", "POST"])
def signup():
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
        flash("User already exists", category='warning')
        # Make sure duplicate users can't exist lol
        return redirect(url_for('auth.signup'))

    user_db.insert({
        "user_id": user_id,
        "user_name": user_name,
        "password": hashpw(password.encode(), gensalt()).decode()
    })

    return redirect(url_for('main.index'))

@auth.route('/logout')
def logout():
    return 'Logout'
