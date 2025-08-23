import json
import collections
from data_processing.util import type_to_vec, move_category_to_vec, move_target_to_vec, status_to_vec, volatile_status_to_vec
from data_processing.util import get_nested


def process_final_moves(path):
    with open(f'{path}/processed/moves.json', 'r') as f:
        moves = json.load(f, object_pairs_hook=collections.OrderedDict)

    processed_moves = {}

    for key, data in moves.items():
        if data['isNonstandard']:
            continue

        move = {
            'num': data['num'],
            'type': type_to_vec(data['type']),
            'accuracy': data['accuracy'] / 100,
            'cannotMiss': data['accuracy'] == True,
            'basePower': data['basePower'] / 100,
            'category': move_category_to_vec(data['category']),
            'pp': data['pp'] / 16,
            'priority': data['priority'] / 7,
            'target': move_target_to_vec(data['target']),
            'critRatio': data['critRatio'] if 'critRatio' in data else 0,
            'multihit': data['multihit'] if type(data['multihit']) == list else [data['multihit'], data['multihit']],
            'boosts': {
                "atk": get_nested(data, ['boosts', 'atk'], 0) / 6,
                "def": get_nested(data, ['boosts', 'def'], 0) / 6,
                "spa": get_nested(data, ['boosts', 'spa'], 0) / 6,
                "spd": get_nested(data, ['boosts', 'spd'], 0) / 6,
                "spe": get_nested(data, ['boosts', 'spe'], 0) / 6
            },
            'flags': {
                "heal": get_nested(data, ['flags', 'heal'], 0),
                "dance": get_nested(data, ['flags', 'dance'], 0),
                "wind": get_nested(data, ['flags', 'wind'], 0),
                "distance": get_nested(data, ['flags', 'distance'], 0),
                "protect": get_nested(data, ['flags', 'protect'], 0),
                "failmefirst": get_nested(data, ['flags', 'failmefirst'], 0),
                "mirror": get_nested(data, ['flags', 'mirror'], 0),
                "reflectable": get_nested(data, ['flags', 'reflectable'], 0),
                "contact": get_nested(data, ['flags', 'contact'], 0),
                "powder": get_nested(data, ['flags', 'powder'], 0),
                "pledgecombo": get_nested(data, ['flags', 'pledgecombo'], 0),
                "charge": get_nested(data, ['flags', 'charge'], 0),
                "failcopycat": get_nested(data, ['flags', 'failcopycat'], 0),
                "recharge": get_nested(data, ['flags', 'recharge'], 0),
                "snatch": get_nested(data, ['flags', 'snatch'], 0),
                "sound": get_nested(data, ['flags', 'sound'], 0),
                "pulse": get_nested(data, ['flags', 'pulse'], 0),
                "metronome": get_nested(data, ['flags', 'metronome'], 0),
                "defrost": get_nested(data, ['flags', 'defrost'], 0),
                "bite": get_nested(data, ['flags', 'bite'], 0),
                "allyanim": get_nested(data, ['flags', 'allyanim'], 0),
                "punch": get_nested(data, ['flags', 'punch'], 0),
                "noassist": get_nested(data, ['flags', 'noassist'], 0),
                "nonsky": get_nested(data, ['flags', 'nonsky'], 0),
                "bullet": get_nested(data, ['flags', 'bullet'], 0),
                "slicing": get_nested(data, ['flags', 'slicing'], 0),
                "nosleeptalk": get_nested(data, ['flags', 'nosleeptalk'], 0),
                "failinstruct": get_nested(data, ['flags', 'failinstruct'], 0),
                "cantusetwice": get_nested(data, ['flags', 'cantusetwice'], 0),
                "failencore": get_nested(data, ['flags', 'failencore'], 0),
                "failmimic": get_nested(data, ['flags', 'failmimic'], 0),
                "gravity": get_nested(data, ['flags', 'gravity'], 0),
                "nosketch": get_nested(data, ['flags', 'nosketch'], 0),
                "mustpressure": get_nested(data, ['flags', 'mustpressure'], 0),
                "bypasssub": get_nested(data, ['flags', 'bypasssub'], 0),
                "futuremove": get_nested(data, ['flags', 'futuremove'], 0),
            },
            'secondary': {
                "chance": get_nested(data, ['secondary', 'chance'], 0) / 100,
                "status": status_to_vec(get_nested(data, ['secondary', 'status'], ""), default=True),
                "volatileStatus": volatile_status_to_vec(get_nested(data, ['secondary', 'volatileStatus'], ""), default=True),
                "self": {
                    "boosts": {
                        "atk": get_nested(data, ['secondary', 'self', 'boosts', 'atk'], 0) / 6,
                        "def": get_nested(data, ['secondary', 'self', 'boosts', 'def'], 0) / 6,
                        "spa": get_nested(data, ['secondary', 'self', 'boosts', 'spa'], 0) / 6,
                        "spd": get_nested(data, ['secondary', 'self', 'boosts', 'spd'], 0) / 6,
                        "spe": get_nested(data, ['secondary', 'self', 'boosts', 'spe'], 0) / 6
                    }
                }
            }
        }
        processed_moves[key] = move

    with open(f'{path}/final/moves.json', 'w') as f:
        json.dump(processed_moves, f, indent=4, sort_keys=False)

    print('processed final moves')


if __name__ == '__main__':
    process_final_moves('../../data')

