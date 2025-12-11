WEAPON_CONFIG = {
    # Melee weapons
    "milchflasche": {
        "type": "melee",
        "damage": 5,
        "range": 4.5,  # Grid units
        "cooldown": 0,  # Frames between attacks
        "image": "weapons/milchflasche.png",
        "size": 2,
    },
    "schwert": {
        "type": "melee",
        "damage": 15,
        "range": 2,
        "cooldown": 20,
        "image": "weapons/schwert.png",
        "size": 2,
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
        "image": "weapons/wasserpistole.png",
        "size": 2,
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
        "size": 2,
    },
    "spraydose": {
        "type": "spray",
        "damage": 1,
        "bullet_speed": 6,
        "fire_rate": 2,  # frames between emitted droplets
        "bullet_image": "",  # use generated color if not provided
        "bullet_size": (6, 6),
        "bullet_color": (200, 100, 255),
        "image": "spraydose.png",
        "size": 2,
        "gravity": True,
    },
}
