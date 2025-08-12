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
    Supports numbers, booleans, lists of numbers, lists of lists,
    and lists of JSON objects.

    Parameters:
        data (dict): The nested JSON-like dictionary.
        key_order (list, optional): Predefined list of key paths for consistent ordering.
                                    Each key path is a tuple of keys.

    Returns:
        tensor: 1D torch tensor of all flattened values.
        key_order: List of key paths used, so you can reuse it for consistent ordering.
    """

    def flatten_value(v):
        """Recursively flatten a value that may be number, bool, list, or dict."""
        if isinstance(v, bool) or isinstance(v, (int, float)):
            return [float(v)]
        elif isinstance(v, dict):
            # dict should be processed in key order
            values = []
            for _, subval in sorted(v.items()):
                values.extend(flatten_value(subval))
            return values
        elif isinstance(v, list):
            values = []
            for item in v:
                values.extend(flatten_value(item))
            return values
        else:
            raise ValueError(f"Unsupported leaf type: {type(v)}")

    def collect_items(d, path=()):
        items = []
        for k, v in sorted(d.items()):
            new_path = path + (k,)
            if isinstance(v, dict):
                items.extend(collect_items(v, new_path))
            else:
                # Store flattened value but keep path
                items.append((new_path, flatten_value(v)))
        return items

    # Step 1: Determine key order if not given
    if key_order is None:
        collected = collect_items(data)
        key_order = [k for k, _ in collected]
    else:
        collected = collect_items(data)
        collected_dict = dict(collected)
        for k in key_order:
            if k not in collected_dict:
                raise ValueError(f"Missing key path {k} in input JSON")

    # Step 2: Flatten values in consistent order
    flat_values = []
    collected_dict = dict(collected)
    for k in key_order:
        flat_values.extend(collected_dict[k])

    return torch.tensor(flat_values, dtype=torch.float32)


def pad(array, length, value=0):
    return array + [value] * (length - len(array))
