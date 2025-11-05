"""Configuration files - game settings, constants, and entity configurations."""

from .settings import *
from .constants import *
from .enemy_config import get_enemy_config
from .gem_config import get_gem_config
from .trophy_config import get_trophy_config
from .weapon_config import WEAPON_CONFIG

__all__ = [
    "get_enemy_config",
    "get_gem_config",
    "get_trophy_config",
    "WEAPON_CONFIG",
]
