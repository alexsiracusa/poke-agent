import json
import torch


class FeatureLookup:
    def __init__(self, path):
        self.abilities = None
        self.items = None
        self.moves = None
        self.pokemon = None

        self.pokemon_embeddings = None

        self.ability_tensors = None
        self.item_tensors = None
        self.move_tensors = None
        self.pokemon_tensors = None

        try:
            # Loading tensors
            with open(f'{path}/lookup/abilities.json', 'r') as f:
                self.abilities = json.load(f)
            with open(f'{path}/lookup/items.json', 'r') as f:
                self.items = json.load(f)
            with open(f'{path}/lookup/moves.json', 'r') as f:
                self.moves = json.load(f)
            with open(f'{path}/lookup/pokemon.json', 'r') as f:
                self.pokemon = json.load(f)
            with open(f'{path}/final/pokemon_embeddings.json', 'r') as f:
                self.pokemon_embeddings = json.load(f)

            # Loading tensors
            self.ability_tensors = torch.load(f'{path}/tensors/abilities.pt')
            self.item_tensors = torch.load(f'{path}/tensors/items.pt')
            self.move_tensors = torch.load(f'{path}/tensors/moves.pt')
            self.pokemon_tensors = torch.load(f'{path}/tensors/pokemon.pt')

        except Exception as e:
            raise Exception(f'Failed to load data: {e}')

    def get_pokemon_embeddings(self, pokemon):
        return [self.pokemon_embeddings[poke] for poke in pokemon]


if __name__ == '__main__':
    lookup = FeatureLookup(path='../data')

    print(lookup.move_tensors[210])
    print(lookup.moves['flamethrower'])
    print(lookup.moves['thunderbolt'])

    print(lookup.ability_tensors.shape)
    print(lookup.item_tensors.shape)
    print(lookup.move_tensors.shape)
    print(lookup.pokemon_tensors.shape)

