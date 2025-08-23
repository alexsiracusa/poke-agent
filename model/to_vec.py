import numpy as np
from enum import Enum
from typing import Dict
from poke_env.battle import PokemonGender, Effect, PokemonType, Status


def enum_to_one_hot(enum_cls, member):
    """Convert an enum member to a one-hot numpy array."""
    members = list(enum_cls)
    one_hot = np.zeros(len(members), dtype=int)
    if member is not None:
        idx = members.index(member)
        one_hot[idx] = 1
    return one_hot

def gender_to_vec(gender: PokemonGender):
    return list(enum_to_one_hot(PokemonGender, gender))

def pokemon_type_to_vec(type: PokemonType):
    return list(enum_to_one_hot(PokemonType, type))

def status_to_vec(status: Status):
    return list(enum_to_one_hot(Status, status))

def effect_to_vec(effect: Effect):
    return list(enum_to_one_hot(Effect, effect))

def effects_to_vec(effects: Dict[Effect, int]):
    vector = np.zeros(len(Effect), dtype=int)

    for effect, value in effects.items():
        vector += effect_to_vec(effect) * value

    return list(vector)







