from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound
from tinydb import where

import fetch
from app import character_db

# This module is for the main functions of the site - characters, campaigns, spells, etc.

main = Blueprint('main', __name__)

@main.route('/')
def index():
    characters = []
    if current_user.is_authenticated: # type: ignore
        characters = character_db.search(where('owner') == current_user.get_id()) # type: ignore
    return render_template("_core/index.html",
        characters = characters
    )

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
            fetch=fetch,
            **character)
    except TemplateNotFound:
        abort(404)

#ANCHOR - Edit character
@main.route('/characters/<character_id>', methods=['POST'])
def set_character(character_id):
    value = request.form.get('value', '') or request.form.getlist('value[]')
    fetch.update_character(character_id, request.form.get('attribute', ''),
        value)
    #TODO - make sure user is authorized for that character
    return {'success':True}

@main.route('/fetch/<game>/<to_fetch>')
def fetch_from_rules(game, to_fetch):
    match to_fetch:
        case value if value.startswith("condition"):
            return fetch.fetch_condition(game, value[value.index(':')+1:])
        case "skills":
            return fetch.fetch_skills(game)
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