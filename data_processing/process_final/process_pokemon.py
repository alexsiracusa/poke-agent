import json
import collections
from data_processing.util import type_to_vec
from data_processing.util import get_nested


def process_final_pokemon(path):
    with open(f'{path}/processed/pokemon.json', 'r') as f:
        pokemon = json.load(f, object_pairs_hook=collections.OrderedDict)

    processed_pokemon = {}

    for key, data in pokemon.items():
        pokemon = {
            'num': data['num'],
        }
        processed_pokemon[key] = pokemon

    with open(f'{path}/final/pokemon.json', 'w') as f:
        json.dump(processed_pokemon, f, indent=4, sort_keys=False)

    print('processed final moves')


if __name__ == '__main__':
    process_final_pokemon('../../data')

