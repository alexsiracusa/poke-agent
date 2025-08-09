import json
import collections

with open('../../data/raw/pokedex.json', 'r') as f:
    pokemon = json.load(f, object_pairs_hook=collections.OrderedDict)

with open('../../data/raw/gen9ou.json', 'r') as f:
    pokemon_stats = json.load(f, object_pairs_hook=collections.OrderedDict)["pokemon"]


TOP_N_ITEMS = 5
TOP_N_TERA = 5
TOP_N_SPREADS = 5
TOP_N_MOVES = 15

processed_pokemon = {}

for num, (key, data) in enumerate(pokemon.items()):
    # abilities with negative numbers are unofficial/not in the real games
    if data['num'] < 0:
        continue

    pokemon = {
        'num': data['num'],
        'name': data['name'],
        'types': data['types'],
        'baseStats': data['baseStats'],
        'heightm': data['heightm'],
        'weightkg': data['weightkg'],
        'abilities': list(data['abilities'].values())
    }

    def process_spread(spread: str, frequency: float):
        # ex: Adamant:0/252/0/0/4/252
        spread = spread.replace(':', '/')
        spread = spread.split('/')

        return {
            'nature': spread[0],
            'hp': int(spread[1]),
            'atk': int(spread[2]),
            'def': int(spread[3]),
            'spa': int(spread[4]),
            'spd': int(spread[5]),
            'spe': int(spread[6]),
            'frequency': frequency,
        }


    def process_stats(stats):
        return {
            'lead': stats['lead'],
            'usage': stats['usage'],
            'count': stats['count'],
            'weight': stats['weight'],
            'viability': stats['viability'],
            'abilities': [{'name': key, 'frequency': value} for key, value in stats['abilities'].items()],
            'items': [{'name': key, 'frequency': value} for key, value in stats['items'].items()][:TOP_N_ITEMS],
            'tera': [{'name': key, 'frequency': value} for key, value in stats['teraTypes'].items()][:TOP_N_TERA],
            'spreads': [process_spread(key, value) for key, value in stats['spreads'].items()][:TOP_N_SPREADS],
            'moves': [{'name': key, 'frequency': value} for key, value in stats['moves'].items()][:TOP_N_MOVES],
        }

    if data['name'] in pokemon_stats:
        stats = pokemon_stats[data['name']]
        pokemon['stats'] = process_stats(stats)

    processed_pokemon[key] = pokemon

    print(pokemon)


with open('../../data/processed/pokemon.json', 'w') as f:
    json.dump(processed_pokemon, f, indent=4, sort_keys=False)