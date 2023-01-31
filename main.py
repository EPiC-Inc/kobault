from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound

import fetch

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
@login_required
def characters():
    #TODO - Get a list of all the logged-in user's characters
    abort(501)

@main.route('/characters/<game>/<character_id>')
@login_required
def character_sheet(game, character_id):
    user_id = current_user.get_id() # type: ignore
    user_name = current_user.get_name() # type: ignore
    #TODO - make sure user is authorized for that character
    try:
        if character_id == "new":
            character_id = fetch.new_character(game, user_id, user_name)
            return redirect(url_for('main.character_sheet', game=game, character_id=character_id))

        character = fetch.fetch_character(character_id)
        if not character:
            abort(404)

        return render_template(f"{game}/character_sheet.html", 
            editable=False if request.args.get('readonly') else True,
            **character)
    except TemplateNotFound:
        abort(404)

#ANCHOR - Edit character
@main.route('/characters/<character_id>', methods=['POST'])
def set_character(character_id):
    fetch.update_character(character_id, request.form.get('attribute', ''),
        request.form.get('value', ''))
    #TODO - make sure user is authorized for that character
    return {'success':True}

@main.route('/fetch/<game>/<to_fetch>')
def fetch_from_rules(game, to_fetch):
    match to_fetch:
        case value if value.startswith("condition"):
            return fetch.fetch_condition(game, value[value.index(':')+1:])
        case _:
            return ''

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