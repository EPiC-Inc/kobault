import json
from time import sleep
from uuid import uuid1

from tinydb import TinyDB, where

from app import character_db

# This program acts as middleware from the frontend to the database

GAMES = ['pathfinder1e']

# Just a simple mutex - probably very vulnerable to deadlocks if anything crashes before it's released
DB_LOCK = False
def obtain_database_lock(write=False):
    global DB_LOCK
    print("Lock", DB_LOCK, "Writing", write)
    c = 0
    while DB_LOCK:
        c += 1
        print('character db locked')
        if c > 4 and not write:
            print("Breaking out :3 (VERY BAD IDEA METHINKS)")
            break
        if c > 100:
            raise LookupError()
        sleep(0.2)
    if write: DB_LOCK = True
def release_database_lock():
    print("unlocking...")
    global DB_LOCK
    DB_LOCK = False

def fetch(game: str, name: str, attribute: str | None = None):
    return ''

def fetch_condition(game: str, condition: str) -> dict:
    with open(f'data/{game}/conditions.json') as conditions_file:
        conditions = json.load(conditions_file)
    to_return = conditions[condition]
    del conditions
    return to_return

def fetch_skills(game: str, full: bool = False) -> list | dict:
    with open(f"data/{game}/skills.json") as skillfile:
        skills = json.load(skillfile)
    if full:
        return skills
    else:
        return list(skills.keys())

# alters='mesmerist/Towering Ego'
# replaces='mesmerist/Painful Stare'
# per_day=3
# uses_left=2
def fetch_feature(game: str, class_: str, feature_name: str) -> str:
    return fetch(game, 'class')

def fetch_character(character_id: str) -> dict:
    obtain_database_lock()
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
        print("obtaining lock...")
        obtain_database_lock(write=True)
        new_attribute[section] = value # type: ignore
        character_db.update({attribute:new_attribute}, where('character_id')==character_id)
    else:
        print("obtaining lock...")
        obtain_database_lock(write=True)
        character_db.update({attribute:value}, where('character_id')==character_id)
    release_database_lock()

def new_character(game: str, user_id: str, user_name: str) -> str | None:
    if not game in GAMES:
        return None
    character_id = str(uuid1())

    obtain_database_lock(write=True)
    character_db.insert({
        "character_id": character_id,
        "name": "Unnamed Character",
        'game': game,
    })

    match game:
        case "pathfinder1e":
            character_db.update({
                'hp': '10', 'max_hp': '10', "nonlethal_damage": '0',
                'class_': 'class / subclass (0)', 'background': 'NA', 'user_id': user_id,
                'race': 'NA', 'alignment': 'NA', 'exp': 'NA',
                'strength': '10', 'dexterity': '10', 'constitution': '10',
                'intelligence': '10', 'wisdom': '10', 'charisma': '10',
                'languages': "Common", 'personality': 'Mysterious',
                'skills': {}, 'skill_bonuses': {}, 'items': {}, 'armor': {},
                'traits': {}, 'weapons': {},
                'spells': {}, 'features': {}, 'trinkets': {},
                'permanent_stat_modifiers': [],
                'base_attack_bonus': '+1', 'speed': '30',
                'conditions': [],
                'armor': None,
                'owner': user_id, 'user_name': user_name, 'npc': False
            }, where('character_id') == character_id)
    release_database_lock()
    return character_id