import json

from metamon.env import get_metamon_teams
from metamon.interface import TeamPreviewObservationSpace, DefaultShapedReward, DefaultActionSpace, DefaultObservationSpace

team_set = get_metamon_teams("gen9ou", "modern_replays")
obs_space = DefaultObservationSpace()
reward_fn = DefaultShapedReward()
action_space = DefaultActionSpace()

from metamon.env import BattleAgainstBaseline
from metamon.baselines import get_baseline

env = BattleAgainstBaseline(
    battle_format="gen9ou",
    observation_space=obs_space,
    action_space=action_space,
    reward_function=reward_fn,
    team_set=team_set,
    opponent_type=get_baseline("Gen1BossAI"),
)

# standard `gymnasium` environment
for _ in range(3):
    print('new battle')
    obs, info = env.reset()
    terminated = False
    while not terminated:
        next_obs, reward, terminated, truncated, info = env.step(env.action_space.sample())