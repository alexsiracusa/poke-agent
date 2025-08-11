import json
import collections


def process_raw_abilities(path):
    with open(f'{path}/raw/abilities.json', 'r') as f:
        abilities = json.load(f, object_pairs_hook=collections.OrderedDict)

    with open(f'{path}/raw/abilities_text.json', 'r') as f:
        abilities_text = json.load(f, object_pairs_hook=collections.OrderedDict)

    processed_abilities = {}

    for num, (key, data) in enumerate(abilities.items()):
        # abilities with negative numbers are unofficial/not in the real games
        if data['num'] < 0:
            continue

        desc = abilities_text[key]
        ability = {
            'num': data['num'],
            'name': data['name'],
            'desc': desc['desc'] if 'desc' in desc else desc['shortDesc'],
            'shortDesc': desc['shortDesc'],
            'rating': data['rating'],
        }
        processed_abilities[key] = ability


    with open(f'{path}/processed/abilities.json', 'w') as f:
        json.dump(processed_abilities, f, indent=4, sort_keys=False)

    print('processed raw abilities')


if __name__ == '__main__':
    process_raw_abilities('../../data')
