import torch
import torch.nn as nn
from poke_env.battle import Battle, Pokemon
from util import pad, flatten_list

from feature_lookup import FeatureLookup
from hybrid_embedding import HybridEmbedding


NUM_ABILITIES = 311
NUM_ITEMS = 249
NUM_MOVES = 686
NUM_POKEMON = 1330

class STATIC_FEATURES:
    ABILITIES = 1
    ITEMS = 1
    MOVES = 104
    POKEMON = 241

class LEARNABLE_FEATURES:
    ABILITIES = 50
    ITEMS = 50
    MOVES = 50
    POKEMON = 50



class TimestepEncoder(nn.Module):
    def __init__(self, path):
        super(TimestepEncoder, self).__init__()
        self.lookup = FeatureLookup(path)

        self.ability_embeddings = HybridEmbedding(NUM_ABILITIES, STATIC_FEATURES.ABILITIES, LEARNABLE_FEATURES.ABILITIES, self.lookup.ability_tensors)
        self.item_embeddings = HybridEmbedding(NUM_ITEMS, STATIC_FEATURES.ITEMS, LEARNABLE_FEATURES.ITEMS, self.lookup.item_tensors)
        self.move_embeddings = HybridEmbedding(NUM_MOVES, STATIC_FEATURES.MOVES, LEARNABLE_FEATURES.MOVES, self.lookup.move_tensors)
        self.pokemon_embeddings = HybridEmbedding(NUM_POKEMON, STATIC_FEATURES.POKEMON, LEARNABLE_FEATURES.POKEMON, self.lookup.pokemon_tensors)

    def encode_pokemon(self, pokemon : list[str]):
        pokemon_ids = torch.tensor([self.lookup.pokemon[poke] for poke in pokemon])
        feature_tensor = self.pokemon_embeddings(pokemon_ids)

        embeddings = self.lookup.get_pokemon_embeddings(pokemon)
        embeddings_tensor = torch.stack([torch.cat([
            self.ability_embeddings(torch.tensor(features['abilities'])).flatten(),
            self.item_embeddings(torch.tensor(features['items'])).flatten(),
            self.move_embeddings(torch.tensor(features['moves'])).flatten(),
        ]) for features in embeddings])

        return torch.cat([feature_tensor, embeddings_tensor], dim=1)

    def forward(self, battle: Battle):
        pokemon = flatten_list([
            battle.active_pokemon.species if battle.active_pokemon else 'nothing',
            battle.opponent_active_pokemon.species if battle.opponent_active_pokemon else 'nothing',
            pad([poke.species for poke in battle.available_switches], 5, 'nothing'),
            pad([poke.species for key, poke in battle.opponent_team.items() if not poke.active], 5, 'nothing')
        ])

        static_features = self.encode_pokemon(pokemon)

        print(pokemon, static_features.shape)



if __name__ == '__main__':
    model = TimestepEncoder(path='../data')

    print(model.encode_pokemon(['ivysaur', 'venusaur']).shape)


