import pygame as pg
import os, sys
from .platform_class import Platform
from .gem import Gem
from .player import Player
from .settings import *
from .bullet import Bullet  # Import the Bullet class
import importlib


## Class GameWorld
class GameWorld:

    def __init__(self):
        # Pygame und das Fenster initialisieren
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.keep_going = True
        self.camera_offset_x = 0  # Horizontal camera offset
        self.player_gems = 0
        self.bullets = pg.sprite.Group()  # Group to manage bullets

    def load_level(self, level_name):
        # Dynamically import the level configuration
        self.level_module = importlib.import_module(f"platformer.levels.{level_name}")
        self.level_config = self.level_module.level_config

        # Load ground boundaries
        self.ground_start = self.level_config["x_bounds"][0]
        self.ground_end = self.level_config["x_bounds"][1]
        self.bottom = self.level_config["y_bounds"][0]
        self.top = self.level_config["y_bounds"][1]

        # Load sprites
        grass_image = pg.image.load(
            os.path.join(IMAGEPATH, "grass_02.png")
        ).convert_alpha()
        block_image = pg.image.load(
            os.path.join(IMAGEPATH, "block_00.png")
        ).convert_alpha()
        gem_image = pg.image.load(os.path.join(IMAGEPATH, "gem.png")).convert_alpha()

        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.items = pg.sprite.Group()

        for loc in self.level_config["grass_locations"]:
            x, y = loc
            p = Platform(x, y, grass_image)
            self.platforms.add(p)
            self.all_sprites.add(p)

        for loc in self.level_config["block_locations"]:
            x, y = loc
            p = Platform(x, y, block_image)
            self.platforms.add(p)
            self.all_sprites.add(p)

        for loc in self.level_config["gem_locations"]:
            x, y = loc
            g = Gem(x, y, gem_image)
            self.items.add(g)
            self.all_sprites.add(g)

        self.player = Player(PLAYER_START_X, PLAYER_START_Y, world=self)
        self.player_sprite_group = pg.sprite.GroupSingle()
        self.player_sprite_group.add(self.player)
        self.all_sprites.add(self.player)

    def reset(self):
        # Neustart oder Status zurücksetzen
        # Hier werden alle Elemente der GameWorld initialisiert
        ## Load Assets
        grass_image = pg.image.load(
            os.path.join(IMAGEPATH, "grass_02.png")
        ).convert_alpha()
        block_image = pg.image.load(
            os.path.join(IMAGEPATH, "block_00.png")
        ).convert_alpha()
        gem_image = pg.image.load(os.path.join(IMAGEPATH, "gem.png")).convert_alpha()

        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()

        for loc in self.level_config["grass_locations"]:
            x, y = loc
            p = Platform(x, y, grass_image)
            self.platforms.add(p)
            self.all_sprites.add(p)

        for loc in self.level_config["block_locations"]:
            x, y = loc
            p = Platform(x, y, block_image)
            self.platforms.add(p)
            self.all_sprites.add(p)

        for item in self.items:
            self.items.add(item)
            self.all_sprites.add(item)

        self.player = Player(
            PLAYER_START_X, PLAYER_START_Y, world=self, start_gems=self.player_gems
        )
        self.player_sprite_group = pg.sprite.GroupSingle()
        self.player_sprite_group.add(self.player)
        self.all_sprites.add(self.player)

    def events(self):
        for event in pg.event.get():
            if (event.type == pg.QUIT) or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                self.keep_going = False
                self.game_over()
            elif event.type == pg.KEYDOWN and event.key == pg.K_f:
                self.shoot_bullet()

    def shoot_bullet(self):
        # Determine the direction based on player's x-velocity
        self.direction = 1 if self.player.vx >= 0 else -1
        bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, self)
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)

    def update_camera(self):
        # Define the free movement range dynamically based on the camera offset
        free_range_left = self.camera_offset_x + WIDTH // 3
        free_range_right = self.camera_offset_x + 2 * WIDTH // 3

        # Adjust the camera offset only when the player moves outside the free range
        player_center_x = self.player.rect.centerx
        if player_center_x < free_range_left:
            self.camera_offset_x -= free_range_left - player_center_x
        elif player_center_x > free_range_right:
            self.camera_offset_x += player_center_x - free_range_right

    def update(self):
        # Update all sprites
        self.all_sprites.update()
        # Update bullets
        self.bullets.update()
        # Update the camera
        self.update_camera()

    def draw(self):
        # Fill the screen with the background color
        self.screen.fill(BG_COLOR)

        # Draw all sprites with the camera offset
        for sprite in self.all_sprites:
            offset_rect = sprite.rect.move(-self.camera_offset_x, 0)
            self.screen.blit(sprite.image, offset_rect)

        # Draw the player's gems (lifes) at the top left corner
        self.draw_gems()

        # Update the display
        pg.display.flip()

    def draw_gems(self):
        # Render the text showing the number of gems
        font = pg.font.Font(None, 36)  # Use default font with size 36
        text = font.render(
            f"Player Lives: {self.player.gems}", True, (255, 255, 255)
        )  # White color
        self.screen.blit(text, (10, 10))  # Position at top-left corner (10, 10)

    def start_screen(self):
        pass

    def win_screen(self):
        pass

    def loose_screen(self):
        self.player_gems = self.player.gems
        pass

    def game_over(self):
        print("Bye, Bye, Baby!")
        pg.quit()
        sys.exit()


## Ende Class GameWorld
