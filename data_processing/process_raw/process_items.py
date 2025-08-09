import json
import collections

with open('../../data/raw/items.json', 'r') as f:
    items = json.load(f, object_pairs_hook=collections.OrderedDict)

with open('../../data/raw/items_text.json', 'r') as f:
    items_text = json.load(f, object_pairs_hook=collections.OrderedDict)

processed_items = {}

for num, (key, data) in enumerate(items.items()):
    # items with negative numbers are unofficial/not in the real games
    if data['num'] < 0:
        continue

    desc = items_text[key]

    item = {
        'num': data['num'],
        'name': data['name'],
        'shortDesc': desc['shortDesc'],
        'isBerry': data['isBerry'] if 'isBerry' in desc else False,
        'isNonstandard': data['isNonstandard'] if 'isNonstandard' in data else False,
        'gen': data['gen'],
    }
    processed_items[key] = item


with open('../../data/processed/items.json', 'w') as f:
    json.dump(processed_items, f, indent=4, sort_keys=False)



