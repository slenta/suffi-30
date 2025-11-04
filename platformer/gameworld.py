import pygame as pg
import os, sys
from .platform_class import Platform
from .moving_platform import MovingPlatform  # Import the MovingPlatform class
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
from .weapon import WeaponPickup
from .pipe import Pipe  # Import the Pipe class
from .spike import Spike  # Import the Spike class
from .ladder import Ladder, LadderTop  # Import the Ladder classes
from .waterfall import Waterfall, WaterfallTop  # Import the Waterfall classes
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
        self.game_over_flag = False
        self.current_fps = FPS  # Track current FPS for powerup effects
        self.return_to_level_selection = False  # Flag to return to level selection

        # Cheat code tracking
        self.cheat_buffer = ""  # Buffer to store typed characters
        self.marvin_mode = False  # Marvin mode state

        # Sprite groups
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.moving_platforms = pg.sprite.Group()
        self.gems = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.trophies = pg.sprite.Group()
        self.weapon_pickups = pg.sprite.Group()
        self.pipes = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
        self.ladders = pg.sprite.Group()
        self.ladder_tops = pg.sprite.Group()
        self.waterfalls = pg.sprite.Group()
        self.waterfall_tops = pg.sprite.Group()

        # Camera
        self.camera_offset_x = 0
        self.camera_offset_y = 0

        # Level bounds
        self.x_bounds = [-600, 3000]
        self.y_bounds = [-200, 300]

        # Level stack for sub-levels (stores tuples of level_name, player_state, return_position)
        self.level_stack = []
        self.current_level_name = None

        # Timer system
        self.level_time_limit = None  # Time limit in seconds (None = no limit)
        self.time_remaining = None  # Current time remaining in seconds
        self.timer_start_ticks = None  # Pygame ticks when timer started
        self.parent_time_remaining = (
            None  # Store parent level's time when entering sub-level
        )

        # Encounter message system
        self.encounter_message = None  # Current message to display
        self.encounter_message_timer = 0  # Timer for how long to display message
        self.encounter_message_duration = (
            180  # Duration in frames (3 seconds at 60 FPS)
        )

    def load_level(
        self, level_name, player_spawn_override=None, preserve_player_state=None
    ):
        """
        Load a level by name.

        Args:
            level_name: Name of the level to load
            player_spawn_override: Optional (x, y) tuple to override spawn position
            preserve_player_state: Optional dict with player state (gems, trophies, health, weapons)
        """
        # Clear all sprite groups
        self.all_sprites.empty()
        self.platforms.empty()
        self.moving_platforms.empty()
        self.gems.empty()
        self.enemies.empty()
        self.bullets.empty()
        self.powerups.empty()
        self.trophies.empty()
        self.weapon_pickups.empty()
        self.pipes.empty()
        self.spikes.empty()
        self.ladders.empty()
        self.ladder_tops.empty()

        # Store current level name
        self.current_level_name = level_name

        # Dynamically import the level configuration
        self.level_module = importlib.import_module(f"platformer.levels.{level_name}")
        self.level_config = self.level_module.level_config

        # Load ground boundaries
        self.ground_start = self.level_config["x_bounds"][0]
        self.ground_end = self.level_config["x_bounds"][1]
        self.bottom = self.level_config["y_bounds"][0]
        self.top = self.level_config["y_bounds"][1]

        # Initialize timer system
        # If we're in a sub-level, continue the parent's timer
        if self.level_stack:
            # Sub-level: inherit parent's remaining time
            if self.parent_time_remaining is not None:
                self.time_remaining = self.parent_time_remaining
                self.timer_start_ticks = pg.time.get_ticks()
                self.level_time_limit = None  # Sub-level doesn't have its own limit
                print(
                    f"⏱️ Sub-level continuing timer: {self.time_remaining:.1f}s remaining"
                )
        else:
            # Main level: initialize timer from level config
            self.level_time_limit = self.level_config.get("level_time", None)
            if self.level_time_limit is not None:
                self.time_remaining = float(self.level_time_limit)
                self.timer_start_ticks = pg.time.get_ticks()
                print(f"⏱️ Level timer started: {self.level_time_limit}s")
            else:
                self.time_remaining = None
                self.timer_start_ticks = None

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

        # Load moving platforms
        for moving_data in self.level_config.get("moving_platform_locations", []):
            # Determine which image to use
            platform_image = (
                grass_image
                if moving_data.get("platform_type", "block") == "grass"
                else block_image
            )

            mp = MovingPlatform(
                moving_data["x"],
                moving_data["y"],
                platform_image,
                moving_data.get("movement_type", "linear"),
                moving_data.get("speed", 1),
                moving_data.get("distance", 5),
                moving_data.get("direction", "horizontal"),
            )
            self.moving_platforms.add(mp)
            self.platforms.add(mp)  # Add to platforms for collision detection
            self.all_sprites.add(mp)

        for loc in self.level_config["gem_locations"]:
            x, y = loc
            g = Gem(x, y, gem_image)
            self.items.add(g)
            self.all_sprites.add(g)

            # Add ladders with tops
        if "ladder_locations" in self.level_config:
            for x, y in self.level_config["ladder_locations"][:-1]:  # All but last
                ladder = Ladder(x, y)
                self.all_sprites.add(ladder)
                self.ladders.add(ladder)
            # Last location gets a ladder top
            if self.level_config["ladder_locations"]:
                x, y = self.level_config["ladder_locations"][-1]
                ladder_top = LadderTop(x, y)
                self.all_sprites.add(ladder_top)
                self.ladder_tops.add(ladder_top)

        # Add waterfalls
        if "waterfall_locations" in self.level_config:
            for x, y in self.level_config["waterfall_locations"]:
                waterfall = Waterfall(x, y)
                self.all_sprites.add(waterfall)
                self.waterfalls.add(waterfall)

        # Use level-specific player spawn point if defined, otherwise use default
        player_spawn = self.level_config.get(
            "player_spawn", (PLAYER_START_X, PLAYER_START_Y)
        )

        # Override spawn if provided (e.g., when returning from sub-level)
        if player_spawn_override:
            player_spawn = player_spawn_override

        spawn_x, spawn_y = player_spawn

        # Create player with preserved state if provided
        if preserve_player_state:
            self.player = Player(
                spawn_x,
                spawn_y,
                world=self,
                start_gems=preserve_player_state.get("gems", 0),
                trophies_collected=preserve_player_state.get("trophies", 0),
                health=preserve_player_state.get("health", 100),
            )
            # Restore weapons
            if "weapons" in preserve_player_state:
                self.player.weapons = preserve_player_state["weapons"].copy()
                self.player.active_weapon = preserve_player_state.get("active_weapon")
        else:
            self.player = Player(spawn_x, spawn_y, world=self)

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
                enemy_data.get("chase_range", 10),  # Default chase range to 10 tiles
                enemy_data.get("melee_damage", 5),  # Default melee damage to 5
                enemy_data.get(
                    "can_throw_explosives", True
                ),  # Default to True for regular enemies
                enemy_data.get(
                    "is_minion", False
                ),  # Default to False for regular enemies
                enemy_data.get(
                    "can_summon_minions", False
                ),  # Default to False - must be explicitly enabled
                enemy_data.get("encounter_message", None),  # Optional encounter message
                enemy_data.get(
                    "shoot_cooldown", 60
                ),  # Default to 60 frames (1 second at 60 FPS)
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
        trophy_image_path = self.level_config.get("trophy_image", "trophy.png")
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

        # Load weapon pickups
        for weapon_data in self.level_config.get("weapon_locations", []):
            weapon = WeaponPickup(
                weapon_data["x"] * GRIDSIZE,
                weapon_data["y"] * GRIDSIZE,
                weapon_data["type"],
            )
            self.weapon_pickups.add(weapon)
            self.all_sprites.add(weapon)

        # Load pipes (for sub-levels)
        for pipe_data in self.level_config.get("pipe_locations", []):
            pipe = Pipe(
                pipe_data["x"] * GRIDSIZE,
                pipe_data["y"] * GRIDSIZE,
                pipe_data["sub_level"],
                pipe_data.get("return_x"),
                pipe_data.get("return_y"),
                pipe_data.get("direction", "down"),
            )
            self.pipes.add(pipe)
            self.platforms.add(pipe)  # Add to platforms so player can stand on it
            self.all_sprites.add(pipe)
            print(
                f"🚪 Created pipe at ({pipe_data['x']}, {pipe_data['y']}) -> grid ({pipe_data['x'] * GRIDSIZE}, {pipe_data['y'] * GRIDSIZE}) -> sub-level: {pipe_data['sub_level']}"
            )

        # Load spikes
        for spike_data in self.level_config.get("spike_locations", []):
            spike = Spike(
                spike_data["x"],
                spike_data["y"],
                spike_data.get("direction", "up"),
                spike_data.get("damage", 10),
            )
            self.spikes.add(spike)
            self.all_sprites.add(spike)

        # Load level-specific background music
        self.original_music_track = None
        self.alternative_music_tracks = []

        if (
            "background_music" in self.level_config
            and self.level_config["background_music"]
        ):
            music_path = self.level_config["background_music"]
            # Check if it's an absolute path or relative to platformer directory
            if not os.path.isabs(music_path):
                # Try relative to platformer directory (where assets now lives)
                music_path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), music_path
                )
            self.original_music_track = music_path
            sound_manager.play_background_music(music_path)

        # Load alternative music tracks if specified
        if "alternative_music_tracks" in self.level_config:
            for alt_music_path in self.level_config["alternative_music_tracks"]:
                if not os.path.isabs(alt_music_path):
                    alt_music_path = os.path.join(
                        os.path.dirname(os.path.abspath(__file__)), alt_music_path
                    )

                if os.path.exists(alt_music_path):
                    self.alternative_music_tracks.append(alt_music_path)
                    print(
                        f"🎵 Loaded alternative music: {os.path.basename(alt_music_path)}"
                    )
                else:
                    print(f"❌ Alternative music not found: {alt_music_path}")

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
        self.moving_platforms = pg.sprite.Group()

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

        # Load moving platforms
        for moving_data in self.level_config.get("moving_platform_locations", []):
            # Determine which image to use
            platform_image = (
                grass_image
                if moving_data.get("platform_type", "block") == "grass"
                else block_image
            )

            mp = MovingPlatform(
                moving_data["x"],
                moving_data["y"],
                platform_image,
                moving_data.get("movement_type", "linear"),
                moving_data.get("speed", 1),
                moving_data.get("distance", 5),
                moving_data.get("direction", "horizontal"),
            )
            self.moving_platforms.add(mp)
            self.platforms.add(mp)  # Add to platforms for collision detection
            self.all_sprites.add(mp)

        for item in self.items:
            self.items.add(item)
            self.all_sprites.add(item)

        # Load weapon pickups
        for weapon_data in self.level_config.get("weapon_locations", []):
            weapon = WeaponPickup(
                weapon_data["x"] * GRIDSIZE,
                weapon_data["y"] * GRIDSIZE,
                weapon_data["type"],
            )
            self.weapon_pickups.add(weapon)
            self.all_sprites.add(weapon)

        # Load enemies
        for enemy in self.enemies:
            enemy.reset_position()
            self.all_sprites.add(enemy)

        for powerup in self.powerups:
            self.all_sprites.add(powerup)

        for trophy in self.trophies:
            self.all_sprites.add(trophy)

        for weapon in self.weapon_pickups:
            self.all_sprites.add(weapon)

        # Re-add pipes
        for pipe in self.pipes:
            self.all_sprites.add(pipe)

        # Re-add spikes
        for spike in self.spikes:
            self.all_sprites.add(spike)

        self.all_sprites.add(self.exit)

        # Use level-specific player spawn point if defined, otherwise use default
        player_spawn = self.level_config.get(
            "player_spawn", (PLAYER_START_X, PLAYER_START_Y)
        )
        spawn_x, spawn_y = player_spawn

        self.player = Player(
            spawn_x,
            spawn_y,
            world=self,
            start_gems=self.player_gems,
            trophies_collected=self.player.trophies_collected,
        )
        self.player_sprite_group = pg.sprite.GroupSingle()
        self.player_sprite_group.add(self.player)
        self.all_sprites.add(self.player)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                self.keep_going = False
            elif event.type == pg.KEYDOWN:
                # Track typed characters for cheat code detection
                # Check if the key press has a unicode character that is alphabetic
                if event.unicode and event.unicode.isalpha():
                    char = event.unicode.lower()
                    self.cheat_buffer += char

                    # Keep buffer size reasonable (increase to 20 for reliability)
                    max_buffer_size = 20
                    if len(self.cheat_buffer) > max_buffer_size:
                        self.cheat_buffer = self.cheat_buffer[-max_buffer_size:]

                    # Check if cheat code has been typed
                    if CHEAT_CODE in self.cheat_buffer:
                        self.marvin_mode = not self.marvin_mode  # Toggle Marvin mode
                        self.cheat_buffer = ""  # Clear buffer after activation
                        if self.marvin_mode:
                            print("🎮 MARVIN MODE ACTIVATED! 🎮")
                            sound_manager.play_sound_effect("powerup_collect")
                        else:
                            print("🎮 Marvin Mode deactivated")

                # Game controls
                if event.key == pg.K_f:  # Shoot
                    self.player.shoot_bullet()
                elif event.key == pg.K_g:  # Melee attack
                    self.player.melee_attack()
                elif event.key == pg.K_e:
                    self.player.throw_exploding_object()

    def level_complete(self):
        # Check if we're in a sub-level
        if self.level_stack:
            # Return to parent level
            self.exit_sub_level()
            return

        # Otherwise, normal level completion
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
        user_quit = False
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    user_quit = True
                elif event.type == pg.KEYDOWN:
                    waiting = False

        # Set flags based on how user exited the completion screen
        self.keep_going = False
        if not user_quit:
            self.return_to_level_selection = True
            print("🏁 Level completed! Returning to level selection...")
        else:
            print("👋 User quit from level completion screen")

        # Implement your transition logic here (e.g., load next level or quit)

    def enter_sub_level(self, pipe):
        """Enter a sub-level through a pipe."""
        print(f"🚪 Entering sub-level: {pipe.sub_level_name}")

        # Save current timer state
        if self.time_remaining is not None:
            self.parent_time_remaining = self.time_remaining
            print(f"⏱️ Saving parent timer state: {self.time_remaining:.1f}s")

        # Save current level state
        player_state = {
            "gems": self.player.gems,
            "trophies": self.player.trophies_collected,
            "health": self.player.health,
            "weapons": (
                self.player.weapons.copy() if hasattr(self.player, "weapons") else {}
            ),
            "active_weapon": getattr(self.player, "active_weapon", None),
        }

        # Determine return position (use pipe's return position or player's current position)
        if pipe.return_x is not None and pipe.return_y is not None:
            return_position = (pipe.return_x, pipe.return_y)
        else:
            # Convert player's pixel position to grid position
            return_position = (
                self.player.rect.centerx // GRIDSIZE,
                self.player.rect.bottom // GRIDSIZE,
            )

        # Push current level onto stack
        self.level_stack.append(
            {
                "level_name": self.current_level_name,
                "player_state": player_state,
                "return_position": return_position,
            }
        )

        # Load the sub-level (preserve player state)
        self.load_level(pipe.sub_level_name, preserve_player_state=player_state)

        # Play a sound effect (optional)
        sound_manager.play_sound_effect("jump")

    def exit_sub_level(self):
        """Exit current sub-level and return to parent level."""
        if not self.level_stack:
            print("⚠️ No parent level to return to!")
            return

        print("🚪 Exiting sub-level...")

        # Save the current time remaining (it was counting down in the sub-level)
        current_time = self.time_remaining

        # Pop parent level from stack
        parent_level = self.level_stack.pop()

        # Get updated player state (preserve items collected in sub-level)
        current_state = {
            "gems": self.player.gems,
            "trophies": self.player.trophies_collected,
            "health": self.player.health,
            "weapons": (
                self.player.weapons.copy() if hasattr(self.player, "weapons") else {}
            ),
            "active_weapon": getattr(self.player, "active_weapon", None),
        }

        # Load parent level with return position and updated state
        self.load_level(
            parent_level["level_name"],
            player_spawn_override=parent_level["return_position"],
            preserve_player_state=current_state,
        )

        # Restore the timer that was counting down
        if current_time is not None:
            self.parent_time_remaining = current_time
            print(f"⏱️ Restoring parent timer: {current_time:.1f}s")

        # Play a sound effect (optional)
        sound_manager.play_sound_effect("jump")

    def update_camera(self):
        # Define the free movement range dynamically based on the camera offset
        # Horizontal camera
        free_range_left = self.camera_offset_x + WIDTH // 3
        free_range_right = self.camera_offset_x + 2 * WIDTH // 3

        # Adjust the camera offset only when the player moves outside the free range
        player_center_x = self.player.rect.centerx
        if player_center_x < free_range_left:
            self.camera_offset_x -= free_range_left - player_center_x
        elif player_center_x > free_range_right:
            self.camera_offset_x += player_center_x - free_range_right

        # Vertical camera
        free_range_top = self.camera_offset_y + HEIGHT // 3
        free_range_bottom = self.camera_offset_y + 2 * HEIGHT // 3

        # Adjust the camera offset only when the player moves outside the free range
        player_center_y = self.player.rect.centery
        if player_center_y < free_range_top:
            self.camera_offset_y -= free_range_top - player_center_y
        elif player_center_y > free_range_bottom:
            self.camera_offset_y += player_center_y - free_range_bottom

    def update(self):
        # Update timer
        if self.time_remaining is not None and self.timer_start_ticks is not None:
            elapsed_seconds = (pg.time.get_ticks() - self.timer_start_ticks) / 1000.0
            self.time_remaining = max(0, self.time_remaining - elapsed_seconds)
            self.timer_start_ticks = pg.time.get_ticks()  # Reset for next frame

            # Check if time has run out
            if self.time_remaining <= 0:
                self.on_timer_expired()

        # Update moving platforms first
        for moving_platform in self.moving_platforms:
            moving_platform.update()

        # Update all sprites except enemies
        for sprite in self.all_sprites:
            if not isinstance(sprite, Enemy) and sprite not in self.moving_platforms:
                sprite.update()

        # Update enemies and pass the player object
        for enemy in self.enemies:
            enemy.update(self.player)

        # Update bullets
        for bullet in self.bullets:
            bullet.update()

        # Update pipes
        for pipe in self.pipes:
            pipe.update()

        # Update the camera
        self.update_camera()

    def draw(self):
        # Draw background
        self.draw_background()

        # Draw all sprites with the camera offset
        for sprite in self.all_sprites:
            if sprite != self.player:
                offset_rect = sprite.rect.move(
                    -self.camera_offset_x, -self.camera_offset_y
                )
                self.screen.blit(sprite.image, offset_rect)

        # Draw player with weapon
        self.player.draw(self.screen, self.camera_offset_x, self.camera_offset_y)

        # Draw enemy health bars
        for enemy in self.enemies:
            enemy.draw_health_bar(
                self.screen, self.camera_offset_x, self.camera_offset_y
            )

        # Draw HUD
        draw_gems(self.screen, self.player)
        draw_trophies(self.screen, self.player, self.total_trophies)
        draw_health_bar(self.screen, self.player, 200, 20, self.player.max_health)

        # Draw encounter message (if active)
        self.draw_encounter_message()

        # Draw timer (top right corner)
        if self.time_remaining is not None:
            self.draw_timer()

        # Draw Marvin Mode indicator
        if self.marvin_mode:
            font = pg.font.Font(None, 72)
            marvin_text = font.render("MFG", True, (255, 215, 0))  # Gold color
            text_rect = marvin_text.get_rect(center=(WIDTH // 2, 40))
            # Add a semi-transparent black background for better readability
            bg_rect = text_rect.inflate(20, 10)
            bg_surface = pg.Surface((bg_rect.width, bg_rect.height), pg.SRCALPHA)
            bg_surface.fill((0, 0, 0, 128))
            self.screen.blit(bg_surface, bg_rect.topleft)
            self.screen.blit(marvin_text, text_rect)

        pg.display.flip()

    def draw_background(self):
        """Draw the background - either an image or solid color.
        Tiles the background at its original size, matching the level renderer behavior.
        """
        if self.background_image:
            # Calculate parallax scrolling offset for both X and Y
            bg_offset_x = int(self.camera_offset_x * self.background_scroll_speed)
            bg_offset_y = int(self.camera_offset_y * self.background_scroll_speed)

            # Get background and screen dimensions
            bg_width = self.background_image.get_width()
            bg_height = self.background_image.get_height()
            screen_width = self.screen.get_width()
            screen_height = self.screen.get_height()

            # Tile the background at its original size (no scaling)
            # This matches the level renderer behavior
            start_x = -(bg_offset_x % bg_width) if bg_width > 0 else 0
            start_y = -(bg_offset_y % bg_height) if bg_height > 0 else 0

            # Draw background tiles
            y = start_y
            while y < screen_height:
                x = start_x
                while x < screen_width:
                    self.screen.blit(self.background_image, (x, y))
                    x += bg_width
                y += bg_height
        else:
            # Fall back to solid color background
            # Check for background image first
            if "background_image" in self.level_config:
                if not hasattr(self, "background_surface"):
                    print(f"IMAGEPATH is: {IMAGEPATH}")
                    print(f"Current working directory: {os.getcwd()}")
                    print(
                        f"Looking for background image: {self.level_config['background_image']}"
                    )

                    # Try both with and without the backgrounds folder
                    bg_paths = [
                        os.path.join(
                            IMAGEPATH,
                            "backgrounds",
                            self.level_config["background_image"],
                        ),
                        os.path.join(IMAGEPATH, self.level_config["background_image"]),
                        os.path.join(
                            "platformer",
                            "assets",
                            "backgrounds",
                            self.level_config["background_image"],
                        ),
                    ]

                    for bg_path in bg_paths:
                        print(f"\nTrying path: {bg_path}")
                        print(f"File exists: {os.path.exists(bg_path)}")
                        try:
                            # Load the image
                            original_bg = pg.image.load(bg_path).convert()
                            print(
                                f"Successfully loaded background image from: {bg_path}"
                            )

                            # Calculate scaling to maintain aspect ratio
                            img_width, img_height = original_bg.get_size()
                            width_ratio = WIDTH / img_width
                            height_ratio = HEIGHT / img_height

                            # Use the smaller ratio to fit screen while maintaining aspect ratio
                            scale_ratio = max(width_ratio, height_ratio)
                            new_width = int(img_width * scale_ratio)
                            new_height = int(img_height * scale_ratio)

                            # Scale image maintaining aspect ratio
                            self.background_surface = pg.transform.scale(
                                original_bg, (new_width, new_height)
                            )

                            # Create a surface for the final background
                            final_surface = pg.Surface((WIDTH, HEIGHT))
                            final_surface.fill(
                                (0, 0, 0)
                            )  # Fill with black for letterboxing

                            # Calculate position to center the image
                            x_offset = (WIDTH - new_width) // 2
                            y_offset = (HEIGHT - new_height) // 2

                            # Blit the scaled image centered
                            final_surface.blit(
                                self.background_surface, (x_offset, y_offset)
                            )
                            self.background_surface = final_surface
                            break
                        except Exception as e:
                            print(f"Error loading from {bg_path}: {str(e)}")
                            self.background_surface = None
                            continue

                if self.background_surface:
                    # Apply parallax scrolling - background moves slower than foreground
                    bg_x = int(-self.camera_offset_x * 0.5) % WIDTH
                    # Draw the background twice to cover the whole screen when scrolling
                    self.screen.blit(self.background_surface, (bg_x, 0))
                    self.screen.blit(self.background_surface, (bg_x - WIDTH, 0))
                else:
                    # Fallback to color if image loading failed
                    bg_color = self.level_config.get(
                        "background_color", (135, 206, 235)
                    )
                    self.screen.fill(bg_color)
            else:
                # Use level-specific background color if defined, otherwise use default
                bg_color = self.level_config.get("background_color", (135, 206, 235))
                self.screen.fill(bg_color)

    def draw_timer(self):
        """Draw the countdown timer in the top right corner."""
        if self.time_remaining is None:
            return

        # Format time as MM:SS
        minutes = int(self.time_remaining // 60)
        seconds = int(self.time_remaining % 60)
        time_text = f"{minutes:02d}:{seconds:02d}"

        # Choose color based on remaining time
        if self.time_remaining <= 10:
            color = (255, 0, 0)  # Red when less than 10 seconds
        elif self.time_remaining <= 30:
            color = (255, 165, 0)  # Orange when less than 30 seconds
        else:
            color = (255, 255, 255)  # White otherwise

        # Render the timer text
        font = pg.font.Font(None, 48)
        timer_surface = font.render(time_text, True, color)

        # Position in top right corner with some padding
        timer_rect = timer_surface.get_rect()
        timer_rect.topright = (WIDTH - 20, 10)

        # Draw semi-transparent background for better readability
        bg_rect = timer_rect.inflate(20, 10)
        bg_surface = pg.Surface((bg_rect.width, bg_rect.height), pg.SRCALPHA)
        bg_surface.fill((0, 0, 0, 128))
        self.screen.blit(bg_surface, bg_rect.topleft)

        # Draw the timer
        self.screen.blit(timer_surface, timer_rect)

    def show_encounter_message(self, message):
        """Display an encounter message when player first sees an enemy."""
        self.encounter_message = message
        self.encounter_message_timer = self.encounter_message_duration

    def draw_encounter_message(self):
        """Draw the encounter message in yellow at the center of the screen."""
        if self.encounter_message_timer <= 0 or not self.encounter_message:
            return

        # Render the message in yellow
        font = pg.font.Font(None, 36)
        message_surface = font.render(self.encounter_message, True, (255, 255, 0))

        # Position at center of screen
        message_rect = message_surface.get_rect()
        message_rect.center = (WIDTH // 2, HEIGHT // 2)

        # Draw semi-transparent black background for better readability
        bg_rect = message_rect.inflate(40, 20)
        bg_surface = pg.Surface((bg_rect.width, bg_rect.height), pg.SRCALPHA)
        bg_surface.fill((0, 0, 0, 180))
        self.screen.blit(bg_surface, bg_rect.topleft)

        # Draw the message
        self.screen.blit(message_surface, message_rect)

        # Decrease the timer
        self.encounter_message_timer -= 1

    pass

    def load_sound_effects(self):
        """Load common sound effects for the game."""
        # Define common sound effects with their file paths
        sound_effects = {
            "jump": "jump.ogg",
            "gem_collect": "gem_collect.ogg",
            "enemy_hit": "enemy_hit.ogg",
            "player_hurt": "player_hurt.ogg",
            "player_death": "player_death.ogg",  # Player death/fall sound
            "powerup_collect": "powerup_collect.ogg",
            "trophy_collect": "trophy_collect.ogg",
            "level_complete": "level_complete.ogg",
            "explode": "explode.ogg",
            "menu_move": "menu_move.ogg",  # Menu cursor movement
            "menu_select": "menu_select.ogg",  # Menu selection
        }

        # Load each sound effect (silently ignore missing files)
        sounds_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "assets", "sounds"
        )
        for name, filename in sound_effects.items():
            full_path = os.path.join(sounds_dir, filename)
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

            # Check if it's an absolute path or relative to platformer directory
            if not os.path.isabs(bg_path):
                # Try relative to platformer directory (where assets now lives)
                bg_path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), bg_path
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
                        os.path.dirname(os.path.abspath(__file__)), alt_bg_path
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
        """Change to the next alternative background and music (used by power-up)."""
        if self.alternative_backgrounds:
            # Cycle through alternative backgrounds
            self.current_background_index = (self.current_background_index + 1) % (
                len(self.alternative_backgrounds) + 1
            )

            if self.current_background_index == 0:
                # Back to original background
                self.load_background_image()
                # Restore original music
                if self.original_music_track:
                    sound_manager.play_background_music(self.original_music_track)
                    print("🎨 Switched to original background and music")
                else:
                    print("🎨 Switched to original background")
            else:
                # Switch to alternative background
                self.background_image = self.alternative_backgrounds[
                    self.current_background_index - 1
                ]
                # Switch to alternative music if available
                if self.alternative_music_tracks and (
                    self.current_background_index - 1
                ) < len(self.alternative_music_tracks):
                    alt_music = self.alternative_music_tracks[
                        self.current_background_index - 1
                    ]
                    sound_manager.play_background_music(alt_music)
                    print(
                        f"🎨 Switched to alternative background {self.current_background_index} with music: {os.path.basename(alt_music)}"
                    )
                else:
                    print(
                        f"🎨 Switched to alternative background {self.current_background_index}"
                    )
        else:
            print("⚠️ No alternative backgrounds available")

    def set_fps(self, fps):
        """Set the game FPS (used by power-up effects)."""
        self.current_fps = fps
        print(f"🕐 FPS changed to {fps}")

    def reset_fps(self):
        """Reset FPS to default value."""
        self.current_fps = FPS
        print(f"🕐 FPS reset to {FPS}")

    def on_timer_expired(self):
        """Called when the level timer reaches zero. Currently a placeholder."""
        # TODO: Implement timer expiration logic (e.g., lose life, restart level, etc.)
        print("⏱️ Timer expired! (placeholder function)")
        pass

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
