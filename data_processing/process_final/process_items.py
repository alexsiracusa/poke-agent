import json
import collections


def process_final_items(path):
    with open(f'{path}/processed/items.json', 'r') as f:
        moves = json.load(f, object_pairs_hook=collections.OrderedDict)

    processed_items = {}

    for key, data in moves.items():
        if data['isNonstandard']:
            continue

        move = {
            "isBerry": data['isBerry'],
        }
        processed_items[key] = move

    with open(f'{path}/final/items.json', 'w') as f:
        json.dump(processed_items, f, indent=4, sort_keys=False)

    print('processed final items')


if __name__ == '__main__':
    process_final_items('../../data')

