import json
import collections
import torch
from data_processing.util.util import flatten_json_to_tensor


def process_move_tensors(path):
    with open(f'{path}/final/moves.json', 'r') as f:
        moves = json.load(f, object_pairs_hook=collections.OrderedDict)

    tensors = []
    lookup = {}

    for num, (key, data) in enumerate(moves.items()):
        lookup[key] = num
        del data['num']
        tensors.append(flatten_json_to_tensor(data))


    tensors = torch.stack(tensors, dim=0)

    torch.save(tensors, f'{path}/tensors/moves.pt')
    with open(f'{path}/lookup/moves.json', 'w') as f:
        json.dump(lookup, f, indent=4, sort_keys=False)

    print('processed move tensors')


if __name__ == '__main__':
    process_move_tensors('../../data')
