import json

with open('data/pathfinder1e/conditions.json', 'r') as condfile:
    conditions = json.load(condfile)

for cond in conditions:
    conditions[cond]['affects'] = {}
print(conditions)

with open('data/pathfinder1e/conditions.json', 'w') as condfile:
    condfile.write(json.dumps(conditions))