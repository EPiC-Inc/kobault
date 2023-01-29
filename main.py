from flask import Blueprint, abort, redirect, render_template, request, url_for
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
def characters():
    #TODO - Get a list of all the logged-in user's characters
    abort(501)

@main.route('/characters/<game>/<character_id>')
def character_sheet(game, character_id):
    #TODO - make sure user is authorized for that character
    #TODO - fetch character from storage
    try:
        if character_id == "new":
            character_id = fetch.new_character(game)
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