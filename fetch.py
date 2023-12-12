"""This program acts as middleware from the frontend to the database api."""

from dataclasses import asdict
from json import load, dumps
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


def fetch_character(character_id: str) -> dict | None:
    character = None
    character_game = None
    for game in GAMES:
        if game == "pathfinder1e":
            character_game = game
            character = pathfinder_character_db.query(
                "*", where_column="character_id", where_data=[character_id]
            )
            if character:
                character = Characters.Pathfinder(*character[0])
                break
    if not character:
        return None
    else:
        character = asdict(character) # type: ignore
        character["game"] = character_game
        return character  # type: ignore


def update_character(
    character_id: str, attribute: str, value: str | int | list | dict
) -> None:
    print("updating character")
    print(attribute)
    print(value)
    character_db = None
    character = fetch_character(character_id)
    if not character:
        return
    game = character.get("game")
    if game == "pathfinder1e":
        character_db = pathfinder_character_db
    if ":" in attribute:
        attribute, section = attribute.split(":", maxsplit=1)
        new_attribute = character[attribute]
        new_attribute[section] = value  # type: ignore
        new_attribute = dumps(new_attribute)

        character_db.update_property(
            attribute, new_attribute, "character_id", character_id
        )
    else:
        character_db.update_property(attribute, value, "character_id", character_id)


def new_character(game: str, user_id: str, user_name: str) -> str | None:
    if not game in GAMES:
        return None

    match game:
        case "pathfinder1e":
            new_character = Characters.Pathfinder(user_id=user_id)
            pathfinder_character_db.insert_object(new_character)
        case _:
            return None
    return new_character.character_id
