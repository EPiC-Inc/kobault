"""This program acts as middleware from the frontend to the database api."""

# from dataclasses import asdict
from json import load
from time import sleep
from uuid import uuid1

from app import pathfinder_character_db
from objects import Characters

GAMES = ["pathfinder1e"]

def fetch(game: str, name: str, attribute: str | None = None):
    return ""


def fetch_condition(game: str, condition: str) -> dict:
    with open(f"data/{game}/conditions.json") as conditions_file:
        conditions = load(conditions_file)
    to_return = conditions[condition]
    del conditions
    return to_return


def fetch_skills(game: str, full: bool = False) -> list | dict:
    with open(f"data/{game}/skills.json") as skill_file:
        skills = load(skill_file)
    if full:
        return skills
    else:
        return list(skills.keys())


def fetch_character(character_id: str) -> dict:
    character = character_db.get({"character_id": character_id})[0]
    if not character:
        return {}
    else:
        return character


def update_character(
    character_id: str, attribute: str, value: str | int | list | dict
) -> None:
    print("updating character")
    print(attribute)
    print(value)
    if ":" in attribute:
        attribute, section = attribute.split(":", maxsplit=1)
        new_attribute = fetch_character(character_id)[attribute]
        print("obtaining lock...")
        obtain_database_lock(write=True)
        new_attribute[section] = value  # type: ignore
        character_db.update(
            {attribute: new_attribute}, where("character_id") == character_id
        )
    else:
        print("obtaining lock...")
        character_db.update({attribute: value}, where("character_id") == character_id)


def new_character(game: str, user_id: str, user_name: str) -> str | None:
    if not game in GAMES:
        return None
    character_id = str(uuid1())

    character_db.insert(
        {
            "character_id": character_id,
            "name": "Unnamed Character",
            "game": game,
        }
    )

    match game:
        case "pathfinder1e":
            character_db.insert_object(Characters.Pathfinder(user_id=user_id))
    return character_id
