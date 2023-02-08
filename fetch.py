import json
from uuid import uuid1

from tinydb import TinyDB, where

from app import character_db

# This program acts as middleware from the frontend to the database

GAMES = ['pathfinder1e']

def fetch(game: str, name: str, attribute: str | None = None):
    return ''

def fetch_condition(game: str, condition: str) -> dict:
    with open(f'data/{game}/conditions.json') as conditions_file:
        conditions = json.load(conditions_file)
    to_return = conditions[condition]
    del conditions
    return to_return

def fetch_skills(game: str) -> list:
    with open(f"data/{game}/skills.json") as skillfile:
        skills = json.load(skillfile)
    return list(skills.keys())

def fetch_classes(game: str) -> str:
    return fetch(game, 'class')

# alters='mesmerist/Towering Ego'
# replaces='mesmerist/Painful Stare'
# per_day=3
# uses_left=2
def fetch_feature(game: str, class_: str, feature_name: str) -> str:
    return fetch(game, 'class')

def fetch_character(character_id: str) -> dict:
    character = character_db.get(where('character_id')==character_id)
    if not character: return {}
    else: return character

def update_character(character_id: str, attribute:str, value: str | int | list | dict) -> None:
    print('updating character')
    print(attribute)
    print(value)
    if ":" in attribute:
        attribute, section = attribute.split(":", maxsplit=1)
        new_attribute = fetch_character(character_id)[attribute]
        new_attribute[section] = value # type: ignore
        character_db.update({attribute:new_attribute}, where('character_id')==character_id)
    else:
        character_db.update({attribute:value}, where('character_id')==character_id)

def new_character(game: str, user_id: str, user_name: str) -> str | None:
    if not game in GAMES:
        return None
    character_id = str(uuid1())
    character_db.insert({
        "character_id": character_id,
        "name": "Unnamed Character",
        'game': game,
    })

    match game:
        case "pathfinder1e":
            character_db.update({
                'hp': 10, 'max_hp': 10,
                'classes': {}, 'background': 'NA', 'user_id': user_id,
                'race': 'NA', 'alignment': 'NA', 'exp': 'NA',
                'age': 'NA', 'body': 'NA', 'appearance': 'NA',
                'strength': 10, 'dexterity': 10, 'constitution': 10,
                'intelligence': 10, 'wisdom': 10, 'charisma': 10,
                'languages': "Common", 'personality': 'Mysterious',
                'skills': {}, 'items': [], 'traits': [],
                'permanent_stat_modifiers': {},
                'conditions': [],
                'armor': None,
                'owner': user_id,
                'user_name': user_name,
            }, where('character_id') == character_id)
    return character_id