import numpy as np


types = [
    'Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice',
    'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug',
    'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy'
]

statuses = ['tox', 'slp', 'frz', 'brn', 'psn', 'par']

volatile_statuses = ['flinch', 'sparklingaria', 'saltcure', 'healblock', 'syrupbomb', 'confusion']

move_types = [
    'all', 'self', 'normal', 'allAdjacent', 'randomNormal',
    'scripted', 'adjacentAllyOrSelf', 'allAdjacentFoes',
    'adjacentFoe', 'allies', 'allyTeam', 'foeSide', 'any',
    'allySide', 'adjacentAlly'
]

move_categories = ['Physical', 'Status', 'Special']


def make_one_hot_encoder(strings):
    # Map each string to an index
    str_to_idx = {s: i for i, s in enumerate(strings)}
    size = len(strings)

    def encoder(s):
        one_hot = np.zeros(size, dtype=int)
        idx = str_to_idx.get(s)
        if idx is None:
            raise ValueError(f"{s} not found in list")
        one_hot[idx] = 1
        return one_hot

    return encoder


type_to_vec = make_one_hot_encoder(types)
status_to_vec = make_one_hot_encoder(statuses)
volatile_status_to_vec = make_one_hot_encoder(volatile_statuses)
move_type_to_vec = make_one_hot_encoder(move_types)
move_category_to_vec = make_one_hot_encoder(move_categories)








