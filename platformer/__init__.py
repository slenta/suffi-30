"""
Suffi Platformer Game Package

A pygame-based platformer with organized module structure.
"""

# Core game systems
from .core.gameworld import GameWorld
from .core.base_sprites import GridSprite
from .core.sound_manager import sound_manager

# Entities
from .entities.player import Player
from .entities.enemies import Enemy
from .entities.bullet import Bullet, ExplodingObject

# Collectibles
from .collectibles.gem import Gem
from .collectibles.powerup import PowerUp
from .collectibles.trophy import Trophy, Exit
from .collectibles.weapon import WeaponPickup

# World objects
from .world.platform_class import Platform
from .world.moving_platform import MovingPlatform
from .world.ladder import Ladder, LadderTop
from .world.pipe import Pipe
from .world.spike import Spike
from .world.waterfall import Waterfall, WaterfallTop

# UI
from .ui.level_selection import LevelSelectionScreen

# Configuration
from .config.settings import *
from .config.constants import *
from .config.enemy_config import get_enemy_config
from .config.gem_config import get_gem_config
from .config.trophy_config import get_trophy_config
from .config.weapon_config import WEAPON_CONFIG

__all__ = [
    # Core
    "GameWorld",
    "GridSprite",
    "sound_manager",
    # Entities
    "Player",
    "Enemy",
    "Bullet",
    "ExplodingObject",
    # Collectibles
    "Gem",
    "PowerUp",
    "Trophy",
    "Exit",
    "WeaponPickup",
    # World
    "Platform",
    "MovingPlatform",
    "Ladder",
    "LadderTop",
    "Pipe",
    "Spike",
    "Waterfall",
    "WaterfallTop",
    # UI
    "LevelSelectionScreen",
    # Config functions
    "get_enemy_config",
    "get_gem_config",
    "get_trophy_config",
    "WEAPON_CONFIG",
]
