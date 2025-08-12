from data_processing.process_tensors import process

def process_pokemon_tensors(path, debug=False):
    process(path, 'pokemon', include_nothing=True, debug=debug)

if __name__ == '__main__':
    process_pokemon_tensors('../../data', debug=True)
