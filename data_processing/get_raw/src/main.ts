import {Pokedex} from "../../../modules/pokemon-showdown/data/pokedex";
import {Items} from "../../../modules/pokemon-showdown/data/items";
import {Abilities} from "../../../modules/pokemon-showdown/data/abilities";
import {Moves} from "../../../modules/pokemon-showdown/data/moves";

import {PokedexText} from "../../../modules/pokemon-showdown/data/text/pokedex";
import {ItemsText} from "../../../modules/pokemon-showdown/data/text/items";
import {AbilitiesText} from "../../../modules/pokemon-showdown/data/text/abilities";
import {MovesText} from "../../../modules/pokemon-showdown/data/text/moves";

import * as fs from 'fs';

function safeStringify(obj: any): string {
    return JSON.stringify(obj, (_key, value) => {
        if (typeof value === 'function') {
            return value.toString();
        }
        return value;
    }, 2);
}

const pokedex = safeStringify(Pokedex);
const items = safeStringify(Items)
const abilities = safeStringify(Abilities);
const moves = safeStringify(Moves);

fs.writeFileSync('../../data/raw/pokedex.json', pokedex, 'utf-8');
fs.writeFileSync('../../data/raw/items.json', items, 'utf-8');
fs.writeFileSync('../../data/raw/abilities.json', abilities, 'utf-8');
fs.writeFileSync('../../data/raw/moves.json', moves, 'utf-8');


const pokedex_text = safeStringify(PokedexText);
const items_text = safeStringify(ItemsText)
const abilities_text = safeStringify(AbilitiesText);
const moves_text = safeStringify(MovesText);

fs.writeFileSync('../../data/raw/pokedex_text.json', pokedex_text, 'utf-8');
fs.writeFileSync('../../data/raw/items_text.json', items_text, 'utf-8');
fs.writeFileSync('../../data/raw/abilities_text.json', abilities_text, 'utf-8');
fs.writeFileSync('../../data/raw/moves_text.json', moves_text, 'utf-8');



