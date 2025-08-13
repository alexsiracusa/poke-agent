## Overview
This folder contains the following folders:

| Folder      | Description                                                                                                                                |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| `raw`       | Contains the raw data gathered from various sources documented in the section below                                                        |
| `processed` | Gathers all the raw data together into comprehensive jsons which contain all relevant data for `pokemon`, `items`, `moves` and `abilities` |
| `final`     | Translates the data from `processed` into purely numerical values that can be easily translated into a single tensor per entry             |
| `tensors`   | The final tensor feature set for all `pokemon`/`items`/`moves`/`abilities` such that the `i'th` row corresponds to the `i'th` pokemon      |
| `lookup`    | Lookup tables by name with IDs for all `pokemon`/`items`/`moves`/`abilities` to find the corresponding tensor from the `tensors` folder    |



## Raw Data
> **_NOTE:_**  It might be better to scrape data using showdowns API [here](https://github.com/smogon/pokemon-showdown/blob/master/sim/DEX.md)

| File                  | Description                                                   | Source                                                                                                                                    |
|-----------------------|---------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| `pokedex.json`        | All Pokemon along with their base stats and other information | converted to json from `data/pokedex.ts` in the [`pokemon-showdown`](https://github.com/smogon/pokemon-showdown) GitHub repository        |
| `pokedex_text.json`   | All Pokemon and their names                                   | converted to json from `data/text/pokedex.ts` in the [`pokemon-showdown`](https://github.com/smogon/pokemon-showdown) GitHub repository   |
| `items.json`          | All items and related information                             | converted to json from `data/items.ts` in the [`pokemon-showdown`](https://github.com/smogon/pokemon-showdown) GitHub repository          |
| `items_text.json`     | All items and their text descriptions                         | converted to json from `data/text/items.ts` in the [`pokemon-showdown`](https://github.com/smogon/pokemon-showdown) GitHub repository     |
| `abilities.json`      | All abilities and related information                         | converted to json from `data/abilities.ts` in the [`pokemon-showdown`](https://github.com/smogon/pokemon-showdown) GitHub repository      |
| `abilities_text.json` | All abilities and their text descriptions                     | converted to json from `data/text/abilities.ts` in the [`pokemon-showdown`](https://github.com/smogon/pokemon-showdown) GitHub repository |
| `moves.json`          | All moves and related information                             | converted to json from `data/moves.ts` in the [`pokemon-showdown`](https://github.com/smogon/pokemon-showdown) GitHub repository          |
| `moves_text.json`     | All moves and their text descriptions                         | converted to json from `data/text/moves.ts` in the [`pokemon-showdown`](https://github.com/smogon/pokemon-showdown) GitHub repository     |
| `gen9ou0.txt`         | Usage stats for each pokemon in gen9ou throughout May 2025    | downloaded from https://www.smogon.com/stats/2025-05/moveset/                                                                             |
| `gen9ou.json`         | Usage stats for each pokemon in gen9ou                        | downloaded from an unofficial smogon data scraper found [here](https://github.com/pkmn/smogon) at `data/stats/gen9ou.json`                |


# Final Features
### Enums
```
TYPE: ['Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy']
NATURE: ['Lonely','Adamant','Naughty','Brave','Bold','Impish','Lax','Relaxed','Modest','Mild','Rash','Quiet','Calm','Gentle','Careful','Sassy','Timid','Hasty','Jolly','Naive','Hardy','Docile','Serious','Bashful','Quirky']
MOVE_CATEGORY: ['Physical', 'Status', 'Special']
MOVE_TARGET: ['scripted', 'allAdjacent', 'randomNormal', 'adjacentFoe', 'normal', 'self', 'allAdjacentFoes', 'adjacentAlly', 'all', 'allies', 'allyTeam', 'adjacentAllyOrSelf', 'any', 'allySide', 'foeSide']
STATUS: ['tox', 'slp', 'frz', 'brn', 'psn', 'par']
VOLATILE_STATUS: ['flinch', 'sparklingaria', 'saltcure', 'healblock', 'syrupbomb', 'confusion']
```

### Ability Features

```
{
  "num": embedding,
  "rating": int
}
```

### Item Features

```
{
  "num": embedding,
  "isBerry": boolean
}
```

### Move Features
```
{
  "num": embedding,
  "type": TYPE,
  "accuracy": int,
  "cannotMiss": boolean,
  "basePower": int,
  "category": MOVE_CATEGORY,
  "pp": int,
  "priority": int,
  "target": MOVE_TARGET,
  "critRatio": int,
  "multihit": int,
  "boosts": {
    "atk": int,
    "def": int,
    "spa": int,
    "spd": int,
    "spe": int
  },
  "flags": {
    "heal": boolean,
    "dance": boolean,
    "wind": boolean,
    "distance": boolean,
    "protect": boolean,
    "failmefirst": boolean,
    "mirror": boolean,
    "reflectable": boolean,
    "contact": boolean,
    "powder": boolean,
    "pledgecombo": boolean,
    "charge": boolean,
    "failcopycat": boolean,
    "recharge": boolean,
    "snatch": boolean,
    "sound": boolean,
    "pulse": boolean,
    "metronome": boolean,
    "defrost": boolean,
    "bite": boolean,
    "allyanim": boolean,
    "punch": boolean,
    "noassist": boolean,
    "nonsky": boolean,
    "bullet": boolean,
    "slicing": boolean,
    "nosleeptalk": boolean,
    "failinstruct": boolean,
    "cantusetwice": boolean,
    "failencore": boolean,
    "failmimic": boolean,
    "gravity": boolean,
    "nosketch": boolean,
    "mustpressure": boolean,
    "bypasssub": boolean,
    "futuremove": boolean
  },
  "secondary": {
    "chance": int,
    "status": STATUS,
    "volatileStatus": VOLATILE_STATUS,
    "self": {
      "boosts": {
        "atk": int,
        "def": int,
        "spa": int,
        "spd": int,
        "spe": int
      }
    }
  }
}
```

### Pokemon Features

```
{
  "num": embedding,
  "types": {
    "primary": TYPE,
    "secondary": TYPE
  },
  "baseStats": {
    "hp": int / 100,
    "atk": int / 100,
    "def": int / 100,
    "spa": int / 100,
    "spd": int / 100,
    "spe": int / 100
  },
  "heightm": float / 5,
  "weightkg": float / 100,
  "stats": {
    "lead": {
      "raw": float,
      "real": float,
      "weighted": float
    },
    "usage": {
      "raw": float,
      "real": float,
      "weighted": float
    },
    "count": int,
    "weight": float,
    "viability": [int, int, int, int],
    "abilities_frequency": [float, float, float],
    "items_frequency": [float, float, float, float, float],
    "tera": [TYPE, TYPE, TYPE, TYPE, TYPE],
    "tera_frequency": [float, float, float, float, float],
    "spreads": [
      {
        "nature": NATURE,
        "hp": int / 252,
        "atk": int / 252,
        "def": int / 252,
        "spa": int / 252,
        "spd": int / 252,
        "spe": int / 252,
        "frequency": float
      } x 5
    ],
    "move_frequencies": [
      float, float, float, float, float,
      float, float, float, float, float,
      float, float, float, float, float,
    ]
  }
}

```

#### Pokemon Embedding Features
```
{
  "abilities": [embedding, embedding, embedding],
  "items": [embedding, embedding, embedding, embedding, embedding],
  "moves": [
    embedding, embedding, embedding, embedding, embedding,
    embedding, embedding, embedding, embedding, embedding,
    embedding, embedding, embedding, embedding, embedding
  ],
}
```


