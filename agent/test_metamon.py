import asyncio
from threading import Thread
from poke_env import to_id_str

import numpy as np

import json
import metamon
from metamon.env import get_metamon_teams
from metamon.env import PokeEnvWrapper, QueueOnLocalLadder
from metamon.interface import DefaultActionSpace, DefaultShapedReward, DefaultObservationSpace


class TrainEnv(QueueOnLocalLadder):
    def __init__(self, *args, **kwargs):
        super().__init__(
            battle_format="gen9ou",
            observation_space = DefaultObservationSpace(),
            action_space = DefaultActionSpace(),
            reward_function = DefaultShapedReward(),
            *args, **kwargs,
        )
        self.turn_counter = 0

    def step(self, action):
        print('step')
        _, reward, terminated, truncated, info = super().step(action)
        return self.current_battle, reward, terminated, truncated, info

team_set = get_metamon_teams("gen9ou", "modern_replays")


num_battles = 5
p1 = TrainEnv(player_team_set=team_set, player_username='p1', num_battles=num_battles)
p2 = TrainEnv(player_team_set=team_set, player_username='p2', num_battles=num_battles)


def play(player, num_battles):
    def play():
        for _ in range(num_battles):
            print('new game')
            terminated = False
            # player.current_battle = None
            obs, info = player.reset()
            # player.current_battle.finished = False
            while not terminated:
                next_obs, reward, terminated, truncated, info = player.step(player.action_space.sample())

    return play


if __name__ == "__main__":
    thread1 = Thread(target=play(p1, num_battles))
    thread2 = Thread(target=play(p2, num_battles))

    thread1.start()
    thread2.start()

    thread1.join()  # Wait for thread1 to complete
    thread2.join()  # Wait for thread2 to complete

    print("Main program: All functions completed.")




