import torch
import torch.nn as nn
from typing import List, Optional
from poke_env.battle import Battle, Pokemon, PokemonType

from util import pad, flatten_list
from feature_lookup import FeatureLookup
from hybrid_embedding import HybridEmbedding
from to_vec import gender_to_vec, effects_to_vec, pokemon_type_to_vec, status_to_vec


NUM_ABILITIES = 313
NUM_ITEMS = 250
NUM_MOVES = 687
NUM_POKEMON = 1331

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

    def _encode_pokemon_species(self, pokemon : List[str]) -> torch.tensor:
        pokemon_ids = torch.tensor([self.lookup.pokemon[poke] for poke in pokemon])
        feature_tensor = self.pokemon_embeddings(pokemon_ids)

        embeddings = self.lookup.get_pokemon_embeddings(pokemon)
        embeddings_tensor = torch.stack([torch.cat([
            self.ability_embeddings(torch.tensor(features['abilities'])).flatten(),
            self.item_embeddings(torch.tensor(features['items'])).flatten(),
            self.move_embeddings(torch.tensor(features['moves'])).flatten(),
        ]) for features in embeddings])

        return torch.cat([feature_tensor, embeddings_tensor], dim=1)

    def _encode_pokemon(self, pokemon : List[Optional[Pokemon]]) -> torch.tensor:
        features = torch.stack([torch.tensor(flatten_list([
            flatten_list([                        # 60
                pokemon_type_to_vec(type)
                for type in
                pad(poke.types, 3, None)
            ]),
            gender_to_vec(poke.gender),           # 3
            poke.level / 100,                     # 1
            poke.current_hp / 500,                # 1
            poke.max_hp / 500,                    # 1
            poke.current_hp_fraction,             # 1
            poke.active,                          # 1
            poke.boosts['accuracy'] / 6,          # 1
            poke.boosts['atk'] / 6,               # 1
            poke.boosts['def'] / 6,               # 1
            poke.boosts['evasion'] / 6,           # 1
            poke.boosts['spa'] / 6,               # 1
            poke.boosts['spd'] / 6,               # 1
            poke.boosts['spe'] / 6,               # 1
            effects_to_vec(poke.effects),         # 224
            poke.first_turn,                      # 1
            poke.is_terastallized,                # 1
            pokemon_type_to_vec(poke.tera_type),  # 20
            poke.must_recharge,                   # 1
            poke.protect_counter,                 # 1
            poke.revealed,                        # 1
            (poke.stats['hp'] or -500) / 500,     # 1
            (poke.stats['atk'] or -500) / 500,    # 1
            (poke.stats['def'] or -500) / 500,    # 1
            (poke.stats['spa'] or -500) / 500,    # 1
            (poke.stats['spd'] or -500) / 500,    # 1
            (poke.stats['spe'] or -500) / 500,    # 1
            status_to_vec(poke.status),           # 7
            poke.status_counter,                  # 1
        ])) if poke is not None else torch.zeros(338) for poke in pokemon])

        abilities = self.ability_embeddings(torch.tensor([
            self.lookup.abilities[poke.ability or 'unknown' if poke else 'nothing'] for poke in pokemon
        ]))

        moves = torch.stack([
            self.move_embeddings(torch.tensor([
                self.lookup.moves[move] for move in
                pad(list(poke.moves.keys()) if poke else [], 4, 'unknown')
            ])).flatten()
            for poke in pokemon
        ])

        items = self.item_embeddings(torch.tensor([
            self.lookup.items[
                (
                    poke.item or 'unknown'
                    if poke.item != 'unknown_item' else 'unknown'
                ) if poke else 'nothing'
            ] for poke in pokemon
        ]))

        preparing_moves = self.move_embeddings(torch.tensor([
            self.lookup.moves[poke.preparing_move.id if poke and poke.preparing_move else 'nothing'] for poke in pokemon
        ]))

        return torch.cat([features, abilities, moves, items, preparing_moves], dim=1)


    def forward(self, battle: Battle):
        # ----------------
        # POKEMON FEATURES
        # ----------------
        pokemon: List[Optional[Pokemon]] = flatten_list([
            battle.active_pokemon,
            battle.opponent_active_pokemon,
            pad([poke for poke in battle.available_switches], 5, None),
            pad([poke for key, poke in battle.opponent_team.items() if not poke.active], 5, None)
        ])

        # Species related features
        pokemon_species = [poke.species if poke is not None else 'nothing' for poke in pokemon]
        species_features = self._encode_pokemon_species(pokemon_species)

        # Individual and Battle related features
        individual_features = self._encode_pokemon(pokemon)

        # Final Pokemon features
        pokemon_features = torch.cat([species_features, individual_features], dim=1)


        # ----------------
        # BATTLE CONDITION FEATURES
        # ----------------

        # self._weather: Dict[Weather, int] = {}
        # self._fields: Dict[Field, int] = {}  # set()
        # self._opponent_side_conditions: Dict[SideCondition, int] = {}  # set()
        # self._side_conditions: Dict[SideCondition, int] = {}  # set()
        # self._reviving: bool = False
        # self._opponent_used_mega_evolve = False
        # self._opponent_used_z_move = False
        # self._opponent_used_dynamax = False
        # self._opponent_used_tera = False
        # self._used_mega_evolve = False
        # self._used_z_move = False
        # self._used_dynamax = False
        # self._used_tera = False



        return pokemon_features.flatten()



if __name__ == '__main__':
    model = TimestepEncoder(path='../data')

    print(model._encode_pokemon_species(['ivysaur', 'venusaur']).shape)


