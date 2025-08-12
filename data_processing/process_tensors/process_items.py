from data_processing.process_tensors import process

def process_item_tensors(path, debug=False):
    process(path, 'items', include_nothing=True, debug=debug)

if __name__ == '__main__':
    process_item_tensors('../../data', debug=True)
