import json
import collections

with open('../../data/raw/moves.json', 'r') as f:
    moves = json.load(f, object_pairs_hook=collections.OrderedDict)

with open('../../data/raw/moves_text.json', 'r') as f:
    moves_text = json.load(f, object_pairs_hook=collections.OrderedDict)

processed_moves = {}

for num, (key, data) in enumerate(moves.items()):
    # moves with negative numbers are unofficial/not in the real games
    if data['num'] < 0:
        continue

    desc = moves_text[key if 'hiddenpower' not in key else 'hiddenpower']

    move = {
        'num': data['num'],
        'name': data['name'],
        'type': data['type'],
        'accuracy': data['accuracy'],
        'cannotMisss': data['accuracy'] == True,
        'basePower': data['basePower'],
        'category': data['category'],
        'pp': data['pp'],
        'priority': data['priority'],
        'target': data['target'],
        'multihit': data['multihit'] if 'multihit' in data else None,
        'boosts': data['boosts'] if 'boosts' in data else None,
        'secondary': data['secondary'] if 'secondary' in data else None,
        'desc': desc['desc'] if 'desc' in desc else desc['shortDesc'],
        'shortDesc': desc['shortDesc'] if 'shortDesc' in desc else desc['desc'],
        'isNonstandard': data['isNonstandard'] if 'isNonstandard' in data else False,
    }
    processed_moves[key] = move


with open('../../data/processed/moves.json', 'w') as f:
    json.dump(processed_moves, f, indent=4, sort_keys=False)



