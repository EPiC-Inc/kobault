from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

# This module is for the main functions of the site - characters, campaigns, spells, etc.

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return 'Index'

@main.route('/characters')
def characters():
    #TODO - Get a list of all the logged-in user's characters
    abort(501)

@main.route('/characters/<game>/<character_id>')
def character_sheet(game, character_id):
    #TODO - fetch character from storage
    try:
        return render_template(f"{game}/character_sheet.html", 
            game=game, max_hp=32, character_name="test_character")
    except TemplateNotFound:
        abort(404)

#TODO - add a place to print the character and have it in a pathfinder pdf

@main.route('/campaigns')
def campaign_hub():
    abort(501)

@main.route('/campaign/<campaign_id>')
def campaign(campaign_id):
    abort(501)

#TODO - much much later, maybe make a seperate blueprint for this
# @main.route("/compendium")
# def compendium_hub():
#     abort(501)

# @main.route("/compendium/<category>")
# def compendium_category():
#     abort(501)