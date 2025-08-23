from data_processing.process_tensors import process

def process_ability_tensors(path, debug=False):
    process(path, 'abilities', include_nothing=True, debug=debug)

if __name__ == '__main__':
    process_ability_tensors('../../data', debug=True)
