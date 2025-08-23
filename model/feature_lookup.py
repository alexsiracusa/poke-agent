import json
import torch


class FeatureLookup:
    def __init__(self, path):
        self._abilities = None
        self._items = None
        self._moves = None
        self._pokemon = None

        self._ability_tensors = None
        self._item_tensors = None
        self._move_tensors = None
        self._pokemon_tensors = None

        try:
            # Loading tensors
            with open(f'{path}/lookup/abilities.json', 'r') as f:
                self._abilities = json.load(f)
            with open(f'{path}/lookup/items.json', 'r') as f:
                self._items = json.load(f)
            with open(f'{path}/lookup/moves.json', 'r') as f:
                self._moves = json.load(f)
            with open(f'{path}/lookup/pokemon.json', 'r') as f:
                self._pokemon = json.load(f)

            # Loading tensors
            self._ability_tensors = torch.load(f'{path}/tensors/abilities.pt')
            self._item_tensors = torch.load(f'{path}/tensors/items.pt')
            self._move_tensors = torch.load(f'{path}/tensors/moves.pt')
            self._pokemon_tensors = torch.load(f'{path}/tensors/pokemon.pt')

            # with open(f'{path}/tensors/abilities.pt', 'r') as f:
            #     self._ability_tensors = json.load(f)
            # with open(f'{path}/tensors/items.pt', 'r') as f:
            #     self._item_tensors = json.load(f)
            # with open(f'{path}/tensors/moves.pt', 'r') as f:
            #     self._move_tensors = json.load(f)
            # with open(f'{path}/tensors/pokemon.pt', 'r') as f:
            #     self._pokemon_tensors = json.load(f)

        except Exception as e:
            raise Exception(f'Failed to load lookup tables: {e}')

    def get_ability_tensor(self, ability):
        if isinstance(ability, str):
            ability = self._abilities[ability.lower()]

        return self._ability_tensors[ability]

    def get_item_tensor(self, item):
        if isinstance(item, str):
            item = self._items[item.lower()]

        return self._item_tensors[item]

    def get_move_tensor(self, move):
        if isinstance(move, str):
            move = self._moves[move.lower()]

        return self._move_tensors[move]

    def get_pokemon_tensor(self, pokemon):
        if isinstance(pokemon, str):
            pokemon = self._pokemon[pokemon.lower()]

        return self._pokemon_tensors[pokemon]


if __name__ == '__main__':
    lookup = FeatureLookup(path='../data')

    print(lookup.get_move_tensor(210))
    print(lookup.get_move_tensor('flamethrower'))
    print(lookup.get_move_tensor('thunderbolt'))

