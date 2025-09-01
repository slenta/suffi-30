import pygame as pg
import os, sys
from .platform_class import Platform
from .gem import Gem
from .player import Player
from .settings import *
from .bullet import Bullet  # Import the Bullet class
from .enemies import Enemy
from .bullet import ExplodingObject  # Import the ExplodingObject class
from .powerup import PowerUp  # Import the PowerUp class
from .trophy import Exit, Trophy
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
        self.enemies = pg.sprite.Group()  # Group to manage enemies
        self.powerups = pg.sprite.Group()  # Group to manage power-ups

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

        # Load enemies
        for enemy_data in self.level_config["enemy_locations"]:
            enemy = Enemy(
                enemy_data["x"],  # Grid-based x-coordinate
                enemy_data["y"],  # Grid-based y-coordinate
                os.path.join(IMAGEPATH, enemy_data["image"]),
                enemy_data["speed"],
                enemy_data["patrol_range"],
                enemy_data.get(
                    "size_multiplier", 1
                ),  # Default to 1 square if not specified
                enemy_data.get("health", 1),  # Default health to 1 if not specified
                enemy_data.get("damage", 1),  # Default damage to 1 if not specified
                enemy_data.get("shoot_range", 5),  # Default shooting range to 5 tiles
                self,  # Pass the GameWorld instance as the world
            )
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        # Load power-ups
        for powerup_data in self.level_config["powerup_locations"]:
            powerup = PowerUp(
                powerup_data["x"] * GRIDSIZE,
                powerup_data["y"] * GRIDSIZE,
                powerup_data["type"],
                self,
            )
            self.all_sprites.add(powerup)
            self.powerups.add(powerup)

        # Load trophies and exits
        self.trophies = pg.sprite.Group()
        for x, y in self.level_config["trophy_locations"]:
            trophy = Trophy(x * GRIDSIZE, y * GRIDSIZE)
            self.trophies.add(trophy)
            self.all_sprites.add(trophy)
        self.total_trophies = len(self.level_config["trophy_locations"])

        exit_x, exit_y = self.level_config["exit_location"]
        self.exit = Exit(exit_x * GRIDSIZE, exit_y * GRIDSIZE)
        self.all_sprites.add(self.exit)

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

        # Load enemies
        for enemy in self.enemies:
            enemy.reset_position()
            self.all_sprites.add(enemy)

        for powerup in self.powerups:
            self.all_sprites.add(powerup)

        for trophy in self.trophies:
            self.all_sprites.add(trophy)

        self.all_sprites.add(self.exit)

        self.player = Player(
            PLAYER_START_X,
            PLAYER_START_Y,
            world=self,
            start_gems=self.player_gems,
            trophies_collected=self.player.trophies_collected,
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
            elif (
                event.type == pg.KEYDOWN and event.key == pg.K_e
            ):  # Detect 'E' key press
                self.throw_exploding_object()

    def shoot_bullet(self):
        # Determine the direction of the bullet based on the player's current velocity
        direction_x = 1 if self.player.vx >= 0 else -1
        direction_y = 0  # Assuming bullets only move horizontally for now
        damage = 1  # Set the damage dealt by the player's bullets

        # Create the bullet
        bullet = Bullet(
            self.player.rect.centerx,
            self.player.rect.centery,
            direction_x,
            direction_y,
            damage,  # Pass the GameWorld instance as the world
            self,
        )
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)

    def throw_exploding_object(self):
        # Determine the direction of the throw based on the player's facing direction
        direction_x = 1 if self.player.vx >= 0 else -1
        direction_y = 0  # Exploding objects are thrown horizontally
        damage = 10  # Set the damage dealt by the exploding object

        # Create the exploding object
        exploding_object = ExplodingObject(
            self.player.rect.centerx,
            self.player.rect.centery,
            direction_x,
            direction_y,
            damage,
            self,
        )
        self.bullets.add(exploding_object)
        self.all_sprites.add(exploding_object)

    def fade_to_black(self, duration=60):
        """Fade the screen to black from the center outward over 'duration' frames."""
        clock = pg.time.Clock()
        for frame in range(duration):
            self.draw()  # Draw the current frame
            # Calculate the radius for this frame
            max_radius = int((WIDTH**2 + HEIGHT**2) ** 0.5 // 2)
            radius = int((frame / duration) * max_radius)
            # Create a transparent surface
            fade_surface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
            # Draw a solid black circle in the center
            pg.draw.circle(
                fade_surface, (0, 0, 0, 255), (WIDTH // 2, HEIGHT // 2), radius
            )
            self.screen.blit(fade_surface, (0, 0))
            pg.display.flip()
            clock.tick(60)

    def show_level_complete_text(self):
        """Display 'Level Complete!' in big white letters at the center of the screen."""
        self.screen.fill((0, 0, 0))
        font = pg.font.Font(None, 120)  # Big font
        text = font.render("Level Complete!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pg.display.flip()

        # Wait until the user closes the window or presses any key
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN):
                    waiting = False
        pg.quit()
        sys.exit()

    def level_complete(self):
        self.fade_to_black(duration=60)
        self.show_level_complete_text()
        # Implement your transition logic here (e.g., load next level or quit)

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
        # Update all sprites except enemies
        for sprite in self.all_sprites:
            if not isinstance(sprite, Enemy):
                sprite.update()

        # Update enemies and pass the player object
        for enemy in self.enemies:
            enemy.update(self.player)

        # Update bullets
        for bullet in self.bullets:
            bullet.update()

        # Update the camera
        self.update_camera()

    def draw(self):
        # Fill the screen with the background color
        self.screen.fill(BG_COLOR)

        # Draw all sprites with the camera offset
        for sprite in self.all_sprites:
            offset_rect = sprite.rect.move(-self.camera_offset_x, 0)
            self.screen.blit(sprite.image, offset_rect)

        # Draw health bars for enemies
        for enemy in self.enemies:
            enemy.draw_health_bar(self.screen, self.camera_offset_x)

        # Draw the player's gems (lives) at the top left corner
        self.draw_gems()
        self.draw_trophies()
        self.draw_health_bar()  # Draw the health bar

        # Update the display
        pg.display.flip()

    def draw_trophies(self):
        # Render the text showing the number of trophies collected
        font = pg.font.Font(None, 36)  # Use default font with size 36
        text = font.render(
            f"Trophies Collected: {self.player.trophies_collected} / {self.total_trophies}",
            True,
            (255, 255, 255),
        )  # White color
        self.screen.blit(text, (10, 50))  # Position below the gems text

    def draw_gems(self):
        # Render the text showing the number of gems
        font = pg.font.Font(None, 36)  # Use default font with size 36
        text = font.render(
            f"Player Lives: {self.player.gems}", True, (255, 255, 255)
        )  # White color
        self.screen.blit(text, (10, 10))  # Position at top-left corner (10, 10)

    def draw_health_bar(self):
        # Define the position and size of the health bar
        bar_width = 200
        bar_height = 20
        bar_x = WIDTH - bar_width - 20  # Top-right corner with padding
        bar_y = 10

        # Calculate the width of the filled portion based on player's health
        max_health = self.player.max_health  # Assume max_health is defined in Player
        current_health = self.player.health
        fill_width = int((current_health / max_health) * bar_width)

        # Draw the health bar background (gray)
        pg.draw.rect(
            self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height)
        )

        # Draw the filled portion of the health bar (green)
        pg.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, fill_width, bar_height))

        # Optionally, draw a border around the health bar (white)
        pg.draw.rect(
            self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2
        )

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
