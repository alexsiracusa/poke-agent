from data_processing.process_tensors import process

def process_move_tensors(path, debug=False):
    process(path, 'moves', include_nothing=True, debug=debug)

if __name__ == '__main__':
    process_move_tensors('../../data', debug=True)
