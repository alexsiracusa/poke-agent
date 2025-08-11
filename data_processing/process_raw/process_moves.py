import json
import collections

with open('../../data/raw/moves.json', 'r') as f:
    moves = json.load(f, object_pairs_hook=collections.OrderedDict)

with open('../../data/raw/moves_text.json', 'r') as f:
    moves_text = json.load(f, object_pairs_hook=collections.OrderedDict)

processed_moves = {}

target = set()
category = set()
flags = set()
status = set()
volatileStatus = set()
types = set()

for num, (key, data) in enumerate(moves.items()):
    # moves with negative numbers are unofficial/not in the real games
    if data['num'] < 0:
        continue

    desc = moves_text[key if 'hiddenpower' not in key else 'hiddenpower']

    target.add(data['target'])
    category.add(data['category'])
    flags.update(list(data['flags'].keys()))
    types.add(data['type'])
    if 'secondary' in data and data['secondary']:
        status.add(data.get('secondary', {}).get('status'))
        volatileStatus.add(data.get('secondary', {}).get('volatileStatus'))


    move = {
        'num': data['num'],
        'name': data['name'],
        'type': data['type'],
        'accuracy': 100 if data['accuracy'] == True else data['accuracy'],
        'cannotMiss': data['accuracy'] == True,
        'basePower': data['basePower'],
        'category': data['category'],
        'pp': data['pp'],
        'priority': data['priority'],
        'target': data['target'],
        'critRatio': data['critRatio'] if 'critRatio' in data else 0,
        'multihit': data['multihit'] if 'multihit' in data else 1,
        'boosts': data['boosts'] if 'boosts' in data else None,
        'flags': data['flags'] if 'flags' in data else None,
        'secondary': data['secondary'] if 'secondary' in data else None,
        'desc': desc['desc'] if 'desc' in desc else desc['shortDesc'],
        'shortDesc': desc['shortDesc'] if 'shortDesc' in desc else desc['desc'],
        'isNonstandard': data['isNonstandard'] if 'isNonstandard' in data else False,
    }
    processed_moves[key] = move


with open('../../data/processed/moves.json', 'w') as f:
    json.dump(processed_moves, f, indent=4, sort_keys=False)


print(target)
print(category)
print(flags)
print(status)
print(volatileStatus)
print(types)
