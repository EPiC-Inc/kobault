from uuid import uuid1

from tinydb import where

from app import character_db

# This program acts as middleware from the frontend to the database

GAMES = ['pathfinder1e']

def fetch(game: str, attribute: str) -> str:
    return ''

def fetch_classes(game: str) -> str:
    return fetch(game, 'class')

# alters='mesmerist/Towering Ego'
# replaces='mesmerist/Painful Stare'
# per_day=3
# uses_left=2
def fetch_feature(game: str, class_: str, feature_name: str) -> str:
    return fetch(game, 'class')

def fetch_character(character_id: str) -> dict:
    character = character_db.search(where('character_id')==character_id)
    if not character: return {}
    else: return character[0]

def update_character(character_id: str, attribute:str, value: str | int) -> None:
    print('updating character')
    print(attribute)
    print(value)
    character_db.update({attribute:value}, where('character_id')==character_id)

def new_character(game: str) -> str | None:
    if not game in GAMES:
        return None
    character_id = str(uuid1())
    character_db.insert({
        "character_id": character_id,
        "name": "Unnamed Character",
    })

    match game:
        case "pathfinder1e":
            character_db.update({
                'game': game,
                'ac': 10,
                'max_hp': 10,
                'skills': [],
            }, where('character_id') == character_id)
    return character_id