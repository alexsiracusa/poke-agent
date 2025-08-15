from metamon.interface import (
    ObservationSpace,
    UniversalState,
    UniversalMove,
    UniversalPokemon,
    consistent_move_order,
    register_observation_space,
    consistent_pokemon_order,
    clean_name
)
import gymnasium as gym
import numpy as np
import string
import json

@register_observation_space()
class CustomDefaultObservationSpace(ObservationSpace):
    """The default observation space used by the paper.

    Observations become a dictionary with two keys:
        - "numbers": A 48-dimensional vector of numerical features
        - "text": A string of text features with inconsistent length, but a consistent
            number of whitespace-separated words.
    """

    @property
    def gym_space(self):
        return gym.spaces.Dict(
            {
                "numbers": gym.spaces.Box(
                    low=-10.0,
                    high=10.0,
                    shape=(48,),
                    dtype=np.float32,
                ),
                "text": gym.spaces.Text(
                    max_length=900,
                    min_length=800,
                    charset=set(string.ascii_lowercase)
                    | set(str(n) for n in range(0, 10))
                    | {"<", ">"},
                ),
            }
        )

    @property
    def tokenizable(self) -> dict[str, int]:
        return {
            "text": 87,
        }

    def _get_move_string_features(self, move: UniversalMove, active: bool) -> list[str]:
        out = [clean_name(move.name)]
        if active:
            out += [clean_name(move.move_type), clean_name(move.category)]
        return out

    def _get_move_pad_string(self, active: bool) -> list[str]:
        out = ["<blank>"]
        if active:
            out += ["<blank>", "<blank>"]
        return out

    def _get_move_numerical_features(
        self, move: UniversalMove, active: bool
    ) -> list[float]:
        if not active:
            return []
        # notably missing PP, which (for now) is too unreliable across replay parser vs. poke-env vs. actual pokemon showdown
        return [move.base_power / 200.0, move.accuracy, move.priority / 5.0]

    def _get_move_pad_numerical(self, active: bool) -> list[float]:
        if not active:
            return []
        return [-2.0] * 3

    def _get_pokemon_string_features(
        self, pokemon: UniversalPokemon, active: bool
    ) -> list[str]:
        out = [pokemon.name, pokemon.item, pokemon.ability]
        if active:
            out += [pokemon.types, pokemon.effect, pokemon.status]
        else:
            out += ["<moveset>"]
            move_num = -1
            for move_num, move in enumerate(consistent_move_order(pokemon.moves)):
                out += self._get_move_string_features(move, active=False)
            while move_num < 3:
                out += self._get_move_pad_string(active=False)
                move_num += 1
        return out

    def _get_pokemon_pad_string(self, active: bool) -> list[str]:
        blanks = 3 + (4 if active else 5)
        return ["<blank>"] * blanks

    def _get_pokemon_numerical_features(
        self, pokemon: UniversalPokemon, active: bool
    ) -> list[float]:
        out = [pokemon.hp_pct]
        if active:
            stat = lambda s: getattr(pokemon, f"base_{s}") / 255.0
            boost = lambda b: getattr(pokemon, f"{b}_boost") / 6.0
            out.append(pokemon.lvl / 100.0)
            out += map(stat, ["atk", "spa", "def", "spd", "spe", "hp"])
            out += map(
                boost, ["atk", "spa", "def", "spd", "spe", "accuracy", "evasion"]
            )
        return out

    def _get_pokemon_pad_numerical(self, active: bool) -> list[float]:
        blanks = 1 + (14 if active else 0)
        return [-2.0] * blanks

    def _get_move_features(self, move: UniversalMove):
        return {
            'name': move.name,
            'current_pp': move.current_pp
        }

    def _get_pokemon_features(self, pokemon: UniversalPokemon, active=False):
        return {
            'base_species': pokemon.base_species,
            'types': pokemon.types.split(' '),
            'item': pokemon.item,
            'ability': pokemon.ability,

            'active': active,
            'hp_pct': pokemon.hp_pct,
            'lvl': pokemon.lvl,
            'effect': pokemon.effect,
            'status': pokemon.status,
            'tera_type': pokemon.tera_type,

            'boosts': {
                'atk': pokemon.atk_boost,
                'def': pokemon.def_boost,
                'spa': pokemon.spa_boost,
                'spd': pokemon.spd_boost,
                'spe': pokemon.spe_boost,
                'acc': pokemon.accuracy_boost,
                'eva': pokemon.evasion_boost
            },

            'moves': [self._get_move_features(move) for move in pokemon.moves]
        }

    def state_to_obs(self, state: UniversalState) -> dict[str, np.ndarray]:
        return {
            'player_active_pokemon': self._get_pokemon_features(state.player_active_pokemon, active=True),
            'opponent_active_pokemon': self._get_pokemon_features(state.opponent_active_pokemon, active=True),
            'available_switches': [self._get_pokemon_features(pokemon) for pokemon in state.available_switches],

            'player_prev_move': self._get_move_features(state.player_prev_move),
            'opponent_prev_move': self._get_move_features(state.opponent_prev_move),

            'player_conditions': state.player_conditions,  # ex: 'stealthrock'
            'opponent_conditions': state.opponent_conditions,
            'weather': state.weather,

            'opponents_remaining': state.opponents_remaining,
            'battle_field': state.battle_field,
            'battle_lost': state.battle_lost,
            'battle_won': state.battle_won,
            'can_tera': state.can_tera,
            'forced_switch': state.forced_switch,

            'opponent_teampreview': state.opponent_teampreview
        }