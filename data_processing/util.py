import numpy as np
import torch


def get_nested(d, keys, default=None):
    """
    Safely get a nested value from a dictionary.

    Args:
        d (dict): The dictionary to search.
        keys (list | tuple): Sequence of keys representing the nested path.
        default: Value to return if the path doesn't exist.

    Returns:
        The nested value, or default if any key is missing.
    """
    current = d
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


def make_one_hot_encoder(strings):
    # Map each string to an index
    str_to_idx = {s: i for i, s in enumerate(strings)}
    size = len(strings)

    def encoder(s, default=False):
        one_hot = np.zeros(size)
        idx = str_to_idx.get(s)
        if idx is None and default:
            return list(one_hot)
        elif idx is None:
            raise ValueError(f"{s} not found in list")
        one_hot[idx] = 1
        return list(one_hot)

    return encoder



def flatten_json_to_tensor(data, key_order=None):
    """
    Flattens a nested JSON into a 1D torch tensor.

    Parameters:
        data (dict): The nested JSON-like dictionary.
        key_order (list, optional): Predefined list of key paths for consistent ordering.
                                    Each key path is a tuple of keys.

    Returns:
        tensor: 1D torch tensor of all flattened values.
        key_order: List of key paths used, so you can reuse it for consistent ordering.
    """

    def collect_items(d, path=()):
        items = []

        for k, v in sorted(d.items()):
            new_path = path + (k,)
            if isinstance(v, dict):
                items.extend(collect_items(v, new_path))
            elif isinstance(v, bool) or isinstance(v, (int, float)):
                items.append((new_path, [float(v)]))
            elif isinstance(v, list):
                items.append((new_path, list(map(float, v))))
            else:
                raise ValueError(f"Unsupported leaf type at {new_path}: {type(v)}")

        return items

    # Step 1: If no key_order, extract and sort keys from this JSON
    if key_order is None:
        collected = collect_items(data)
        key_order = [k for k, _ in collected]
    else:
        collected = collect_items(data)
        collected_dict = dict(collected)
        # Ensure all keys exist
        for k in key_order:
            if k not in collected_dict:
                raise ValueError(f"Missing key path {k} in input JSON")

    # Step 2: Flatten in consistent order
    flat_values = []
    collected_dict = dict(collected)
    for k in key_order:
        flat_values.extend(collected_dict[k])

    return torch.tensor(flat_values, dtype=torch.float32)

