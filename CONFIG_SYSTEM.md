# Centralized Configuration System

## Overview

The game now uses centralized configuration files for enemies, weapons, trophies, and gems. This makes it easier to:
- Define enemy types once and reuse them across levels
- Tune game balance by modifying config files
- Add new enemy/weapon/item types without touching level files
- Keep level files clean and focused on layout

## Configuration Files

### 1. `enemy_config.py`
Defines all enemy types with their default properties.

**Available Enemy Types:**
- `baby_erzieherin` - Baby level boss
- `teddybear` - Baby level mini-boss
- `trance_totem` - Trancefloor enemy
- `trance_jesus` - Trancefloor enemy
- `trance_hippie` - Trancefloor enemy
- `trance_okf` - Trancefloor boss
- `dj_booth` - Trancefloor final boss
- `basic_enemy` - Generic enemy template

### 2. `weapon_config.py` (formerly `weapon_stats.py`)
Defines all weapon types and their properties.

**Available Weapon Types:**
- `milchflasche` - Melee weapon (baby bottle)
- `schwert` - Melee weapon (sword)
- `wasserpistole` - Shooting weapon (water pistol)
- `gun` - Shooting weapon

### 3. `gem_config.py`
Defines gem types and their properties.

**Available Gem Types:**
- `standard` - Regular gem (1 point)
- `heart` - Extra life
- `gold` - Gold gem (3 points)

### 4. `trophy_config.py`
Defines trophy types and their properties.

**Available Trophy Types:**
- `standard` - Standard trophy
- `baby` - Baby-themed trophy
- `trance` - Trance-themed trophy
- `golden` - Golden trophy

## Usage in Level Files

### Old Format (Still Supported)
```python
"enemy_locations": [
    {
        "x": 130,
        "y": -24,
        "image": "enemies/trance-totem.png",
        "speed": 2,
        "patrol_range": 100,
        "size_multiplier": 4,
        "health": 15,
        "damage": 5,
        "shoot_range": 5,
        "chase_range": 10,
        "melee_damage": 2,
        "can_throw_explosives": False,
        "encounter_message": "Watch out for the Totem!",
    },
]
```

### New Format (Recommended)
```python
"enemy_locations": [
    # Simple usage - use all defaults from config
    {"type": "trance_totem", "x": 130, "y": -24},
    
    # With overrides - customize specific properties
    {"type": "trance_totem", "x": 200, "y": -24, "health": 30, "speed": 3},
]
```

### Gem Usage
```python
"gem_locations": [
    # Old format (tuple) - still works
    (17, 8),
    (60, 12),
    
    # New format with type
    {"type": "standard", "x": 100, "y": 10},
    {"type": "gold", "x": 150, "y": 10},
]
```

### Trophy Usage
```python
"trophy_locations": [
    # Old format (tuple) - still works
    (40, 13),
    
    # New format with type
    {"type": "standard", "x": 90, "y": 13},
    {"type": "golden", "x": 135, "y": 13},
]
```

## Benefits

### 1. Cleaner Level Files
Before:
```python
"enemy_locations": [
    {
        "x": 130, "y": -24, "image": "enemies/trance-totem.png",
        "speed": 2, "patrol_range": 100, "size_multiplier": 4,
        "health": 15, "damage": 5, "shoot_range": 5,
        "chase_range": 10, "melee_damage": 2,
        "can_throw_explosives": False,
        "encounter_message": "Watch out for the Totem!",
    },
]
```

After:
```python
"enemy_locations": [
    {"type": "trance_totem", "x": 130, "y": -24},
]
```

### 2. Easy Game Balance
Want to make all totems stronger? Just edit `enemy_config.py`:
```python
"trance_totem": {
    "health": 20,  # Changed from 15
    ...
}
```

### 3. Consistent Enemy Behavior
All instances of the same enemy type behave identically unless explicitly overridden.

### 4. Backward Compatible
Old level files still work without modification. You can migrate gradually.

## Adding New Enemy Types

1. Add to `enemy_config.py`:
```python
ENEMY_TYPES = {
    "new_enemy": {
        "name": "New Enemy",
        "image": "enemies/new-enemy.png",
        "speed": 2,
        "patrol_range": 50,
        "size_multiplier": 3,
        "health": 20,
        "damage": 5,
        "shoot_range": 10,
        "chase_range": 15,
        "melee_damage": 5,
        "can_throw_explosives": True,
        "can_summon_minions": False,
        "encounter_message": "A new challenger appears!",
        "shoot_cooldown": 60,
    },
}
```

2. Use in level files:
```python
"enemy_locations": [
    {"type": "new_enemy", "x": 100, "y": 50},
]
```

## Migration Guide

### Step 1: Identify Duplicate Enemies
Look for enemies with identical or very similar stats across levels.

### Step 2: Add to Config
Add the enemy template to `enemy_config.py`.

### Step 3: Update Level Files
Replace detailed configs with template references:
```python
# Before
{"x": 100, "y": 50, "image": "...", "speed": 2, ...}

# After
{"type": "enemy_name", "x": 100, "y": 50}
```

### Step 4: Test
Run the level and verify the enemy behaves correctly.

## Advanced Usage

### Overriding Multiple Properties
```python
{
    "type": "trance_totem",
    "x": 130,
    "y": -24,
    "health": 30,  # Override
    "speed": 3,    # Override
    "encounter_message": "Custom message!",  # Override
}
```

### Keeping Custom Enemies
For truly unique enemies (like the "yourself" enemy in trancefloor), keep using the old format:
```python
{
    "x": 480,
    "y": -22,
    "image": "player/suffi.png",
    "speed": 3,
    # ... custom stats ...
}
```

## Best Practices

1. **Use templates for recurring enemies** - If an enemy appears more than once, add it to `enemy_config.py`
2. **Override sparingly** - Only override when you need a specific variation
3. **Document custom enemies** - Add comments explaining why a custom config is needed
4. **Keep configs DRY** - Don't duplicate enemy definitions across levels
5. **Test after changes** - Always test levels after modifying config files
