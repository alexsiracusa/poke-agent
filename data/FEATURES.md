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
  "type": enum,
  "accuracy": int,
  "cannotMiss": boolean,
  "basePower": int,
  "category": enum,
  "pp": int,
  "priority": int,
  "target": enum,
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
    "status": enum,
    "volatileStatus": enum,
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

```
type: ['Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy']
category: ['Physical', 'Status', 'Special']
target: ['scripted', 'allAdjacent', 'randomNormal', 'adjacentFoe', 'normal', 'self', 'allAdjacentFoes', 'adjacentAlly', 'all', 'allies', 'allyTeam', 'adjacentAllyOrSelf', 'any', 'allySide', 'foeSide']
status: []'tox', 'slp', 'frz', 'brn', 'psn', 'par']
volatileStatus: ['flinch', 'sparklingaria', 'saltcure', 'healblock', 'syrupbomb', 'confusion']
```

### Pokemon Features

```
{
  "num": embedding,
  "types": {
    "primary": enum,
    "secondary": enum
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
    "tera": [enum, enum, enum, enum, enum],
    "tera_frequency": [float, float, float, float, float],
    "spreads": [
      {
        "nature": enum,
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