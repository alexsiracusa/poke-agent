from process_raw import process_raw_pokemon, process_raw_items, process_raw_abilities, process_raw_moves
from process_final import process_final_moves, process_final_pokemon
from process_tensors import process_move_tensors

data_dir = '../data'

print("\nPROCESSING RAW")
process_raw_pokemon(data_dir)
process_raw_items(data_dir)
process_raw_abilities(data_dir)
process_raw_moves(data_dir)


print("\nPROCESSING FINAL")
process_final_moves(data_dir)
process_final_pokemon(data_dir)


print("\nPROCESSING TENSORS")
process_move_tensors(data_dir)





