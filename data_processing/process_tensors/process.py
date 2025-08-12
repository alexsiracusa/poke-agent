import json
import collections
import torch
from data_processing.util.util import flatten_json_to_tensor


def process(path, name, include_nothing=False, debug=False):
    with open(f'{path}/final/{name}.json', 'r') as f:
        jsons = json.load(f, object_pairs_hook=collections.OrderedDict)

    tensors = []
    lookup = {}

    if include_nothing:
        lookup['nothing'] = 0

    for num, (key, data) in enumerate(jsons.items()):
        lookup[key] = num + int(include_nothing)
        if 'num' in data:
            del data['num']
        tensors.append(flatten_json_to_tensor(data))

    tensors = torch.stack(tensors, dim=0)

    if include_nothing:
        zero_row = torch.zeros(1, tensors.size(1))
        tensors = torch.cat((zero_row, tensors), dim=0)

    torch.save(tensors, f'{path}/tensors/{name}.pt')
    with open(f'{path}/lookup/{name}.json', 'w') as f:
        json.dump(lookup, f, indent=4, sort_keys=False)

    if debug:
        print(tensors.shape)

    print(f'processed {name} tensors')

