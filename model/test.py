

from metamon.env import get_metamon_teams
from metamon.interface import TeamPreviewObservationSpace, DefaultShapedReward, DefaultActionSpace
from CustomObservationSpace import CustomDefaultObservationSpace

team_set = get_metamon_teams("gen9ou", "modern_replays")
obs_space = CustomDefaultObservationSpace()
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
obs, info = env.reset()
next_obs, reward, terminated, truncated, info = env.step(env.action_space.sample())

print(next_obs)


