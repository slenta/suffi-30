import pygame
import os
from platformer.config.settings import GRIDSIZE, IMAGEPATH


class Ladder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load the ladder image with proper transparency
        ladder_image = pygame.image.load(
            os.path.join(IMAGEPATH, "ladder", "ladder_02.png")
        ).convert_alpha()

        # Extract a small but wide portion from the middle of the image
        crop_width = 300  # Wide crop
        crop_height = 100  # Back to original height for cleaner look

        # Calculate start positions to get the exact middle of the image
        crop_start_x = (ladder_image.get_width() - crop_width) // 2
        crop_start_y = (ladder_image.get_height() - crop_height) // 2

        # Create a surface for the cropped portion
        cropped = pygame.Surface((crop_width, crop_height), pygame.SRCALPHA)
        cropped.blit(
            ladder_image, (0, 0), (crop_start_x, crop_start_y, crop_width, crop_height)
        )

        # Now scale this larger portion to our grid size
        scale_factor = 2.0  # Make it twice as wide as the grid
        target_width = int(GRIDSIZE * scale_factor)
        target_height = GRIDSIZE

        # Scale the cropped portion
        self.image = pygame.transform.scale(cropped, (target_width, target_height))

        # Center it on the grid
        final_surface = pygame.Surface((GRIDSIZE, GRIDSIZE), pygame.SRCALPHA)
        x_offset = (GRIDSIZE - target_width) // 2
        final_surface.blit(self.image, (x_offset, 0))
        self.image = final_surface

        self.rect = self.image.get_rect()
        self.rect.x = x * GRIDSIZE
        self.rect.y = y * GRIDSIZE

        # Create a narrower collision box for climbing
        self.climb_rect = self.rect.inflate(-GRIDSIZE // 2, 0)

    def can_climb(self, player):
        """Check if player can climb this ladder segment"""
        return self.climb_rect.colliderect(player.rect)


class LadderTop(Ladder):
    def __init__(self, x, y):
        super().__init__(x, y)
        # Add a platform-like top to the ladder image
        pygame.draw.rect(
            self.image, (139, 69, 19), (0, 0, GRIDSIZE, GRIDSIZE // 3)
        )  # Brown wooden top

        # This rect is used for collision detection when walking on top
        self.platform_rect = pygame.Rect(
            self.rect.x, self.rect.y, GRIDSIZE, GRIDSIZE // 3
        )

    def can_climb_up(self, player):
        """Check if player can climb up through this ladder top"""
        return (
            self.climb_rect.colliderect(player.rect)
            and player.rect.bottom > self.rect.top + GRIDSIZE // 3
        )

    def can_climb_down(self, player):
        """Check if player can start climbing down through this ladder top"""
        keys = pygame.key.get_pressed()
        # Check if player is on top of the ladder and pressing down
        is_on_top = (
            player.rect.bottom <= self.rect.top + GRIDSIZE // 3
            and player.rect.centerx >= self.rect.left
            and player.rect.centerx <= self.rect.right
        )
        return keys[pygame.K_DOWN] and is_on_top

    def should_block(self, player):
        """Check if this ladder top should act as a solid platform"""
        # Block if player is above the platform and not pressing down
        keys = pygame.key.get_pressed()
        return (
            player.rect.bottom <= self.rect.top + GRIDSIZE // 3
            and player.rect.centerx >= self.rect.left
            and player.rect.centerx <= self.rect.right
            and not keys[pygame.K_DOWN]
        )

        # Platform collision rect - only the top part is solid
        self.platform_rect = pygame.Rect(
            self.rect.x, self.rect.y, GRIDSIZE, GRIDSIZE // 4
        )

    def is_platform_collision(self, player):
        """Check if player is colliding with the solid top part"""
        # Only count as collision if player is above the platform
        return (
            self.platform_rect.colliderect(player.rect)
            and player.rect.bottom <= self.rect.top + GRIDSIZE // 4
        )

    def can_climb_down(self, player):
        """Check if player can start climbing down from top"""
        keys = pygame.key.get_pressed()
        on_top = (
            player.rect.bottom <= self.rect.top + GRIDSIZE // 4
            and player.rect.bottom > self.rect.top
            and self.climb_rect.collidepoint(player.rect.centerx, player.rect.bottom)
        )
        return on_top and keys[pygame.K_DOWN]
