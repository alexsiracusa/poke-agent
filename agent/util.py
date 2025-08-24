
def pad(array, length, value=0):
    return array + [value] * (length - len(array))

def flatten_list(lst):
    flat = []
    for x in lst:
        if isinstance(x, list):  # if it's a list, extend
            flat.extend(x)
        else:
            flat.append(x)
    return flat