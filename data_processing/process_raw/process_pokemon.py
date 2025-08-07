import json
import collections

with open('../../data/raw/pokedex.json', 'r') as f:
    pokemon = json.load(f, object_pairs_hook=collections.OrderedDict)

with open('../../data/raw/gen9ou.json', 'r') as f:
    pokemon_stats = json.load(f, object_pairs_hook=collections.OrderedDict)["pokemon"]


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
        'abilities': data['abilities']
    }

    if data['name'] in pokemon_stats:
        stats = pokemon_stats[data['name']]


    processed_pokemon[key] = pokemon

    print(pokemon)


with open('../../data/processed/pokemon.json', 'w') as f:
    json.dump(processed_pokemon, f, indent=4, sort_keys=False)