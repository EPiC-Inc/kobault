"""This module handles authentication."""

from hashlib import scrypt
from urllib.parse import urljoin, urlparse

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user

# This is to prevent data races or other multithreading stupidity
from app import User_, user_db
from objects import User


def password_hash(password: str | bytes) -> bytes:
    """Takes a password and runs it through scrypt."""
    SALT = b"U\xa7S\xaa|\xec\xe1Ex\xfc\x7f4"
    if isinstance(password, str):
        password = password.encode()
    return scrypt(password, salt=SALT, n=2**11, r=8, p=1)


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    next = request.args.get("next", url_for("main.index"))

    if request.method == "GET":
        return render_template("_core/login.html", next=next)
    # Get form data
    user_id = request.form.get("user_id")
    password = request.form.get("password")

    if not (user_id and password):
        flash("Please make sure all fields are filled out", category="warning")
        return redirect(url_for("auth.login"))

    user_exists = stored_password = None
    response = user_db.query(
        "user_id, password", where_column="user_id", where_data=[user_id]
    )
    if response:
        user_exists, stored_password = response[0]

    print(user_exists)
    if not user_exists:
        flash("User ID not found", category="warning")
        return redirect(url_for("auth.login"))

    # ANCHOR - actual login
    if password_hash(password) == stored_password:
        to_login = User_(user_exists)
        print(to_login)
        print(current_user)
        login_user(to_login, remember=True)

        return redirect(next)
    else:
        flash("Invalid password", category="warning")
        return redirect(url_for("auth.login"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    next = request.args.get("next", url_for("main.index"))

    if request.method == "GET":
        return render_template("_core/signup.html")
    # Get form data
    user_id = request.form.get("user_id")
    user_name = request.form.get("user_name")
    password = request.form.get("password")

    # TODO - verify user id and password
    if not (user_id and user_name and password):
        flash("Please make sure all fields are filled out", category="warning")
        return redirect(url_for("auth.signup"))

    user_exists = user_db.query("user_id", where_column="user_id", where_data=[user_id])
    if user_exists:
        flash("User ID already exists", category="warning")
        # Make sure duplicate users can't exist lol
        return redirect(url_for("auth.signup"))

    new_user = User(
        user_id=user_id, user_name=user_name, password=password_hash(password)
    )
    user_db.insert(
        [
            new_user.user_id,
            new_user.user_name,
            new_user.password,
        ]
    )

    login_user(User_(user_id), remember=True)
    if next:
        return redirect(next)
    else:
        return redirect(url_for("main.index"))


@auth.route("/logout")
def logout():
    return "Logout"
