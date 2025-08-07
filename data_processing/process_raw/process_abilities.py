import json
import collections

with open('../../data/raw/abilities.json', 'r') as f:
    abilities = json.load(f, object_pairs_hook=collections.OrderedDict)

with open('../../data/raw/abilities_text.json', 'r') as f:
    abilities_text = json.load(f, object_pairs_hook=collections.OrderedDict)

processed_abilities = {}

for num, (key, data) in enumerate(abilities.items()):
    # abilities with negative numbers are unofficial/not in the real games
    if data['num'] < 0:
        pass

    desc = abilities_text[key]
    ability = {
        'num': data['num'],
        'name': data['name'],
        'desc': desc['desc'] if 'desc' in desc else desc['shortDesc'],
        'shortDesc': desc['shortDesc'],
        'rating': data['rating'],
    }
    processed_abilities[key] = ability


with open('../../data/processed/abilities.json', 'w') as f:
    json.dump(processed_abilities, f, indent=4, sort_keys=True)



