import json
import collections
from data_processing.util import type_to_vec, nature_to_vec
from data_processing.util import get_nested, pad
from data_processing.consts import TOP_N_ITEMS, TOP_N_TERA, TOP_N_SPREADS, TOP_N_MOVES


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
                        length=TOP_N_ITEMS,
                        value={'name': '', 'frequency': 0}
                    )]
                ),
                'tera': (
                    [type_to_vec(a['name'], default=True) for a in pad(
                        get_nested(data, ['stats', 'tera'], []),
                        length=TOP_N_TERA,
                        value={'name': '', 'frequency': 0}
                    )]
                ),
                'tera_frequency': (
                    [a['frequency'] for a in pad(
                        get_nested(data, ['stats', 'tera'], []),
                        length=TOP_N_TERA,
                        value={'name': '', 'frequency': 0}
                    )]
                ),
                'spreads': (
                    [{
                        'nature': nature_to_vec(a['nature'], default=True),
                        'hp': a['hp'] / 252,
                        'atk': a['atk'] / 252,
                        'def': a['def'] / 252,
                        'spa': a['spa'] / 252,
                        'spd': a['spd'] / 252,
                        'spe': a['spe'] / 252,
                        'frequency': a['frequency']
                    } for a in pad(
                        get_nested(data, ['stats', 'spreads'], []),
                        length=TOP_N_SPREADS,
                        value={'nature': '', 'hp': 0, 'atk': 0, 'def': 0, 'spa': 0, 'spd': 0, 'spe': 0, 'frequency': 0}
                    )]
                ),
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
