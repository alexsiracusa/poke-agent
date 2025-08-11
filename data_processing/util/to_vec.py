from data_processing.util.util import make_one_hot_encoder


types = [
    'Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice',
    'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug',
    'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy'
]

statuses = ['tox', 'slp', 'frz', 'brn', 'psn', 'par']

volatile_statuses = ['flinch', 'sparklingaria', 'saltcure', 'healblock', 'syrupbomb', 'confusion']

move_targets = [
    'all', 'self', 'normal', 'allAdjacent', 'randomNormal',
    'scripted', 'adjacentAllyOrSelf', 'allAdjacentFoes',
    'adjacentFoe', 'allies', 'allyTeam', 'foeSide', 'any',
    'allySide', 'adjacentAlly'
]

move_categories = ['Physical', 'Status', 'Special']


type_to_vec = make_one_hot_encoder(types)
status_to_vec = make_one_hot_encoder(statuses)
volatile_status_to_vec = make_one_hot_encoder(volatile_statuses)
move_target_to_vec = make_one_hot_encoder(move_targets)
move_category_to_vec = make_one_hot_encoder(move_categories)

def nature_to_vec(nature):
    match nature:            #  ATK DEF SPA SPD SPE
        case 'Lonely':  return [1,  -1, 0,  0,  0 ]
        case 'Adamant': return [1,  0,  -1, 0,  0 ]
        case 'Naughty': return [1,  0,  0,  -1, 0 ]
        case 'Brave':   return [1,  0,  0,  0,  -1]

        case 'Bold':    return [-1, 1,  0,  0,  0 ]
        case 'Impish':  return [0,  1,  -1, 0,  0 ]
        case 'Lax':     return [0,  1,  0,  -1, 0 ]
        case 'Relaxed': return [0,  1,  0,  0,  -1]

        case 'Modest':  return [-1, 0,  1,  0,  0 ]
        case 'Mild':    return [0,  -1, 1,  0,  0 ]
        case 'Rash':    return [0,  0,  1,  -1, 0 ]
        case 'Quiet':   return [0,  0,  1,  0,  -1]

        case 'Calm':    return [-1, 0,  0,  1,  0 ]
        case 'Gentle':  return [0,  -1, 0,  1,  0 ]
        case 'Careful': return [0,  0,  -1, 1,  0 ]
        case 'Sassy':   return [0,  0,  0,  1,  -1]

        case 'Timid':   return [-1, 0,  0,  0,  1 ]
        case 'Hasty':   return [0,  -1, 0,  0,  1 ]
        case 'Jolly':   return [0,  0,  -1, 0,  1 ]
        case 'Naive':   return [0,  0,  0,  -1, 1 ]

        case 'Hardy':   return [0,  0,  0,  0,  0 ]
        case 'Docile':  return [0,  0,  0,  0,  0 ]
        case 'Serious': return [0,  0,  0,  0,  0 ]
        case 'Bashful': return [0,  0,  0,  0,  0 ]
        case 'Quirky':  return [0,  0,  0,  0,  0 ]









