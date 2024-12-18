from dataclasses import asdict
from json import dumps, load
from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from .objects import Characters


fetch = FastAPI()

LOCKS: set[str] = set()
ROOT_PATH = Path(__file__).parent.parent

for path in (ROOT_PATH / "characters", ROOT_PATH / "campaigns"):
    if not path.exists():
        path.mkdir()
    elif not path.is_dir():
        raise FileExistsError(f"{path.name} folder is not a folder??????")

class Games:
    Pathfinder1E = "pathfinder1e"


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

@fetch.get("/characters/{character_id}")
def fetch_character(character_id: str) -> dict | None:
    if (character_file_path := compute_file_path(f"characters/{character_id}")).exists():
        while character_file_path.as_posix() in LOCKS:
            pass
        with character_file_path.open("r") as character_file:
            return load(character_file)
    raise HTTPException(status_code=404, detail="Character not found!")

def new_character(user_id: str, game: str, npc: bool = False) -> str:
    match game:
        case Games.Pathfinder1E:
            character = Characters.Pathfinder(user_id=user_id)
        case _:
            raise HTTPException(status_code=404, detail="Game does not exist!")

    character_id = character.character_id
    if (character_file := compute_file_path(f"characters/{character_id}")).exists():
        raise FileExistsError("UUID clash????")
    LOCKS.add(character_file.as_posix())
    character_file.write_text(dumps(asdict(character)))
    LOCKS.remove(character_file.as_posix())

    return character_id
