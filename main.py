from flask import Blueprint, render_template
from jinja2 import TemplateNotFound

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return 'Index'

@main.route('/<game>/character/<character_id>')
def character_sheet(game, character_id):
    #TODO - fetch character from storage
    try:
        return render_template(f"{game}/character_sheet.html")
    except TemplateNotFound:
        return render_template("_core/404.html"), 404
