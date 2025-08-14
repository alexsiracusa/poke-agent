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

    def state_to_obs(self, state: UniversalState) -> dict[str, np.ndarray]:
        player_str = ["<player>"] + self._get_pokemon_string_features(
            state.player_active_pokemon, active=True
        )
        numerical = [
            state.opponents_remaining / 6.0
        ] + self._get_pokemon_numerical_features(
            state.player_active_pokemon, active=True
        )

        # consistent move order
        move_str, move_num = [], -1
        for move_num, move in enumerate(
            consistent_move_order(state.player_active_pokemon.moves)
        ):
            move_str += ["<move>"] + self._get_move_string_features(move, active=True)
            numerical += self._get_move_numerical_features(move, active=True)

        while move_num < 3:
            move_str += ["<move>"] + self._get_move_pad_string(active=True)
            numerical += self._get_move_pad_numerical(active=True)
            move_num += 1

        # consistent switch order
        switch_str, switch_num = [], -1
        for switch_num, switch in enumerate(
            consistent_pokemon_order(state.available_switches)
        ):
            switch_str += ["<switch>"] + self._get_pokemon_string_features(
                switch, active=False
            )
            numerical += self._get_pokemon_numerical_features(switch, active=False)
        while switch_num < 4:
            switch_str += ["<switch>"] + self._get_pokemon_pad_string(active=False)
            numerical += self._get_pokemon_pad_numerical(active=False)
            switch_num += 1

        force_switch = "<forcedswitch>" if state.forced_switch else "<anychoice>"
        opponent_str = ["<opponent>"] + self._get_pokemon_string_features(
            state.opponent_active_pokemon, active=True
        )
        numerical += self._get_pokemon_numerical_features(
            state.opponent_active_pokemon, active=True
        )
        global_str = ["<conditions>"] + [
            state.weather,
            state.player_conditions,
            state.opponent_conditions,
        ]
        prev_move_str = (
            ["<player_prev>"]
            + self._get_move_string_features(state.player_prev_move, active=False)
            + ["<opp_prev>"]
            + self._get_move_string_features(state.opponent_prev_move, active=False)
        )
        full_text_list = (
            [f"<{state.format}>", force_switch]
            + player_str
            + move_str
            + switch_str
            + opponent_str
            + global_str
            + prev_move_str
        )
        # length should be 85 (type features have 2 words --> final word length of 87)
        text = " ".join(full_text_list)
        text = np.array(text, dtype=np.str_)
        numbers = np.array(numerical, dtype=np.float32)
        return {"text": text, "numbers": numbers}