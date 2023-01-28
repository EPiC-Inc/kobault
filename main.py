from flask import Blueprint, abort, render_template, request
from jinja2 import TemplateNotFound

# This module is for the main functions of the site - characters, campaigns, spells, etc.

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return 'Index'

@main.route('/home')
def home():
    #TODO - make a homepage with campaigns and characters
    return 'home'

@main.route('/characters')
def characters():
    #TODO - Get a list of all the logged-in user's characters
    abort(501)

@main.route('/characters/<game>/<character_id>')
def character_sheet(game, character_id):
    #TODO - make sure user is authorized for that character
    #TODO - fetch character from storage
    try:
        return render_template(f"{game}/character_sheet.html", 
            editable=False if request.args.get('readonly') else True,
            game=game, character_id=character_id,
            hp = 10,
            max_hp=32, character_name="test_character")
    except TemplateNotFound:
        abort(404)

#ANCHOR - Edit character
@main.route('/characters/<character_id>', methods=['POST'])
def set_character(character_id):
    #TODO - make sure user is authorized for that character
    return "test"

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