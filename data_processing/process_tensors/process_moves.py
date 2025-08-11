import json
import collections
import torch
from data_processing.util import flatten_json_to_tensor

with open('../../data/final/moves.json', 'r') as f:
    moves = json.load(f, object_pairs_hook=collections.OrderedDict)

tensors = []
lookup = {}

for num, (key, data) in enumerate(moves.items()):
    lookup[key] = num
    del data['num']
    tensors.append(flatten_json_to_tensor(data))


tensors = torch.stack(tensors, dim=0)
print(tensors.shape)

torch.save(tensors, '../../data/tensors/moves.pt')
with open('../../data/lookup/moves.json', 'w') as f:
    json.dump(lookup, f, indent=4, sort_keys=False)
