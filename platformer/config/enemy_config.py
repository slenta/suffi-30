"""
Centralized enemy configurations.
Define enemy templates that can be referenced in level files.
"""

# Enemy type definitions - use these as templates in level configs
ENEMY_TYPES = {
    # Baby level enemies
    "baby_erzieherin": {
        "name": "Baby Erzieherin (Boss)",
        "image": "enemies/baby-erzieherin.png",
        "speed": 1,
        "patrol_range": 150,
        "size_multiplier": 4,
        "health": 50,
        "damage": 5,
        "shoot_range": 0,
        "chase_range": 10,
        "melee_damage": 10,
        "can_throw_explosives": False,
        "can_summon_minions": False,
        "encounter_message": None,
        "shoot_cooldown": 60,
        "spawn_on_death": None,
    },
    "teddybear": {
        "name": "Teddybear",
        "image": "enemies/teddybear.png",
        "speed": 1,
        "patrol_range": 50,
        "size_multiplier": 3,
        "health": 30,
        "damage": 5,
        "shoot_range": 0,
        "chase_range": 10,
        "melee_damage": 10,
        "can_throw_explosives": False,
        "can_summon_minions": False,
        "encounter_message": None,
        "shoot_cooldown": 60,
    },
    # Trancefloor enemies
    "trance_totem": {
        "name": "Trance Totem",
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
        "can_summon_minions": False,
        "encounter_message": "Watch out for the Totem!",
        "shoot_cooldown": 60,
    },
    "trance_jesus": {
        "name": "Trance Jesus",
        "image": "enemies/trance-jesus.png",
        "speed": 3,
        "patrol_range": 100,
        "size_multiplier": 4,
        "health": 20,
        "damage": 5,
        "shoot_range": 30,
        "chase_range": 20,
        "melee_damage": 4,
        "can_throw_explosives": False,
        "can_summon_minions": False,
        "encounter_message": "Trance Jesus has entered the chat!",
        "shoot_cooldown": 60,
    },
    "trance_hippie": {
        "name": "Trance Hippie",
        "image": "enemies/trance-hippie.png",
        "speed": 1,
        "patrol_range": 30,
        "size_multiplier": 4,
        "health": 20,
        "damage": 2,
        "shoot_range": 30,
        "chase_range": 5,
        "melee_damage": 2,
        "can_throw_explosives": False,
        "can_summon_minions": False,
        "encounter_message": "Peace, Love & Bullets!",
        "shoot_cooldown": 60,
    },
    "trance_okf": {
        "name": "OKF Guardian (Boss)",
        "image": "enemies/trance-okf.png",
        "speed": 2,
        "patrol_range": 300,
        "size_multiplier": 4,
        "health": 40,
        "damage": 5,
        "shoot_range": 0,
        "chase_range": 100,
        "melee_damage": 15,
        "can_throw_explosives": False,
        "can_summon_minions": False,
        "encounter_message": "BOSS FIGHT: The OKF Guardian!",
        "shoot_cooldown": 60,
    },
    "dj_booth": {
        "name": "DJ Booth (Final Boss)",
        "image": "enemies/trancefloor/dj-booth.png",
        "speed": 0,
        "patrol_range": 0,
        "size_multiplier": 8,
        "health": 40,
        "damage": 1,
        "shoot_range": 100,
        "chase_range": 0,
        "melee_damage": 50,
        "can_throw_explosives": False,
        "can_summon_minions": True,
        "encounter_message": "FINAL BOSS: The DJ Booth!",
        "shoot_cooldown": 30,
    },
    # Graffiti level enemies
    "trump": {
        "name": "Trump",
        "image": "trump.png",
        "speed": 1,
        "patrol_range": 50,
        "size_multiplier": 1,
        "health": 2,
        "damage": 1,
        "shoot_range": 0,
        "chase_range": 10,
        "melee_damage": 1,
        "can_throw_explosives": False,
        "can_summon_minions": False,
        "encounter_message": None,
        "shoot_cooldown": 60,
    },
    # Generic enemies for other levels
    "basic_enemy": {
        "name": "Basic Enemy",
        "image": "enemies/basic.png",
        "speed": 1,
        "patrol_range": 50,
        "size_multiplier": 2,
        "health": 10,
        "damage": 5,
        "shoot_range": 5,
        "chase_range": 10,
        "melee_damage": 5,
        "can_throw_explosives": True,
        "can_summon_minions": False,
        "encounter_message": None,
        "shoot_cooldown": 60,
    },
    "druide": {
        "name": "Druide",
        "image": "enemies/trancefloor/plh.png",
        "speed": 1,
        "patrol_range": 50,
        "size_multiplier": 4,
        "health": 50,
        "damage": 5,
        "shoot_range": 5,
        "chase_range": 50,
        "melee_damage": 20,
        "can_throw_explosives": False,
        "can_summon_minions": False,
        "encounter_message": "Look at this crazy costume!",
        "shoot_cooldown": 60,
        "spawn_on_death": {
            "type": "presslufthanna",
        },
    },
    "presslufthanna": {
        "name": "Presslufthanna",
        "image": "enemies/trancefloor/plh.png",
        "speed": 1,
        "patrol_range": 50,
        "size_multiplier": 4,
        "health": 10,
        "damage": 5,
        "shoot_range": 5,
        "chase_range": 50,
        "melee_damage": 20,
        "can_throw_explosives": False,
        "can_summon_minions": False,
        "encounter_message": "PLH gibt dir aufs Maul!",
        "shoot_cooldown": 60,
    },
}


def get_enemy_config(enemy_type, **overrides):
    """
    Get enemy configuration with optional overrides.

    Args:
        enemy_type: Type of enemy from ENEMY_TYPES
        **overrides: Any parameters to override (e.g., x, y, health, speed)

    Returns:
        Dictionary with complete enemy configuration

    Example:
        get_enemy_config('trance_totem', x=100, y=50, health=30)
    """
    if enemy_type not in ENEMY_TYPES:
        raise ValueError(
            f"Unknown enemy type: {enemy_type}. Available types: {list(ENEMY_TYPES.keys())}"
        )

    # Start with the template
    config = ENEMY_TYPES[enemy_type].copy()

    # Apply overrides
    config.update(overrides)

    return config
