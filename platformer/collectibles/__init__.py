"""Collectible items - gems, power-ups, trophies, and weapons."""

from .gem import Gem
from .powerup import PowerUp
from .trophy import Trophy, Exit
from .weapon import WeaponPickup

__all__ = ["Gem", "PowerUp", "Trophy", "Exit", "WeaponPickup"]
