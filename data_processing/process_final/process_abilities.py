import json
import collections


def process_final_abilities(path):
    with open(f'{path}/processed/abilities.json', 'r') as f:
        moves = json.load(f, object_pairs_hook=collections.OrderedDict)

    processed_abilities = {}

    for key, data in moves.items():
        ability = {
            "rating": data['rating'] / 5,
        }
        processed_abilities[key] = ability

    with open(f'{path}/final/abilities.json', 'w') as f:
        json.dump(processed_abilities, f, indent=4, sort_keys=False)

    print('processed final abilities')


if __name__ == '__main__':
    process_final_abilities('../../data')

