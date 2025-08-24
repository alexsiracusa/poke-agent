# self-play training is a planned feature for poke-env
# This script illustrates a very rough approach that can currently be used to train using self-play
# Don't hesitate to open an issue if things seem not to be working

import asyncio
from threading import Thread

import numpy as np

from poke_env import to_id_str
from poke_env.environment.battle import Battle
from poke_env.player import Gen9EnvSinglePlayer
from poke_env.player.openai_api import ObsType

from gymnasium.spaces import Space, Box



class RandomGen9EnvPlayer(Gen9EnvSinglePlayer):
    def embed_battle(self, battle: Battle):
        return np.array([0])

    def complete_current_battle(self):
        self.current_battle = None

    def calc_reward(self, last_battle, current_battle) -> float:
        return self.reward_computing_helper(
            current_battle,
            fainted_value=0.0,
            hp_value=0.0,
            number_of_pokemons=6,
            starting_value=0.0,
            status_value=0.0,
            victory_value=1.0,
        )

    def describe_embedding(self) -> Space[ObsType]:
        """
        Returns the description of the embedding. It must return a Space specifying
        low bounds and high bounds.

        :return: The description of the embedding.
        :rtype: Space
        """
        return Box(low=-1, high=1, shape=(), dtype=np.float32)


def env_algorithm(player, n_battles):
    for _ in range(n_battles):
        done = False
        player.reset()
        while not done and not player.current_battle.finished:
            obs, reward, done, _, _ = player.step(player.action_space.sample())


async def launch_battles(player, opponent):
    battles_coroutine = asyncio.gather(
        player.send_challenges(
            opponent=to_id_str(opponent.username),
            n_challenges=1,
            to_wait=opponent.logged_in,
        ),
        opponent.accept_challenges(opponent=to_id_str(player.username), n_challenges=1),
    )
    await battles_coroutine


def env_algorithm_wrapper(player, kwargs):
    env_algorithm(player, **kwargs)

    player._start_new_battle = False
    while True:
        try:
            player.complete_current_battle()
            player.reset()
            return
        except OSError:
            break


p1 = RandomGen9EnvPlayer(log_level=25, opponent=None)
p2 = RandomGen9EnvPlayer(log_level=25, opponent=None)

p1._start_new_battle = True
p2._start_new_battle = True

loop = asyncio.get_event_loop()

env_algorithm_kwargs = {"n_battles": 5}

t1 = Thread(target=lambda: env_algorithm_wrapper(p1, env_algorithm_kwargs))
t1.start()

t2 = Thread(target=lambda: env_algorithm_wrapper(p2, env_algorithm_kwargs))
t2.start()

while p1._start_new_battle:
    print("battle started")
    loop.run_until_complete(launch_battles(p1, p2))
t1.join()
t2.join()
print('done')