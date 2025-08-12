from process_raw import process_raw_pokemon, process_raw_items, process_raw_abilities, process_raw_moves
from process_final import process_final_moves, process_final_pokemon, process_final_items, process_final_abilities
from process_tensors import process_move_tensors, process_pokemon_tensors, process_ability_tensors, process_item_tensors


data_dir = '../data'

print("\nPROCESSING ITEMS")
process_raw_items(data_dir)
process_final_items(data_dir)
process_item_tensors(data_dir)

print("\nPROCESSING ABILITIES")
process_raw_abilities(data_dir)
process_final_abilities(data_dir)
process_ability_tensors(data_dir)

print("\nPROCESSING MOVES")
process_raw_moves(data_dir)
process_final_moves(data_dir)
process_move_tensors(data_dir)

print("\nPROCESSING POKEMON")
process_raw_pokemon(data_dir)
process_final_pokemon(data_dir)
process_pokemon_tensors(data_dir)


