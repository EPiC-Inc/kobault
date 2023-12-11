"""Holds all the required objects."""

from dataclasses import dataclass, field
from uuid import uuid1

def new_uuid() -> str:
    return str(uuid1())

class Updateable(object):
    def update(self, new):
        for key, value in new.items():
            if hasattr(self, key):
                setattr(self, key, value)

@dataclass(slots=True)
class User:
    user_id: str
    user_name: str
    password: bytes
    characters: list = field(default_factory=list)
    campaigns: list = field(default_factory=list)

class Characters:
    @dataclass(slots=True)
    class Pathfinder(Updateable):
        user_id: str
        character_id: str = field(default_factory=new_uuid)
        npc: bool = False
        game: str = "pathfinder1e"
        name: str = "Unnamed Character"
        hp: str | int = 10
        max_hp: str | int = 10
        nonlethal_damage: str | int = 0
        class_: str = "class / subclass (0)"
        background: str = "N/A"
        race: str = "N/A"
        alignment: str = "True Neutral"
        exp: str | int = "N/A"
        strength: str | int = 10
        dexterity: str | int = 10
        constitution: str | int = 10
        intelligence: str | int = 10
        wisdom: str | int = 10
        charisma: str | int = 10
        languages: str | list = "Common"
        personality: str = "Mysterious"
        traits: dict = field(default_factory=dict)
        skills: dict = field(default_factory=dict)
        skill_bonuses: dict = field(default_factory=dict)
        class_skills: dict = field(default_factory=dict)
        items: dict = field(default_factory=dict)
        armor: dict = field(default_factory=dict)
        weapons: dict = field(default_factory=dict)
        spells: dict = field(default_factory=dict)
        features: dict = field(default_factory=dict)
        trinkets: dict = field(default_factory=dict)
        permanent_stat_modifiers: list = field(default_factory=list)
        base_attack_bonus: str = "+1"
        speed: str | int = 30
        conditions: list = field(default_factory=list)
