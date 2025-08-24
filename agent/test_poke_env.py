import asyncio

from poke_env import RandomPlayer
from poke_env.player import Player
from poke_env.environment.battle import Battle
from poke_env.player.battle_order import BattleOrder

from agent.model.timestep_encoder import TimestepEncoder

from teams import team_1, team_2

encoder = TimestepEncoder('../data')

class MaxDamagePlayer(Player):
    def choose_move(self, battle: Battle):
        features = encoder(battle)
        print(features.shape)

        if battle.available_moves:
            best_move = max(battle.available_moves, key=lambda move: move.base_power)

            if battle.can_tera:
                return self.create_order(best_move, terastallize=True)

            return self.create_order(best_move, terastallize=battle.can_tera is not None)
        else:
            return self.choose_random_move(battle)


player = MaxDamagePlayer(battle_format="gen9ou", team=team_1)
random_player = RandomPlayer(battle_format="gen9ou", team=team_2)

n_battles = 1
asyncio.run(player.battle_against(random_player, n_battles=n_battles))

print(f"Max damage player won {player.n_won_battles} / {n_battles} battles")

