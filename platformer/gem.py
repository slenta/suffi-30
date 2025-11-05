"""Gem collectible sprite."""
from .base_sprites import CollectibleSprite


class Gem(CollectibleSprite):
    """Collectible gem that increases player's gem count."""

    def __init__(self, x, y, image):
        """
        Initialize a gem.

        Args:
            x: X position in grid units
            y: Y position in grid units
            image: Gem image surface
        """
        super().__init__(x, y, image, convert_to_grid=True)

    def apply(self, character):
        """Add a gem to the character's inventory."""
        character.gems += 1
