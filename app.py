from os import environ

from flask import Flask, render_template
from flask_login import LoginManager, UserMixin

from dbapi import Database, Table
from objects import Characters, User

db = Database()
user_db = Table("Users")
pathfinder_character_db = Table("Characters_Pathfinder")

class User_(UserMixin):
    def __init__(self, user_id: str) -> None:
        super().__init__()
        self.id = user_id

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        user = user_db.query("user_name", where_column="user_id", where_data=self.id)
        if user:
            return user[0][0]
        return "N/A"

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

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # type: ignore
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        return User_(user_id)

    return app
