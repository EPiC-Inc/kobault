from os import environ

from flask import Flask, render_template
from flask_login import LoginManager
from tinydb import TinyDB

db = TinyDB("./main_database.json")
user_db = db.table('users')
character_db = db.table('characters')

def page_not_found(e):
    return render_template("_core/404.html"), 404

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = environ.get("KOBAULT_SECRET_KEY")

    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    app.register_error_handler(404, page_not_found)

    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login' # type: ignore
    # login_manager.init_app(app)
    #TODO - add a user loader

    return app
