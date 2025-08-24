import numpy as np
from enum import Enum
from typing import Dict
from poke_env.environment import PokemonGender, PokemonType, Effect, Status, Weather, Field, SideCondition


def enum_to_one_hot(enum_cls, member):
    """Convert an enum member to a one-hot numpy array."""
    members = list(enum_cls)
    one_hot = np.zeros(len(members), dtype=int)
    if member is not None:
        idx = members.index(member)
        one_hot[idx] = 1
    return one_hot.tolist()

def gender_to_vec(gender: PokemonGender):
    return enum_to_one_hot(PokemonGender, gender)

def pokemon_type_to_vec(type: PokemonType):
    return enum_to_one_hot(PokemonType, type)

def status_to_vec(status: Status):
    return enum_to_one_hot(Status, status)


# EFFECT
# Figuring out the max value for all like 250 effects is too much work
# and not worth it, so I'm not doing it.
effect_max_value = []

def effect_to_vec(effect: Effect):
    return enum_to_one_hot(Effect, effect)

def effects_to_vec(effects: Dict[Effect, int]):
    vector = np.zeros(len(Effect), dtype=int)

    for effect, value in effects.items():
        vector += np.array(effect_to_vec(effect)) * value

    return vector.tolist()


# WEATHER
weather_max_values = [
    1, # UNKNOWN
    1, # DESOLATELAND
    1, # DELTASTREAM
    8, # HAIL
    1, # PRIMORDIALSEA
    8, # RAINDANCE
    8, # SANDSTORM
    8, # SNOWSCAPE = SNOW
    8, # SUNNYDAY
]

# Put in poke_env abstract_battle.py around like 650 to fix weather turn counting
#
#   elif event[1] == "-weather":
#       weather = event[2]
#       if weather == "none":
#           self._weather = {}
#           return
#       else:
#           if Weather.from_showdown_message(weather) not in self._weather:
#               self._weather = {Weather.from_showdown_message(weather): self.turn}

def weather_to_vec(weather: Weather):
    return enum_to_one_hot(Weather, weather)

def weathers_to_vec(weathers: Dict[Weather, int], turn: int):
    vector = np.zeros(len(Weather), dtype=int)

    for weather, value in weathers.items():
        vector += np.array(weather_to_vec(weather)) * (turn - value)

    features = []
    for value, max_value in zip(vector, weather_max_values):
        features.append(np.eye(max_value + 1)[value])

    return np.concatenate(features, axis=0).tolist()


# FIELDS
field_max_values = [
    1, # UNKNOWN
    8, # ELECTRIC_TERRAIN
    8, # GRASSY_TERRAIN
    5, # GRAVITY
    5, # HEAL_BLOCK
    5, # MAGIC_ROOM
    8, # MISTY_TERRAIN
    5, # MUD_SPORT
    5, # MUD_SPOT
    8, # PSYCHIC_TERRAIN
    5, # TRICK_ROOM
    5, # WATER_SPORT
    5, # WONDER_ROOM
]

def field_to_vec(field: Field):
    return enum_to_one_hot(Field, field)

def fields_to_vec(fields: Dict[Field, int], turn: int):
    vector = np.zeros(len(Field), dtype=int)

    for field, value in fields.items():
        vector += np.array(field_to_vec(field)) * (turn - value)

    features = []
    for value, max_value in zip(vector, field_max_values):
        features.append(np.eye(max_value + 1)[value])

    return np.concatenate(features, axis=0).tolist()


# SIDE CONDITIONS
side_condition_max_values = [
    1, # UNKNOWN
    8, # AURORA_VEIL
    1, # CRAFTY_SHIELD
    5, # FIRE_PLEDGE
    4, # G_MAX_CANNONADE
    4, # G_MAX_STEELSURGE
    4, # G_MAX_VINE_LASH
    4, # G_MAX_VOLCALITH
    4, # G_MAX_WILDFIRE
    1, # GRASS_PLEDGE
    8, # LIGHT_SCREEN
    5, # LUCKY_CHANT
    1, # MATBLOCK
    5, # MIST
    1, # QUICK_GUARD
    8, # REFLECT
    5, # SAFEGUARD
    3, # SPIKES
    1, # STEALTH_ROCK
    1, # STICKY_WEB
    4, # TAILWIND
    2, # TOXIC_SPIKES
    5, # WATER_PLEDGE
    1, # WIDE_GUARD
]

def side_condition_to_vec(side_condition: SideCondition):
    return enum_to_one_hot(SideCondition, side_condition)

def side_conditions_to_vec(side_conditions: Dict[SideCondition, int], turn: int):
    vector = np.zeros(len(SideCondition), dtype=int)

    for side_condition, value in side_conditions.items():
        if side_condition in [SideCondition.SPIKES, SideCondition.TOXIC_SPIKES]:
            vector += np.array(side_condition_to_vec(side_condition)) * value
        else:
            vector += np.array(side_condition_to_vec(side_condition)) * (turn - value)

    features = []
    for value, max_value in zip(vector, side_condition_max_values):
        features.append(np.eye(max_value + 1)[value])

    return np.concatenate(features, axis=0).tolist()







