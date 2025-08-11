import numpy as np

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

