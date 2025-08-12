import json
import collections
from data_processing.util import type_to_vec
from data_processing.util import get_nested, pad
import numpy as np


def process_final_pokemon(path):
    with open(f'{path}/processed/pokemon.json', 'r') as f:
        pokemon = json.load(f, object_pairs_hook=collections.OrderedDict)

    processed_pokemon = {}
    embedding_features = {}


    for key, data in pokemon.items():
        pokemon = {
            'num': data['num'],
            'types': {
                'primary': type_to_vec(data['types'][0]),
                'secondary': type_to_vec(data['types'][1] if len(data['types']) == 2 else None, default=True)
            },
            'baseStats': {
                'hp': data['baseStats']['hp'] / 100,
                'atk': data['baseStats']['atk'] / 100,
                'def': data['baseStats']['def'] / 100,
                'spa': data['baseStats']['spa'] / 100,
                'spd': data['baseStats']['spd'] / 100,
                'spe': data['baseStats']['spe'] / 100
            },
            'heightm': data['heightm'] / 5,
            'weightkg': data['weightkg'] / 100,
            'stats': {
                'lead': {
                    'raw': get_nested(data, ['stats', 'lead', 'raw'], 0),
                    'real': get_nested(data, ['stats', 'lead', 'real'], 0),
                    'weighted': get_nested(data, ['stats', 'lead', 'weighted'], 0)
                },
                'usage': {
                    'raw': get_nested(data, ['stats', 'usage', 'raw'], 0),
                    'real': get_nested(data, ['stats', 'usage', 'real'], 0),
                    'weighted': get_nested(data, ['stats', 'usage', 'weighted'], 0)
                },
                'count': get_nested(data, ['stats', 'count'], 0),
                'weight': get_nested(data, ['stats', 'weight'], 0),
                'viability': get_nested(data, ['stats', 'viability'], [0, 0, 0, 0]),
                'abilities_frequency': (
                    [a['frequency'] for a in pad(
                        get_nested(data, ['stats', 'abilities'], []),
                        length=3,
                        value={'name': '', 'frequency': 0}
                    )]
                ),
                'items_frequency': (
                    [a['frequency'] for a in pad(
                        get_nested(data, ['stats', 'items_frequency'], []),
                        length=5,
                        value={'name': '', 'frequency': 0}
                    )]
                ),
                'tera': (
                    [type_to_vec(a['name'], default=True) for a in pad(
                        get_nested(data, ['stats', 'tera'], []),
                        length=5,
                        value={'name': '', 'frequency': 0}
                    )]
                ),
                'tera_frequency': (
                    [a['frequency'] for a in pad(
                        get_nested(data, ['stats', 'tera'], []),
                        length=5,
                        value={'name': '', 'frequency': 0}
                    )]
                ),
                # 'spreads': [
                #     {
                #         'nature': enum,
                #         'hp': int / 252,
                #         'atk': int / 252,
                #         'def': int / 252,
                #         'spa': int / 252,
                #         'spd': int / 252,
                #         'spe': int / 252,
                #         'frequency': float
                #     } x 5
                # ],
                'move_frequencies': (
                    [a['frequency'] for a in pad(
                        get_nested(data, ['stats', 'moves'], []),
                        length=15,
                        value={'name': '', 'frequency': 0}
                    )]
                ),
            }
        }
        processed_pokemon[key] = pokemon

    with open(f'{path}/final/pokemon.json', 'w') as f:
        json.dump(processed_pokemon, f, indent=4, sort_keys=False)

    print('processed final pokemon')


if __name__ == '__main__':
    process_final_pokemon('../../data')
