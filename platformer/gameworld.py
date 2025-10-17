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
from .draw import *
from .sound_manager import sound_manager  # Import the sound manager
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
        self.alternative_backgrounds = []  # List of alternative background images
        self.current_background_index = 0  # Track which background is currently shown

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
        trophy_image_path = self.level_config.get(
            "trophy_image", "data/images/trophy.png"
        )
        # Extract just the filename from the path for the Trophy class
        trophy_filename = os.path.basename(trophy_image_path)
        for x, y in self.level_config["trophy_locations"]:
            trophy = Trophy(x * GRIDSIZE, y * GRIDSIZE, trophy_filename)
            self.trophies.add(trophy)
            self.all_sprites.add(trophy)
        self.total_trophies = len(self.level_config["trophy_locations"])

        exit_x, exit_y = self.level_config["exit_location"]
        self.exit = Exit(exit_x * GRIDSIZE, exit_y * GRIDSIZE)
        self.all_sprites.add(self.exit)

        # Load level-specific background music
        if (
            "background_music" in self.level_config
            and self.level_config["background_music"]
        ):
            music_path = self.level_config["background_music"]
            # Check if it's an absolute path or relative to game directory
            if not os.path.isabs(music_path):
                # Try relative to game root directory first
                music_path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)), music_path
                )
            sound_manager.play_background_music(music_path)

        # Load background image
        self.load_background_image()

        # Load common sound effects (if they exist)
        self.load_sound_effects()

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
                event.type == pg.KEYDOWN and event.key == KEYBINDINGS.get("quit")
            ):
                self.keep_going = False
                self.game_over()
            elif event.type == pg.KEYDOWN and event.key == KEYBINDINGS.get("shoot"):
                self.player.shoot_bullet()
            elif event.type == pg.KEYDOWN and event.key == KEYBINDINGS.get("throw"):
                self.player.throw_exploding_object()

    def level_complete(self):
        fade_to_black(
            screen=self.screen,
            draw_callback=self.draw,
            width=WIDTH,
            height=HEIGHT,
            duration=60,
        )
        show_level_complete_text(screen=self.screen, width=WIDTH, height=HEIGHT)
        # Wait until the user closes the window or presses any key
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN):
                    waiting = False
        pg.quit()
        sys.exit()

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
        # Draw background
        self.draw_background()

        # Draw all sprites with the camera offset
        for sprite in self.all_sprites:
            offset_rect = sprite.rect.move(-self.camera_offset_x, 0)
            self.screen.blit(sprite.image, offset_rect)

        # Draw health bars for enemies
        for enemy in self.enemies:
            enemy.draw_health_bar(self.screen, self.camera_offset_x)

        # Draw the player's gems (lives) at the top left corner
        draw_gems(screen=self.screen, player=self.player)
        trophy_image_path = self.level_config.get(
            "trophy_image", "data/images/trophy.png"
        )
        draw_trophies(
            screen=self.screen,
            player=self.player,
            total_trophies=self.total_trophies,
            trophy_image_path=trophy_image_path,
        )
        draw_health_bar(
            screen=self.screen,
            player=self.player,
            width=200,
            height=15,
            max_health=self.player.max_health,
        )

        # Update the display
        pg.display.flip()

    def draw_background(self):
        """Draw the background - either an image or solid color."""
        if self.background_image:
            # Calculate parallax scrolling offset
            bg_offset = int(self.camera_offset_x * self.background_scroll_speed)

            # Get background and screen dimensions
            bg_width = self.background_image.get_width()
            bg_height = self.background_image.get_height()
            screen_width = self.screen.get_width()
            screen_height = self.screen.get_height()

            # Scale background to fit screen height if needed
            if bg_height != screen_height:
                scale_factor = screen_height / bg_height
                scaled_width = int(bg_width * scale_factor)
                self.background_image = pg.transform.scale(
                    self.background_image, (scaled_width, screen_height)
                )
                bg_width = scaled_width

            # Tile the background horizontally to cover the entire screen width
            start_x = -(bg_offset % bg_width)

            # Draw background tiles
            x = start_x
            while x < screen_width:
                self.screen.blit(self.background_image, (x, 0))
                x += bg_width
        else:
            # Fall back to solid color background
            self.screen.fill(BG_COLOR)

    pass

    def load_sound_effects(self):
        """Load common sound effects for the game."""
        # Define common sound effects with their file paths
        sound_effects = {
            "jump": "sounds/jump.wav",
            "gem_collect": "sounds/gem_collect.wav",
            "enemy_hit": "sounds/enemy_hit.wav",
            "player_hurt": "sounds/player_hurt.wav",
            "player_death": "sounds/player_death.wav",  # Player death/fall sound
            "powerup_collect": "sounds/powerup_collect.wav",
            "trophy_collect": "sounds/trophy_collect.wav",
            "level_complete": "sounds/level_complete.wav",
            "explode": "sounds/explode.wav",
            "menu_move": "sounds/menu_move.wav",  # Menu cursor movement
            "menu_select": "sounds/menu_select.wav",  # Menu selection
        }

        # Load each sound effect (silently ignore missing files)
        for name, path in sound_effects.items():
            full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), path)
            sound_manager.load_sound_effect(name, full_path)

    def load_background_image(self):
        """Load level-specific background image."""
        self.background_image = None
        self.background_scroll_speed = 0.5  # Default parallax scroll speed
        self.alternative_backgrounds = []  # Reset alternative backgrounds
        self.current_background_index = 0

        if (
            "background_image" in self.level_config
            and self.level_config["background_image"]
        ):
            bg_path = self.level_config["background_image"]

            # Check if it's an absolute path or relative to game directory
            if not os.path.isabs(bg_path):
                # Try relative to game root directory first
                bg_path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)), bg_path
                )

            # Load background image
            if os.path.exists(bg_path):
                try:
                    self.background_image = pg.image.load(bg_path).convert()
                    print(f"🖼️ Loaded background image: {os.path.basename(bg_path)}")

                    # Get optional background settings
                    if "background_scroll_speed" in self.level_config:
                        self.background_scroll_speed = self.level_config[
                            "background_scroll_speed"
                        ]

                except pg.error as e:
                    print(f"❌ Error loading background image: {e}")
                    self.background_image = None
            else:
                print(f"❌ Background image not found: {bg_path}")

        # Load alternative backgrounds if specified
        if "alternative_backgrounds" in self.level_config:
            for alt_bg_path in self.level_config["alternative_backgrounds"]:
                if not os.path.isabs(alt_bg_path):
                    alt_bg_path = os.path.join(
                        os.path.dirname(os.path.dirname(__file__)), alt_bg_path
                    )

                if os.path.exists(alt_bg_path):
                    try:
                        alt_bg = pg.image.load(alt_bg_path).convert()
                        self.alternative_backgrounds.append(alt_bg)
                        print(
                            f"🖼️ Loaded alternative background: {os.path.basename(alt_bg_path)}"
                        )
                    except pg.error as e:
                        print(f"❌ Error loading alternative background: {e}")
                else:
                    print(f"❌ Alternative background not found: {alt_bg_path}")

    def change_background(self):
        """Change to the next alternative background (used by power-up)."""
        if self.alternative_backgrounds:
            # Cycle through alternative backgrounds
            self.current_background_index = (self.current_background_index + 1) % (
                len(self.alternative_backgrounds) + 1
            )

            if self.current_background_index == 0:
                # Back to original background
                self.load_background_image()
                print("🎨 Switched to original background")
            else:
                # Switch to alternative background
                self.background_image = self.alternative_backgrounds[
                    self.current_background_index - 1
                ]
                print(
                    f"🎨 Switched to alternative background {self.current_background_index}"
                )
        else:
            print("⚠️ No alternative backgrounds available")

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
