"""
Game constants for platformer game.
Contains magic numbers and gameplay parameters extracted from various modules.
"""

# Player constants
PLAYER_KNOCKBACK_DISTANCE = 6  # Grid units
PLAYER_KNOCKBACK_TIMER = 30  # Frames (~0.5 seconds at 60 FPS)
PLAYER_KNOCKBACK_STEPS = 30  # Animation steps
PLAYER_KNOCKBACK_LIFT = 2  # Pixels to lift during knockback

SPIKE_KNOCKBACK_DISTANCE = 2.5  # Grid units
SPIKE_DAMAGE_COOLDOWN = 30  # Frames (~0.5 seconds at 60 FPS)

EXPLODING_OBJECT_COOLDOWN = 180  # Frames (3 seconds at 60 FPS)
EXPLODING_OBJECT_DAMAGE = 1
EXPLODING_OBJECT_SPEED = 3
EXPLODING_OBJECT_INITIAL_VY = -3
EXPLODING_OBJECT_GRAVITY_FACTOR = 0.2

# Ladder constants
LADDER_MOVE_SPEED = 2
WATERFALL_MOVE_SPEED = 2

# Weapon constants
MELEE_ATTACK_DURATION = 15  # Frames
WEAPON_SCALE_FACTOR = 0.5  # Weapon size relative to player

# Enemy constants
ENEMY_MINION_SUMMON_CHANCE = 0.001  # 0.1% per frame
ENEMY_EXPLOSIVE_THROW_CHANCE = 0.01  # 1% per frame
ENEMY_DEATH_TIMER_MAX = 300  # 5 seconds at 60 FPS
ENEMY_DEATH_INITIAL_VY = -12
ENEMY_DEATH_ROTATION_SPEED_MIN = 12
ENEMY_DEATH_ROTATION_SPEED_MAX = 18
ENEMY_MINION_SIZE = 0.5
ENEMY_MINION_HEALTH = 3
ENEMY_MINION_DAMAGE = 1
ENEMY_MINION_MELEE_DAMAGE = 2
ENEMY_MINION_PATROL_RANGE = 50
ENEMY_MINION_SHOOT_RANGE = 3
ENEMY_MINION_CHASE_RANGE = 5

# Power-up constants
POWERUP_SPEED_INCREASE = 4
POWERUP_CHAOS_SPEED_INCREASE = 6
POWERUP_CHAOS_FPS = 10
POWERUP_SIZE_MULTIPLIER = 2
POWERUP_DEFAULT_DURATION = 480  # Frames (8 seconds at 60 FPS)
POWERUP_CHAOS_DURATION = 240  # Frames (4 seconds at 60 FPS)

# Timer constants
ENCOUNTER_MESSAGE_DURATION = 180  # Frames (3 seconds at 60 FPS)

# Collision detection constants
FALL_DEATH_THRESHOLD = 3  # Grid units below nearest platform
FALL_SEARCH_RANGE = 10  # Grid units to search for nearest platform

# Bullet constants
EXPLOSION_RANGE = 3  # Grid units
