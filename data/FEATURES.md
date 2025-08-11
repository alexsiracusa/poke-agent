### Ability Features

```json
{
  "num": json,
  "rating": int
}
```

### Item Features

```json
{
  "num": embedding,
  "isBerry": boolean
}
```

### Move Features

```json
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
    "futuremove": boolean,
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

```javascript
type: {'Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy'}
category: {'Physical', 'Status', 'Special'}
target: {'scripted', 'allAdjacent', 'randomNormal', 'adjacentFoe', 'normal', 'self', 'allAdjacentFoes', 'adjacentAlly', 'all', 'allies', 'allyTeam', 'adjacentAllyOrSelf', 'any', 'allySide', 'foeSide'}
status: {'tox', 'slp', 'frz', 'brn', 'psn', 'par'}
volatileStatus: {'flinch', 'sparklingaria', 'saltcure', 'healblock', 'syrupbomb', 'confusion'}
```