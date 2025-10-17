WEAPON_CONFIG = {
    # Melee weapons
    "milchflasche": {
        "type": "melee",
        "damage": 5,
        "range": 1.5,  # Grid units
        "cooldown": 0,  # Frames between attacks
        "image": "weapons/milchflasche.jpeg",
    },
    "schwert": {
        "type": "melee",
        "damage": 15,
        "range": 2,
        "cooldown": 20,
        "image": "weapons/schwert.png",
    },
    # Shooting weapons
    "wasserpistole": {
        "type": "shooting",
        "damage": 3,
        "bullet_speed": 4,
        "fire_rate": 0,  # Frames between shots
        "bullet_image": "water_bullet.png",
        "bullet_size": (10, 8),
        "bullet_color": (255, 255, 0),
        "image": "weapons/wasserpistole.jpeg",
    },
    "gun": {
        "type": "shooting",
        "damage": 10,
        "bullet_speed": 6,
        "fire_rate": 15,
        "bullet_image": "bullet.png",
        "bullet_size": (10, 5),
        "bullet_color": (255, 255, 0),
        "image": "weapons/gun.png",
    },
}
