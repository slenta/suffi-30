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
POWERUP_CHAOS_DURATION = 360  # Frames (4 seconds at 60 FPS)
# Flight powerup: duration (10s) and speed penalty while flying
POWERUP_FLY_DURATION = 600  # Frames (10 seconds at 60 FPS)
POWERUP_FLY_DURATION = 420  # Frames (7 seconds at 60 FPS)
POWERUP_FLY_SPEED_PENALTY = (
    3  # Reduce player.speed by this amount while flying (stronger slow)
)
# For the joint powerup we enable flight immediately; keep delay at 0 for compatibility
POWERUP_FLY_DELAY = 0  # Frames before flight ability activates (now immediate)

# Joint-specific pixelation strength (much stronger than default)
POWERUP_JOINT_PIXELATION_FACTOR = 24  # Higher = more pixelated

# Timer constants
ENCOUNTER_MESSAGE_DURATION = 180  # Frames (3 seconds at 60 FPS)

# Collision detection constants
FALL_DEATH_THRESHOLD = 3  # Grid units below nearest platform
FALL_SEARCH_RANGE = 10  # Grid units to search for nearest platform

# Bullet constants
EXPLOSION_RANGE = 3  # Grid units

# Highscore constants
SCORE_PER_SECOND_REMAINING = 100  # Points per second of remaining time
SCORE_PER_TROPHY = 10000  # Points per trophy collected
SCORE_PER_DAMAGE = 100  # Points per damage dealt to enemies
SCORE_PER_LIFE = 5000  # Points per life (gem) remaining at level end

# Pixelation effect constants (Teil powerup)
PIXELATION_DURATION = 900  # Frames (15 seconds at 60 FPS)
PIXELATION_FACTOR = (
    8  # Pixelation factor - how much to reduce resolution (higher = more pixelated)
)
