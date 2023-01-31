import json

with open('data/pathfinder1e/conditions.json', 'r') as condfile:
    conditions = json.load(condfile)

for cond_name in conditions:
    print(f"\"{cond_name}\": \"{cond_name}\",")

# for cond in conditions:
#     conditions[cond]['color'] = 'black'
# print(conditions)

# with open('data/pathfinder1e/conditions.json', 'w') as condfile:
#     condfile.write(json.dumps(conditions))