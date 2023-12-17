"""Holds all the required objects."""

from dataclasses import dataclass, field
from uuid import uuid4
from json import loads

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
        user_name: str = "You"
        character_id: str = field(default_factory=lambda: str(uuid4()))
        game: str = "pathfinder1e"
        npc: bool = False
        name: str = "Unnamed Character"
        class_: str = "class / subclass (0)"
        background: str = "N/A"
        age: str  = "N/A"
        race: str = "N/A"
        height: str = "N/A"
        weight: str = "N/A"
        eyes: str = "N/A"
        skin: str = "N/A"
        hair: str = "N/A"
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
        platinum: str | int = 0
        gold: str | int = 0
        silver: str | int = 0
        copper: str | int = 0
        armor: dict = field(default_factory=dict)
        weapons: dict = field(default_factory=dict)
        spells: dict = field(default_factory=dict)
        features: dict = field(default_factory=dict)
        trinkets: dict = field(default_factory=dict)
        permanent_stat_modifiers: list = field(default_factory=list)
        base_attack_bonus: str = "+1"
        fortitude_save: str = "+0"
        reflex_save: str = "+0"
        will_save: str = "+0"
        armor_class: str | int = 10
        armor_class_touch: str | int = 10
        armor_class_flat: str | int = 10
        initiative: str | int = "+0"
        speed: str | int = 30
        combat_maneuver_bonus: str | int = "+0"
        combat_maneuver_defense: str | int = 10
        conditions: list = field(default_factory=list)
        hp: str | int = 10
        max_hp: str | int = 10
        temp_hp: str | int = 0
        nonlethal_damage: str | int = 0

        def __post_init__(self):
            json_attrs = ("traits", "skills", "skill_bonuses", "class_skills", "items", "armor", "weapons", "spells", "features", "trinkets", "permanent_stat_modifiers", "conditions")
            for attr in json_attrs:
                data = getattr(self, attr)
                if isinstance(data, str):
                    setattr(self, attr, loads(data))
