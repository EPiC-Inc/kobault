import json

with open('data/pathfinder1e/skills.json', 'r') as skillsfile:
    skills = json.load(skillsfile)

for skill in "Acrobatics | Appraise | Bluff | Climb | Craft | Diplomacy | Disable Device | Disguise | Escape Artist | Fly | Handle Animal | Heal | Intimidate | Knowledge | Linguistics | Perception | Perform | Profession | Ride | Sense Motive | Sleight of Hand | Spellcraft | Stealth | Survival | Swim | Use Magic Device".split(" | "):
    skills[skill] = {
        "ability": "intelligence",
        "trained": False,
        "blank": False,
    }

with open('data/pathfinder1e/skills.json', 'w') as condfile:
    condfile.write(json.dumps(skills))