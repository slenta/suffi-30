"""Poppable block that can be hit from below by the player."""

import pygame as pg
import os
from ..core.base_sprites import GridSprite
from ..config.settings import GRIDSIZE, IMAGEPATH


class PoppableBlock(GridSprite):
    """Block that can be popped/broken when hit from below by the player."""

    def __init__(self, x, y, image, block_type="disappear", item_data=None, world=None):
        """
        Initialize a poppable block.

        Args:
            x: X position in grid units
            y: Y position in grid units
            image: Block image surface
            block_type: Type of block - "disappear", "fix", or "item"
            item_data: Dict with item info for "item" type blocks (e.g., {"type": "gem", "image": "gem.png"})
            world: Reference to the game world (needed for spawning items)
        """
        super().__init__(x, y, image, convert_to_grid=True)
        self._original_y = self.rect.y  # Store original Y position
        self.block_type = block_type
        self.item_data = item_data
        self.world = world
        self.is_popping = False
        self.has_been_popped = False  # Track if block was already popped
        self.pop_animation_frame = 0
        self.pop_animation_duration = 10  # frames for pop animation
        self.pop_offset_y = 0
        self.max_pop_offset = -GRIDSIZE // 2  # How far the block moves up when popped
        self.original_image = image  # Store original image

        # Load the fixed block image for "fix", "item" and "invisible" types
        if block_type in ["fix", "item", "invisible"]:
            self.fixed_image = pg.image.load(
                os.path.join(IMAGEPATH, "block.png")
            ).convert_alpha()

    def pop(self):
        """Trigger the pop animation."""
        if not self.is_popping and not self.has_been_popped:
            self.is_popping = True
            self.has_been_popped = True
            self.pop_animation_frame = 0

            # Spawn item if this is an "item" type block
            if self.block_type == "item" and self.item_data and self.world:
                self._spawn_item()

    def _spawn_item(self):
        """Spawn the item from this block."""
        item_type = self.item_data.get("type")

        if item_type == "gem":
            from ..collectibles.gem import Gem

            # Get image from item_data or use default
            if "image" in self.item_data:
                gem_image = pg.image.load(
                    os.path.join(IMAGEPATH, self.item_data["image"])
                ).convert_alpha()
            else:
                gem_image = pg.image.load(
                    os.path.join(IMAGEPATH, "gem.png")
                ).convert_alpha()

            # Spawn gem above the block (convert from pixel to grid position)
            gem_x = self.rect.centerx // GRIDSIZE
            gem_y = (self.rect.top // GRIDSIZE) - 1  # One grid unit above

            gem = Gem(gem_x, gem_y, gem_image)
            self.world.items.add(gem)
            self.world.all_sprites.add(gem)

        elif item_type == "powerup":
            from ..collectibles.powerup import PowerUp

            # Spawn powerup above the block
            powerup_x = self.rect.centerx
            powerup_y = self.rect.top - GRIDSIZE

            powerup_type = self.item_data.get("powerup_type", 1)
            powerup = PowerUp(powerup_x, powerup_y, powerup_type, self.world)
            self.world.powerups.add(powerup)
            self.world.all_sprites.add(powerup)
        elif item_type == "weapon":
            # Spawn a weapon pickup (e.g., spraydose) above the block
            from ..collectibles.weapon import WeaponPickup

            weapon_name = self.item_data.get("weapon_name")
            if not weapon_name:
                return

            weapon_x = self.rect.centerx
            weapon_y = self.rect.top - GRIDSIZE

            wp = WeaponPickup(weapon_x, weapon_y, weapon_name)
            try:
                self.world.weapon_pickups.add(wp)
                self.world.all_sprites.add(wp)
            except Exception:
                # Defensive: if world is not available, still keep the sprite alive
                pass

    def update(self):
        """Update the block's pop animation."""
        if self.is_popping:
            self.pop_animation_frame += 1

            # Simple bounce animation: move up then down
            if self.pop_animation_frame <= self.pop_animation_duration // 2:
                # Moving up
                self.pop_offset_y = (
                    self.max_pop_offset
                    * self.pop_animation_frame
                    / (self.pop_animation_duration // 2)
                )
            else:
                # Moving back down
                remaining_frames = (
                    self.pop_animation_duration - self.pop_animation_frame
                )
                self.pop_offset_y = (
                    self.max_pop_offset
                    * remaining_frames
                    / (self.pop_animation_duration // 2)
                )

            # Update visual position
            self.rect.y = int(self.original_y + self.pop_offset_y)

            # End animation
            if self.pop_animation_frame >= self.pop_animation_duration:
                self.is_popping = False
                self.pop_animation_frame = 0
                self.pop_offset_y = 0
                self.rect.y = self.original_y

                # Handle different block types
                if self.block_type == "disappear":
                    # Remove the block from the game
                    self.kill()
                elif self.block_type in ("fix", "item", "invisible"):
                    # Change to solid block appearance
                    self.image = self.fixed_image
                    # If this block has a reference to the world, ensure it becomes a platform
                    if self.world is not None:
                        try:
                            if self not in self.world.platforms:
                                self.world.platforms.add(self)
                        except Exception:
                            # Be defensive if world/platforms not available yet
                            pass

    @property
    def original_y(self):
        """Get the original Y position of the block."""
        return self._original_y

    @original_y.setter
    def original_y(self, value):
        """Set the original Y position."""
        self._original_y = value
