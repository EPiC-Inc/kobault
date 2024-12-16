from json import load
from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import HTTPException


fetch = FastAPI()

GAMES = ("pathfinder1e",)
ROOT_PATH = Path(__file__).parent.parent
LOCKS: set[str] = set()


def compute_file_path(file_path: str | Path) -> Path:
    # Honestly I could probably just do 'if ".." in file_path: raise HTTPException'
    return ROOT_PATH / ((ROOT_PATH / Path(file_path)).resolve().relative_to(ROOT_PATH))


@fetch.get("/{game}/condition/{condition}")
def fetch_condition(game: str, condition: str) -> dict:
    with compute_file_path(f"data/{game}/conditions.json").open("r") as conditions_file:
        conditions = load(conditions_file)
    to_return = conditions[condition]
    del conditions
    return to_return


@fetch.get("/{game}/skills")
def fetch_skills(game: str, full: bool = False) -> list | dict:
    with compute_file_path(f"data/{game}/skills.json").open("r") as skill_file:
        skills: dict = load(skill_file)
    if full:
        return skills
    else:
        return list(skills.keys())

@fetch.get("/character/{character_id}")
def fetch_character(character_id: str) -> dict | None:
    if (character_file_path := compute_file_path(f"characters/{character_id}")).exists():
        while character_file_path.as_posix() in LOCKS:
            pass
        with character_file_path.open("r") as character_file:
            return load(character_file)
    raise HTTPException(status_code=404, detail="Character not found!")
