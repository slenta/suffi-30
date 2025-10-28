import pygame
import os
from platformer.settings import GRIDSIZE, IMAGEPATH

class Waterfall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load the waterfall image with proper transparency
        waterfall_image = pygame.image.load(
            os.path.join(IMAGEPATH, "waterfall", "waterfall_01.png")
        ).convert_alpha()
        
        # Extract a portion from the middle of the image
        crop_width = 300  # Wide crop like the ladder
        crop_height = 100  # Same height as ladder for consistency
        
        # Calculate start positions to get the exact middle of the image
        crop_start_x = (waterfall_image.get_width() - crop_width) // 2
        crop_start_y = (waterfall_image.get_height() - crop_height) // 2
        
        # Create a surface for the cropped portion
        cropped = pygame.Surface((crop_width, crop_height), pygame.SRCALPHA)
        cropped.blit(waterfall_image, (0, 0), 
                    (crop_start_x, crop_start_y, crop_width, crop_height))
        
        # Scale to final size
        scale_factor = 2.0  # Same as ladder for consistency
        target_width = int(GRIDSIZE * scale_factor)
        target_height = GRIDSIZE
        
        # Scale the cropped portion
        self.image = pygame.transform.scale(cropped, (target_width, target_height))
        
        # Center it in the grid
        final_surface = pygame.Surface((GRIDSIZE, GRIDSIZE), pygame.SRCALPHA)
        x_offset = (GRIDSIZE - target_width) // 2
        final_surface.blit(self.image, (x_offset, 0))
        self.image = final_surface
        
        self.rect = self.image.get_rect()
        self.rect.x = x * GRIDSIZE
        self.rect.y = y * GRIDSIZE
        
        # Create a narrower collision box
        self.flow_rect = self.rect.inflate(-GRIDSIZE//2, 0)
    
    def can_flow(self, player):
        """Check if player can flow in this waterfall segment"""
        return self.flow_rect.colliderect(player.rect)

class WaterfallTop(Waterfall):
    def __init__(self, x, y):
        super().__init__(x, y)
        # Add splash effect at top
        pygame.draw.rect(self.image, (173, 216, 230), (0, 0, GRIDSIZE, GRIDSIZE//4))
        
        # Platform collision rect - only the top part is solid
        self.platform_rect = pygame.Rect(
            self.rect.x,
            self.rect.y,
            GRIDSIZE,
            GRIDSIZE//4
        )
    
    def is_platform_collision(self, player):
        """Check if player is colliding with the solid top part"""
        # Only count as collision if player is above or at the platform level
        return (self.platform_rect.colliderect(player.rect) and 
                player.rect.bottom <= self.rect.top + GRIDSIZE//4 and
                player.vy >= 0)  # Only when falling or standing
    
    def can_flow_down(self, player):
        """Check if player can start flowing down from top"""
        keys = pygame.key.get_pressed()
        on_top = (player.rect.bottom <= self.rect.top + GRIDSIZE//4 and
                 player.rect.bottom > self.rect.top and
                 self.flow_rect.collidepoint(player.rect.centerx, player.rect.bottom))
        return on_top and keys[pygame.K_DOWN]