import {Pokedex} from "../../modules/pokemon-showdown/data/pokedex";
import {Items} from "../../modules/pokemon-showdown/data/items";
import {Abilities} from "../../modules/pokemon-showdown/data/abilities";
import {Moves} from "../../modules/pokemon-showdown/data/moves";

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

fs.writeFileSync('../data/raw/pokedex.json', pokedex, 'utf-8');
fs.writeFileSync('../data/raw/items.json', items, 'utf-8');
fs.writeFileSync('../data/raw/abilities.json', abilities, 'utf-8');
fs.writeFileSync('../data/raw/moves.json', moves, 'utf-8');




