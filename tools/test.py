import json

with open('data/pathfinder1e/skills.json', 'r') as skills_file:
    skills = json.load(skills_file)

# for skill in "Acrobatics | Appraise | Bluff | Climb | Craft | Diplomacy | Disable Device | Disguise | Escape Artist | Fly | Handle Animal | Heal | Intimidate | Knowledge | Linguistics | Perception | Perform | Profession | Ride | Sense Motive | Sleight of Hand | Spellcraft | Stealth | Survival | Swim | Use Magic Device".split(" | "):
#     skills[skill] = {
#         "ability": "intelligence",
#         "trained": False,
#         "blank": False,
#     }

with open('data/pathfinder1e/skills.json', 'w') as cond_file:
    cond_file.write(json.dumps(skills))
