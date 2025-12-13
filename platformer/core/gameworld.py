import pygame as pg
import os, sys
import asyncio
from ..world.platform_class import Platform
from ..world.moving_platform import MovingPlatform
from ..world.poppable_block import PoppableBlock
from ..collectibles.gem import Gem
from ..entities.player import Player
from ..config.settings import *
from ..entities.bullet import Bullet
from ..entities.enemies import Enemy
from ..entities.bullet import ExplodingObject
from ..collectibles.powerup import PowerUp
from ..collectibles.trophy import Exit, Trophy
from .draw import *
from .sound_manager import sound_manager
from ..collectibles.weapon import WeaponPickup
from ..world.pipe import Pipe
from ..world.spike import Spike
from ..world.ladder import Ladder, LadderTop
from ..world.waterfall import Waterfall, WaterfallTop
from ..config.enemy_config import get_enemy_config
from ..config.gem_config import get_gem_config
from ..config.trophy_config import get_trophy_config
from ..config.api_config import API_BASE_URL
from ..config.constants import PIXELATION_FACTOR, PIXELATION_DURATION
from .highscore_manager import HighscoreManager
import importlib
from IPython import embed


## Class GameWorld
class GameWorld:
    """Main game world class that manages all game objects, levels, and game state."""

    def __init__(self):
        # Initialize pygame and window
        # Only init pygame if not already initialized (Pygbag handles this)
        if not pg.get_init():
            pg.init()
        # Get existing display surface if available (Pygbag creates it)
        self.screen = pg.display.get_surface()
        if self.screen is None:
            self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.keep_going = True
        self.game_over_flag = False
        self.level_complete_flag = False  # Flag for async level completion
        self.current_fps = FPS
        self.return_to_level_selection = False

        # Cheat code tracking
        self.cheat_buffer = ""
        self.marvin_mode = False
        self.marvin_mode_ever_used = False  # Track if cheat was ever used

        # Highscore system
        self.highscore_manager = HighscoreManager(api_base_url=API_BASE_URL)
        self.current_score = 0

        # Sprite groups
        self._init_sprite_groups()

        # Camera
        self.camera_offset_x = 0
        self.camera_offset_y = 0

        # Level bounds
        self.x_bounds = [-600, 3000]
        self.y_bounds = [-200, 300]

        # Level stack for sub-levels
        self.level_stack = []
        self.current_level_name = None

        # Timer system
        self.level_time_limit = None
        self.time_remaining = None
        self.timer_start_ticks = None
        self.parent_time_remaining = None

        # Background state tracking for sub-level transitions
        self.parent_background_index = 0
        self.parent_music_track = None  # Track music state for sub-level transitions

        # Encounter message system
        self.encounter_message = None
        self.encounter_message_color = None  # Custom color for message
        self.encounter_message_timer = 0
        self.encounter_message_duration = 180  # 3 seconds at 60 FPS

        # Track collected items to prevent respawning
        self.collected_items = set()

        # Track killed enemies to prevent respawning
        self.killed_enemies = set()

        # Global trophy count (parent + sub-levels combined)
        self.global_total_trophies = 0

    def _init_sprite_groups(self):
        """Initialize all sprite groups."""
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.moving_platforms = pg.sprite.Group()
        self.gems = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.trophies = pg.sprite.Group()
        self.required_items = pg.sprite.Group()  # Required items for exit (e.g., keys, tickets)
        self.weapon_pickups = pg.sprite.Group()
        self.pipes = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
        self.ladders = pg.sprite.Group()
        self.ladder_tops = pg.sprite.Group()
        self.waterfalls = pg.sprite.Group()
        self.waterfall_tops = pg.sprite.Group()
        self.poppable_blocks = pg.sprite.Group()

    def _clear_sprite_groups(self):
        """Clear all sprite groups."""
        # Before clearing enemies, track any that are dying so they don't respawn
        for enemy in self.enemies:
            if hasattr(enemy, "is_dying") and enemy.is_dying:
                # Enemy is in the middle of dying - ensure it's tracked as killed
                if hasattr(enemy, "enemy_id") and not getattr(
                    enemy, "is_minion", False
                ):
                    self.killed_enemies.add(enemy.enemy_id)
                    print(
                        f"💀 Tracked dying enemy before group clear: {enemy.enemy_id}"
                    )

        for group in [
            self.all_sprites,
            self.platforms,
            self.moving_platforms,
            self.gems,
            self.enemies,
            self.bullets,
            self.powerups,
            self.trophies,
            self.required_items,
            self.weapon_pickups,
            self.pipes,
            self.spikes,
            self.ladders,
            self.ladder_tops,
            self.waterfalls,
            self.waterfall_tops,
            self.poppable_blocks,
        ]:
            group.empty()

    def load_level(
        self,
        level_name,
        player_spawn_override=None,
        preserve_player_state=None,
        is_sub_level_transition=False,
    ):
        """
        Load a level by name.

        Args:
            level_name: Name of the level to load
            player_spawn_override: Optional (x, y) tuple to override spawn position
            preserve_player_state: Optional dict with player state (gems, trophies, health, weapons)
            is_sub_level_transition: True if entering or exiting a sub-level
        """
        # Clear all sprite groups
        self._clear_sprite_groups()

        # Only clear collected items and killed enemies if loading a truly different level
        # (not a sub-level transition and not the same level during reset)
        is_same_level = self.current_level_name == level_name

        print(f"🔍 load_level: current={self.current_level_name}, new={level_name}")
        print(
            f"🔍 is_same_level={is_same_level}, is_sub_level_transition={is_sub_level_transition}"
        )
        print(f"🔍 collected_items count: {len(self.collected_items)}")
        print(f"🔍 killed_enemies count: {len(self.killed_enemies)}")

        if not is_sub_level_transition and not is_same_level:
            # Starting a completely new level - clear all tracking
            self.collected_items.clear()
            self.killed_enemies.clear()
            print("🧹 Cleared collected items and killed enemies for new level")
        elif is_sub_level_transition:
            print(
                "🔄 Sub-level transition: preserving collected items and killed enemies"
            )
        else:
            print("♻️ Same level reload: preserving collected items and killed enemies")

        self.current_level_name = level_name

        # Import level configuration
        self.level_module = importlib.import_module(f"platformer.levels.{level_name}")
        self.level_config = self.level_module.level_config

        # Optional: allow a level to force-reset collected items / killed enemies
        # Useful for level editing so placed enemies always respawn when the level
        # is loaded even if this is considered the "same" level.
        # If a level requests resetting placed enemies/items on load, only honor
        # that when we are doing a fresh load (not when restoring player state
        # after a respawn). This ensures that respawns keep previously collected
        # gems/trophies, while game-over or explicit fresh loads still clear them.
        if self.level_config.get("reset_killed_on_load", False) and not preserve_player_state:
            self.collected_items.clear()
            self.killed_enemies.clear()
            print("🧹 reset_killed_on_load is set and no preserved player state: cleared collected items and killed enemies")

        # Set level boundaries
        self.ground_start = self.level_config["x_bounds"][0]
        self.ground_end = self.level_config["x_bounds"][1]
        self.bottom = self.level_config["y_bounds"][0]
        self.top = self.level_config["y_bounds"][1]

        # Initialize timer system
        if self.parent_time_remaining is not None:
            # Continuing from sub-level or parent level: inherit remaining time
            self.time_remaining = self.parent_time_remaining
            self.timer_start_ticks = pg.time.get_ticks()
            self.level_time_limit = None
            self.parent_time_remaining = None  # Clear it after using
            print(f"⏱️ Continuing timer: {self.time_remaining:.1f}s remaining")
        elif self.level_stack:
            # Shouldn't happen, but safety check
            print("⚠️ In sub-level but no parent_time_remaining set")
            self.level_time_limit = self.level_config.get("level_time", None)
            if self.level_time_limit is not None:
                self.time_remaining = float(self.level_time_limit)
                self.timer_start_ticks = pg.time.get_ticks()
            else:
                self.time_remaining = None
                self.timer_start_ticks = None
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

        # Load common images
        # Allow level-specific override for grass tile
        default_grass_path = os.path.join(IMAGEPATH, "grass.png")
        grass_image = None
        if "grass_image" in self.level_config and self.level_config["grass_image"]:
            custom = self.level_config["grass_image"]
            if not os.path.isabs(custom):
                possible = [
                    os.path.join(
                        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        custom,
                    ),
                    os.path.join(IMAGEPATH, custom),
                ]
            else:
                possible = [custom]

            for p in possible:
                if os.path.exists(p):
                    try:
                        grass_image = pg.image.load(p).convert_alpha()
                        print(
                            f"🌾 Loaded custom grass image for level: {os.path.basename(p)}"
                        )
                        break
                    except Exception as e:
                        print(f"Error loading custom grass image {p}: {e}")
                        grass_image = None

        if grass_image is None:
            grass_image = pg.image.load(
                os.path.join(IMAGEPATH, "grass.png")
            ).convert_alpha()

        # Load block image (allow level-specific override or tint)
        default_block_path = os.path.join(IMAGEPATH, "block.png")
        block_image = None
        # If the level provides a custom block image path, try to load it
        if "block_image" in self.level_config and self.level_config["block_image"]:
            custom_path = self.level_config["block_image"]
            if not os.path.isabs(custom_path):
                # If path is relative, allow paths relative to project root or IMAGEPATH
                possible = [
                    os.path.join(
                        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        custom_path,
                    ),
                    os.path.join(IMAGEPATH, custom_path),
                ]
            else:
                possible = [custom_path]

            for p in possible:
                if os.path.exists(p):
                    try:
                        block_image = pg.image.load(p).convert_alpha()
                        print(
                            f"🧱 Loaded custom block image for level: {os.path.basename(p)}"
                        )
                        break
                    except Exception as e:
                        print(f"Error loading custom block image {p}: {e}")
                        block_image = None

        # Fallback to default block image
        if block_image is None:
            block_image = pg.image.load(default_block_path).convert_alpha()

        # Apply optional tint to block image for level-specific look
        if "block_tint" in self.level_config and self.level_config["block_tint"]:
            try:
                tint = tuple(self.level_config["block_tint"])  # (r,g,b)
                overlay = pg.Surface(block_image.get_size(), pg.SRCALPHA)
                overlay.fill((tint[0], tint[1], tint[2], 255))
                tinted = block_image.copy()
                tinted.blit(overlay, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
                block_image = tinted
                print(f"🧱 Applied block tint {tint} for level")
            except Exception as e:
                print(f"Error applying block tint: {e}")
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

        # Load poppable blocks
        default_poppable_block_image = pg.image.load(
            os.path.join(IMAGEPATH, "block_pop.png")
        ).convert_alpha()
        for block_data in self.level_config.get("poppable_block_locations", []):
            # Support both tuple (x, y) and dict formats
            if isinstance(block_data, (tuple, list)):
                x, y = block_data
                block_type = "disappear"  # Default type
                item_data = None
                custom_image = None
            else:
                x = block_data["x"]
                y = block_data["y"]
                block_type = block_data.get("type", "disappear")
                item_data = block_data.get("item", None)
                custom_image = block_data.get("image", None)

            # Load custom image if specified, otherwise use default
            if custom_image:
                poppable_block_image = pg.image.load(
                    os.path.join(IMAGEPATH, custom_image)
                ).convert_alpha()
            else:
                poppable_block_image = default_poppable_block_image

            pb = PoppableBlock(x, y, poppable_block_image, block_type, item_data, self)
            self.poppable_blocks.add(pb)
            # Only add to platforms (solid) immediately if not an invisible block
            if block_type != "invisible":
                self.platforms.add(pb)  # Add to platforms for collision detection
            else:
                # Invisible blocks should not be visible until popped - make image transparent
                try:
                    pb.image = pg.Surface((GRIDSIZE, GRIDSIZE), pg.SRCALPHA)
                except Exception:
                    pass
            self.all_sprites.add(pb)

        # Load gems (supports both new template-based and legacy format)
        for gem_data in self.level_config["gem_locations"]:
            # Handle both tuple (x, y) format and dict {'x': x, 'y': y, 'type': ...} format
            if isinstance(gem_data, (tuple, list)):
                x, y = gem_data
                # Use default gem image
                gem_id = f"{level_name}_gem_{x}_{y}"
                if gem_id in self.collected_items:
                    print(f"⏭️  Skipping already collected gem: {gem_id}")
                    continue  # Skip already collected gems
                print(f"💎 Loading gem at ({x}, {y}) - ID: {gem_id}")
                g = Gem(x, y, gem_image)
            else:
                x = gem_data["x"]
                y = gem_data["y"]
                gem_id = f"{level_name}_gem_{x}_{y}"
                if gem_id in self.collected_items:
                    print(f"⏭️  Skipping already collected gem: {gem_id}")
                    continue  # Skip already collected gems
                print(f"💎 Loading gem at ({x}, {y}) - ID: {gem_id}")
                # If gem has a 'type' field, load from config template
                if "type" in gem_data:
                    config = get_gem_config(gem_data["type"])
                    gem_img_path = os.path.join(IMAGEPATH, config["image"])
                    gem_img = pg.image.load(gem_img_path).convert_alpha()
                    g = Gem(x, y, gem_img)
                else:
                    g = Gem(x, y, gem_image)

            self.items.add(g)
            self.all_sprites.add(g)

            # Add ladders with tops
            # Support two formats for ladder_locations for backward compatibility:
            # 1) Flat list of (x,y) pairs (legacy) -> all but last are Ladder, last is LadderTop
            # 2) Nested list of ladders: [ [(x,y)...,(x,top)], [(x2,y)...,(x2,top)], ... ]
            if "ladder_locations" in self.level_config:
                ladders_cfg = self.level_config["ladder_locations"]
                # Detect nested format (list of lists/tuples)
                is_nested = (
                    isinstance(ladders_cfg, (list, tuple))
                    and len(ladders_cfg) > 0
                    and isinstance(ladders_cfg[0], (list, tuple))
                    and isinstance(ladders_cfg[0][0], (list, tuple))
                )

                if is_nested:
                    for ladder_list in ladders_cfg:
                        if not ladder_list:
                            continue
                        for x, y in ladder_list[:-1]:
                            ladder = Ladder(x, y)
                            self.all_sprites.add(ladder)
                            self.ladders.add(ladder)
                        # Last entry is top
                        x, y = ladder_list[-1]
                        ladder_top = LadderTop(x, y)
                        self.all_sprites.add(ladder_top)
                        self.ladder_tops.add(ladder_top)
                else:
                    # Legacy flat format
                    if len(ladders_cfg) >= 2:
                        for x, y in ladders_cfg[:-1]:
                            ladder = Ladder(x, y)
                            self.all_sprites.add(ladder)
                            self.ladders.add(ladder)
                        x, y = ladders_cfg[-1]
                        ladder_top = LadderTop(x, y)
                        self.all_sprites.add(ladder_top)
                        self.ladder_tops.add(ladder_top)
                    elif len(ladders_cfg) == 1:
                        # Single ladder top only
                        x, y = ladders_cfg[0]
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

        # Get custom player image if specified in level config
        player_image = self.level_config.get("player_image", None)
        
        # Create player with preserved state if provided
        if preserve_player_state:
            # Get the preserved max_health, or use default if not present
            max_health = preserve_player_state.get("max_health", 100)
            current_health = preserve_player_state.get("health", max_health)

            self.player = Player(
                spawn_x,
                spawn_y,
                world=self,
                start_gems=preserve_player_state.get("gems", 0),
                trophies_collected=preserve_player_state.get("trophies", 0),
                health=max_health,  # This sets max_health
                player_image=player_image,  # Apply custom image even when preserving state
                required_items=preserve_player_state.get("required_items", []),
            )
            # Set the actual current health separately
            self.player.health = current_health

            # Restore weapons
            if "weapons" in preserve_player_state:
                self.player.weapons = preserve_player_state["weapons"].copy()
                self.player.active_weapon = preserve_player_state.get("active_weapon")
                # Reload the weapon image so the sprite appears
                self.player.load_weapon_image()
            # Restore damage dealt
            self.player.damage_dealt = preserve_player_state.get("damage_dealt", 0)
        else:
            self.player = Player(spawn_x, spawn_y, world=self, player_image=player_image, required_items=[])

        self.player_sprite_group = pg.sprite.GroupSingle()
        self.player_sprite_group.add(self.player)
        self.all_sprites.add(self.player)

        # Show player start message if defined in level config (only on first load, not after sub-level)
        if (
            "player_start_message" in self.level_config
            and not is_sub_level_transition
            and not self.level_stack
        ):
            start_message = self.level_config["player_start_message"]
            start_color = self.level_config.get(
                "player_start_message_color", (255, 255, 255)
            )
            self.show_encounter_message(start_message, start_color)

        # Load enemies (supports both new template-based and legacy detailed configs)
        for enemy_data in self.level_config["enemy_locations"]:
            # If enemy has a 'type' field, load from config template
            if "type" in enemy_data:
                # New format: use enemy template with position and optional overrides
                config = get_enemy_config(
                    enemy_data["type"],
                    x=enemy_data["x"],
                    y=enemy_data["y"],
                    **{
                        k: v
                        for k, v in enemy_data.items()
                        if k not in ["type", "x", "y"]
                    },
                )
            else:
                # Legacy format: use data directly from level file
                config = enemy_data.copy()

            # Create unique enemy ID based on level name and position
            enemy_id = f"{level_name}_enemy_{config['x']}_{config['y']}"
            if enemy_id in self.killed_enemies:
                print(f"⏭️  Skipping already killed enemy: {enemy_id}")
                continue  # Skip already killed enemies

            print(
                f"👾 Loading enemy at ({config['x']}, {config['y']}) - ID: {enemy_id}"
            )

            enemy = Enemy(
                config["x"],
                config["y"],
                os.path.join(IMAGEPATH, config["image"]),
                config["speed"],
                config["patrol_range"],
                config.get("size_multiplier", 1),
                config.get("health", 1),
                config.get("damage", 1),
                config.get("shoot_range", 5),
                self,
                config.get("chase_range", 10),
                config.get("melee_damage", 5),
                config.get("can_throw_explosives", True),
                config.get("is_minion", False),
                config.get("can_summon_minions", False),
                config.get("encounter_message", None),
                config.get("shoot_cooldown", 60),
                config.get("spawn_on_death", None),
                config.get("drop_on_death", None),
                config.get("no_clip", False),
                config.get("encounter_message_color", None),
                config.get("explosive_image", None),
                config.get("explosive_size", 15),
            )
            # Store the enemy ID for tracking when killed
            enemy.enemy_id = enemy_id
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        # Load power-ups
        for powerup_data in self.level_config["powerup_locations"]:
            x = powerup_data["x"]
            y = powerup_data["y"]
            powerup_id = f"{level_name}_powerup_{x}_{y}"
            if powerup_id in self.collected_items:
                continue  # Skip already collected powerups
            powerup = PowerUp(
                x * GRIDSIZE,
                y * GRIDSIZE,
                powerup_data["type"],
                self,
            )
            self.all_sprites.add(powerup)
            self.powerups.add(powerup)

        # Load trophies (supports both new template-based and legacy format)
        self.trophies = pg.sprite.Group()
        default_trophy_image = self.level_config.get("trophy_image", "trophy.png")

        for trophy_data in self.level_config["trophy_locations"]:
            # Handle both tuple (x, y) format and dict {'x': x, 'y': y, 'type': ...} format
            if isinstance(trophy_data, (tuple, list)):
                x, y = trophy_data
                trophy_image = os.path.basename(default_trophy_image)
            else:
                x = trophy_data["x"]
                y = trophy_data["y"]
                # If trophy has a 'type' field, load from config template
                if "type" in trophy_data:
                    config = get_trophy_config(trophy_data["type"])
                    trophy_image = config["image"]
                else:
                    trophy_image = trophy_data.get(
                        "image", os.path.basename(default_trophy_image)
                    )

            trophy_id = f"{level_name}_trophy_{x}_{y}"
            if trophy_id in self.collected_items:
                continue  # Skip already collected trophies

            trophy = Trophy(x * GRIDSIZE, y * GRIDSIZE, trophy_image)
            self.trophies.add(trophy)
            self.all_sprites.add(trophy)

        # Set trophy count for this level
        # Check if total_trophies is manually specified in config (for dropped items, etc.)
        if "total_trophies" in self.level_config:
            current_level_trophy_count = self.level_config["total_trophies"]
        else:
            current_level_trophy_count = len(self.level_config["trophy_locations"])

        # Calculate global trophy count (parent + all sub-levels)
        if not self.level_stack:  # We're in the main/parent level
            # Calculate total trophies from parent and all sub-levels
            self.global_total_trophies = current_level_trophy_count

            # Add trophies from sub-levels
            for pipe_data in self.level_config.get("pipe_locations", []):
                sub_level_name = pipe_data["sub_level"]
                try:
                    sub_level_module = importlib.import_module(
                        f"platformer.levels.{sub_level_name}"
                    )
                    sub_level_config = sub_level_module.level_config
                    # Check if sub-level has manual trophy count
                    if "total_trophies" in sub_level_config:
                        self.global_total_trophies += sub_level_config["total_trophies"]
                    else:
                        self.global_total_trophies += len(
                            sub_level_config.get("trophy_locations", [])
                        )
                except Exception as e:
                    print(
                        f"⚠️ Could not load sub-level {sub_level_name} for trophy count: {e}"
                    )

            print(
                f"🏆 Global trophy count: {self.global_total_trophies} (parent: {current_level_trophy_count})"
            )

        # Use global trophy count for display
        self.total_trophies = (
            self.global_total_trophies
            if self.global_total_trophies > 0
            else current_level_trophy_count
        )

        # Load required items for exit (e.g., ["busticket", "key"])
        self.required_items_for_exit = self.level_config.get("required_items_for_exit", [])

        exit_x, exit_y = self.level_config["exit_location"]
        # Get custom exit images if specified in level config
        closed_image = self.level_config.get("exit_closed_image", "door_closed.png")
        open_image = self.level_config.get("exit_open_image", "door_open.png")
        exit_size = self.level_config.get("exit_size_multiplier", 2)
        self.exit = Exit(
            exit_x * GRIDSIZE, exit_y * GRIDSIZE, closed_image, open_image, exit_size
        )
        self.all_sprites.add(self.exit)

        # Load weapon pickups
        for weapon_data in self.level_config.get("weapon_locations", []):
            x = weapon_data["x"]
            y = weapon_data["y"]
            weapon_id = f"{level_name}_weapon_{x}_{y}"
            if weapon_id in self.collected_items:
                continue  # Skip already collected weapons
            weapon = WeaponPickup(
                x * GRIDSIZE,
                y * GRIDSIZE,
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
                # Go up from core/ to platformer/
                music_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    music_path,
                )
            self.original_music_track = music_path
            sound_manager.play_background_music(music_path)

        # Load alternative music tracks if specified
        if "alternative_music_tracks" in self.level_config:
            for alt_music_path in self.level_config["alternative_music_tracks"]:
                if not os.path.isabs(alt_music_path):
                    # Go up from core/ to platformer/
                    alt_music_path = os.path.join(
                        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        alt_music_path,
                    )

                if os.path.exists(alt_music_path):
                    self.alternative_music_tracks.append(alt_music_path)
                    print(
                        f"🎵 Loaded alternative music: {os.path.basename(alt_music_path)}"
                    )
                else:
                    print(f"❌ Alternative music not found: {alt_music_path}")

        # Load background image (preserve index if this is a sub-level transition)
        self.load_background_image(preserve_background_index=is_sub_level_transition)

        # Restore parent background index if returning from sub-level
        if is_sub_level_transition and hasattr(self, "parent_background_index"):
            self.current_background_index = self.parent_background_index
            print(f"🎨 Restored background index: {self.current_background_index}")
            # Apply the saved background immediately
            if self.current_background_index > 0 and self.alternative_backgrounds:
                if self.current_background_index - 1 < len(
                    self.alternative_backgrounds
                ):
                    self.background_image = self.alternative_backgrounds[
                        self.current_background_index - 1
                    ]
                    print(
                        f"🎨 Applied alternative background {self.current_background_index}"
                    )

            # Restore parent music track if returning from sub-level
            if hasattr(self, "parent_music_track") and self.parent_music_track:
                sound_manager.play_background_music(self.parent_music_track)
                print(
                    f"🎵 Restored parent music: {os.path.basename(self.parent_music_track)}"
                )

        # Load common sound effects (if they exist)
        self.load_sound_effects()

    def reset(self):
        """Reset the current level to initial state while preserving player progress."""
        if not self.current_level_name:
            return

        # Save player gems and trophies before reset
        player_state = {
            "gems": self.player.gems,
            "trophies": self.player.trophies_collected,
            "health": self.player.max_health,  # Reset to full health
            "max_health": self.player.max_health,
            "weapons": (
                self.player.weapons.copy() if hasattr(self.player, "weapons") else {}
            ),
            "active_weapon": getattr(self.player, "active_weapon", None),
        }

        # Always preserve the timer during reset (whether in parent or sub-level)
        # This ensures the timer continues from where it left off
        if self.time_remaining is not None:
            self.parent_time_remaining = self.time_remaining
            if self.level_stack:
                print(
                    f"⏱️ Preserving timer during sub-level reset: {self.time_remaining:.1f}s"
                )
            else:
                print(
                    f"⏱️ Preserving timer during parent level reset: {self.time_remaining:.1f}s"
                )

        # Preserve background and music state during reset
        saved_background_index = self.current_background_index
        saved_music_track = (
            sound_manager.current_music_file
            if hasattr(sound_manager, "current_music_file")
            else None
        )
        print(f"🎨 Preserving background index during reset: {saved_background_index}")
        print(f"🎵 Preserving music track during reset: {saved_music_track}")

        # Reload the current level with preserved player state
        # Mark as sub-level transition if we're in a sub-level to preserve killed enemies/items
        self.load_level(
            self.current_level_name,
            preserve_player_state=player_state,
            is_sub_level_transition=bool(self.level_stack),  # True if in sub-level
        )

        # Restore background and music after reset
        if saved_background_index > 0 and self.alternative_backgrounds:
            self.current_background_index = saved_background_index
            if saved_background_index - 1 < len(self.alternative_backgrounds):
                self.background_image = self.alternative_backgrounds[
                    saved_background_index - 1
                ]
                print(
                    f"🎨 Restored background index after reset: {saved_background_index}"
                )

        if saved_music_track:
            sound_manager.play_background_music(saved_music_track)
            print(
                f"🎵 Restored music after reset: {os.path.basename(saved_music_track)}"
            )

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
                            self.marvin_mode_ever_used = True  # Mark cheat as used
                            print("🎮 MARVIN MODE ACTIVATED! 🎮")
                            sound_manager.play_sound_effect("powerup_collect")
                        else:
                            print("🎮 Marvin Mode deactivated")

                # Game controls
                if event.key == pg.K_f:  # Shoot
                    self.player.start_shoot()
                elif event.key == pg.K_g:  # Melee attack
                    self.player.melee_attack()
                elif event.key == pg.K_e:
                    self.player.throw_exploding_object()
            elif event.type == pg.KEYUP:
                # Stop continuous spray when F key is released
                if event.key == pg.K_f:
                    self.player.stop_shoot()

    async def level_complete(self):
        # If a sub-level exit was reached and that sub-level requested the
        # parent to be finished instead of returning to it, handle that first.
        if getattr(self, "_finish_parent_on_exit", False) and self.level_stack:
            # Prepare to finish the parent level (the parent info is the
            # last element pushed onto level_stack in enter_sub_level()).
            parent_level = self.level_stack[-1]
            parent_name = parent_level.get("level_name")

            try:
                parent_module = importlib.import_module(f"platformer.levels.{parent_name}")
                parent_config = parent_module.level_config

                if "total_trophies" in parent_config:
                    total = parent_config["total_trophies"]
                else:
                    total = len(parent_config.get("trophy_locations", []))

                for pipe_data in parent_config.get("pipe_locations", []):
                    sub_name = pipe_data.get("sub_level")
                    try:
                        sub_mod = importlib.import_module(f"platformer.levels.{sub_name}")
                        sub_cfg = sub_mod.level_config
                        if "total_trophies" in sub_cfg:
                            total += sub_cfg["total_trophies"]
                        else:
                            total += len(sub_cfg.get("trophy_locations", []))
                    except Exception:
                        pass

                # Use parent's name and trophy count for scoring and treat
                # this as a top-level completion (clear the level stack).
                self.current_level_name = parent_name
                self.global_total_trophies = total
                self.total_trophies = total if total > 0 else 0
                self.level_stack.clear()
                print(f"🏁 Sub-level exit finishing parent level: {parent_name} (trophies={total})")
            except Exception as e:
                print(f"⚠️ Could not prepare parent level completion: {e}")
                # Fallback to normal behaviour: return to parent
                self._finish_parent_on_exit = False
                self.exit_sub_level()
                return

            # Clear the flag so normal completion proceeds as a parent-level finish
            self._finish_parent_on_exit = False

        # Check if we're in a sub-level
        if self.level_stack:
            # Return to parent level
            self.exit_sub_level()
            return

        # Otherwise, normal level completion
        await fade_to_black(
            screen=self.screen,
            draw_callback=self.draw,
            width=WIDTH,
            height=HEIGHT,
            duration=60,
        )

        # Check if player used cheat mode
        if self.marvin_mode_ever_used:
            # Show cheat screen instead of highscore
            await self.show_cheat_screen()
            # Return to level selection
            self.keep_going = False
            self.return_to_level_selection = True
            return

        # Calculate final score
        time_remaining = self.time_remaining if self.time_remaining else 0
        score_breakdown = self.highscore_manager.calculate_score(
            time_remaining=time_remaining,
            trophies_collected=self.player.trophies_collected,
            damage_dealt=self.player.damage_dealt,
            lives_remaining=self.player.gems,
        )

        # Show level complete and score
        await self.show_level_complete_with_score(score_breakdown)

        # Prompt for player name and save highscore
        player_name = await self.prompt_player_name()
        if player_name:
            result = self.highscore_manager.add_highscore(
                self.current_level_name, player_name, score_breakdown
            )
            # Handle both sync and async results
            if self.highscore_manager.use_http:
                await result
            print(
                f"💾 Highscore saved for {player_name}: {score_breakdown['total_score']:,}"
            )

        # Show top 5 highscores
        await self.show_highscores()

        # Wait until the user closes the window or presses any key
        waiting = True
        user_quit = False
        while waiting:
            await asyncio.sleep(0)  # Yield control to browser
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

        # Save current background state
        self.parent_background_index = self.current_background_index
        print(f"🎨 Saving parent background index: {self.current_background_index}")

        # Save current music state
        self.parent_music_track = (
            sound_manager.current_music_file
            if hasattr(sound_manager, "current_music_file")
            else None
        )
        print(f"🎵 Saving parent music track: {self.parent_music_track}")

        # Save current level state
        player_state = {
            "gems": self.player.gems,
            "trophies": self.player.trophies_collected,
            "health": self.player.health,
            "max_health": self.player.max_health,
            "weapons": (
                self.player.weapons.copy() if hasattr(self.player, "weapons") else {}
            ),
            "active_weapon": getattr(self.player, "active_weapon", None),
            "damage_dealt": getattr(self.player, "damage_dealt", 0),
            "required_items": getattr(self.player, "required_items", []).copy() if hasattr(self.player, "required_items") else [],
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

        # Load the sub-level (preserve player state and mark as sub-level transition)
        self.load_level(
            pipe.sub_level_name,
            preserve_player_state=player_state,
            is_sub_level_transition=True,
        )

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
            "max_health": self.player.max_health,
            "weapons": (
                self.player.weapons.copy() if hasattr(self.player, "weapons") else {}
            ),
            "active_weapon": getattr(self.player, "active_weapon", None),
            "damage_dealt": getattr(self.player, "damage_dealt", 0),
            "required_items": getattr(self.player, "required_items", []).copy() if hasattr(self.player, "required_items") else [],
        }

        # Set parent_time_remaining before loading so load_level can use it
        if current_time is not None:
            self.parent_time_remaining = current_time
            print(f"⏱️ Timer will continue: {current_time:.1f}s remaining")

        # Load parent level with return position, updated state, and mark as sub-level transition
        self.load_level(
            parent_level["level_name"],
            player_spawn_override=parent_level["return_position"],
            preserve_player_state=current_state,
            is_sub_level_transition=True,
        )

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

        # Update poppable blocks
        for poppable_block in self.poppable_blocks:
            poppable_block.update()

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
        draw_background(
            self.screen,
            self.background_image,
            self.background_scroll_speed,
            self.camera_offset_x,
            self.camera_offset_y,
            self.level_config.get("background_color", (135, 206, 235)),
        )

        # Draw all sprites with the camera offset
        for sprite in self.all_sprites:
            if sprite != self.player:
                offset_rect = sprite.rect.move(
                    -self.camera_offset_x, -self.camera_offset_y
                )
                self.screen.blit(sprite.image, offset_rect)

        # Draw player with weapon
        self.player.draw(self.screen, self.camera_offset_x, self.camera_offset_y)

        # Apply pixelation effect if active
        if self.player.radial_blur_active:
            self._apply_pixelation()

        # Draw enemy health bars
        for enemy in self.enemies:
            enemy.draw_health_bar(
                self.screen, self.camera_offset_x, self.camera_offset_y
            )

        # Draw HUD
        draw_gems(self.screen, self.player)
        trophy_image = self.level_config.get("trophy_image", "trophy.png")
        draw_trophies(self.screen, self.player, self.total_trophies, trophy_image)
        draw_health_bar(self.screen, self.player, 200, 20, self.player.max_health)

        # Draw encounter message (if active)
        if self.encounter_message_timer > 0 and self.encounter_message:
            draw_encounter_message(
                self.screen,
                self.encounter_message,
                WIDTH,
                HEIGHT,
                self.encounter_message_color,
            )
            self.encounter_message_timer -= 1

        # Draw timer (top right corner)
        draw_timer(self.screen, self.time_remaining, WIDTH)

        # Draw score (bottom right corner)
        self.update_current_score()
        draw_score(self.screen, self.current_score, WIDTH)

        # Draw Marvin Mode indicator
        if self.marvin_mode:
            draw_marvin_mode(self.screen, WIDTH)

        pg.display.flip()

    def update_current_score(self):
        """Update the current score based on game state (excluding time bonus)."""
        # Don't include time remaining in the running score - only add it at level completion
        score_breakdown = self.highscore_manager.calculate_score(
            time_remaining=0,  # Time bonus only added at the end
            trophies_collected=self.player.trophies_collected,
            damage_dealt=self.player.damage_dealt,
            lives_remaining=self.player.gems,
        )
        self.current_score = score_breakdown["total_score"]

    async def show_level_complete_with_score(self, score_breakdown):
        """Display level complete with score breakdown."""
        self.screen.fill((0, 0, 0))

        # Title
        font_title = pg.font.Font(None, 48)
        title_text = font_title.render("Level Complete!", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, 20))
        self.screen.blit(title_text, title_rect)

        # Score breakdown
        font_normal = pg.font.Font(None, 28)
        y_offset = 60
        line_spacing = 32

        breakdown_lines = [
            f"Time Bonus: {score_breakdown['time_score']:,}",
            f"Trophy Bonus: {score_breakdown['trophy_score']:,}",
            f"Damage Bonus: {score_breakdown['damage_score']:,}",
            f"Lives Bonus: {score_breakdown['life_score']:,}",
            "",
            f"TOTAL SCORE: {score_breakdown['total_score']:,}",
        ]

        for i, line in enumerate(breakdown_lines):
            if line == "":
                continue
            color = (255, 215, 0) if "TOTAL" in line else (255, 255, 255)
            text = font_normal.render(line, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, y_offset + i * line_spacing))
            self.screen.blit(text, text_rect)

        # Draw instruction at bottom
        instruction_font = pg.font.Font(None, 24)
        instruction = instruction_font.render(
            "Press any key to continue", True, (200, 200, 200)
        )
        instruction_rect = instruction.get_rect(center=(WIDTH // 2, HEIGHT - 15))
        self.screen.blit(instruction, instruction_rect)

        pg.display.flip()

        # Wait for key press
        waiting = True
        while waiting:
            await asyncio.sleep(0)  # Yield control to browser
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                elif event.type == pg.KEYDOWN:
                    waiting = False
            self.clock.tick(60)

    async def prompt_player_name(self):
        """Prompt player to enter their name for highscore."""
        font_title = pg.font.Font(None, 40)
        font_input = pg.font.Font(None, 36)
        player_name = ""
        cursor_visible = True
        cursor_timer = 0

        entering_name = True
        while entering_name:
            await asyncio.sleep(0)  # Yield control to browser
            # Handle cursor blinking
            cursor_timer += 1
            if cursor_timer >= 30:  # Blink every 30 frames (0.5 seconds at 60 FPS)
                cursor_visible = not cursor_visible
                cursor_timer = 0

            # Draw prompt
            self.screen.fill((0, 0, 0))

            title_text = font_title.render("Enter Your Name:", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
            self.screen.blit(title_text, title_rect)

            # Draw input box
            input_text = player_name + ("|" if cursor_visible else " ")
            input_surface = font_input.render(input_text, True, (255, 215, 0))
            input_rect = input_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))

            # Draw box background
            box_rect = input_rect.inflate(30, 15)
            pg.draw.rect(self.screen, (50, 50, 50), box_rect)
            pg.draw.rect(self.screen, (255, 255, 255), box_rect, 2)

            self.screen.blit(input_surface, input_rect)

            # Draw instruction
            instruction_font = pg.font.Font(None, 24)
            instruction = instruction_font.render(
                "Press ENTER to continue", True, (200, 200, 200)
            )
            instruction_rect = instruction.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 100)
            )
            self.screen.blit(instruction, instruction_rect)

            pg.display.flip()
            self.clock.tick(60)

            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return None
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        entering_name = False
                    elif event.key == pg.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.key == pg.K_ESCAPE:
                        return None
                    elif len(player_name) < 20:  # Limit name length
                        if event.unicode.isprintable():
                            player_name += event.unicode

        return player_name if player_name else "Anonymous"

    async def show_highscores(self):
        """Display top 5 highscores for the current level."""
        result = self.highscore_manager.get_top_scores(self.current_level_name, limit=5)
        # Handle both sync and async results
        if self.highscore_manager.use_http:
            top_scores = await result
        else:
            top_scores = result

        self.screen.fill((0, 0, 0))

        # Title
        font_title = pg.font.Font(None, 48)
        title_text = font_title.render("TOP 5 HIGHSCORES", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(WIDTH // 2, 20))
        self.screen.blit(title_text, title_rect)

        # Highscore list
        font_score = pg.font.Font(None, 28)
        y_offset = 60
        line_spacing = 32

        if not top_scores:
            no_scores_text = font_score.render(
                "No highscores yet!", True, (255, 255, 255)
            )
            no_scores_rect = no_scores_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(no_scores_text, no_scores_rect)
        else:
            for i, entry in enumerate(top_scores):
                rank = i + 1
                name = entry["player_name"]
                score = entry["score"]

                # Truncate long names to fit in 20 character field
                if len(name) > 20:
                    name = name[:17] + "..."

                line_text = f"{rank}. {name: <20} {score:>10,}"
                color = (255, 255, 255)

                text = font_score.render(line_text, True, color)
                text_rect = text.get_rect(
                    center=(WIDTH // 2, y_offset + i * line_spacing)
                )
                self.screen.blit(text, text_rect)

        # Instruction
        instruction_font = pg.font.Font(None, 24)
        instruction = instruction_font.render(
            "Press any key to continue", True, (200, 200, 200)
        )
        instruction_rect = instruction.get_rect(center=(WIDTH // 2, HEIGHT - 15))
        self.screen.blit(instruction, instruction_rect)

        pg.display.flip()
        await asyncio.sleep(0)  # Yield control to browser

    async def show_cheat_screen(self):
        """Display cheat screen when player used marvin mode."""
        self.screen.fill((0, 0, 0))

        # Title
        font_title = pg.font.Font(None, 72)
        title_text = font_title.render("You cheated.", True, (255, 165, 0))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        self.screen.blit(title_text, title_rect)

        # Message
        font_message = pg.font.Font(None, 36)
        message_text = font_message.render(
            "No highscore for you...", True, (255, 255, 255)
        )
        message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        self.screen.blit(message_text, message_rect)

        # Instruction
        instruction_font = pg.font.Font(None, 24)
        instruction = instruction_font.render(
            "Press any key to return to level selection", True, (200, 200, 200)
        )
        instruction_rect = instruction.get_rect(center=(WIDTH // 2, HEIGHT - 15))
        self.screen.blit(instruction, instruction_rect)

        pg.display.flip()

        # Wait for key press
        waiting = True
        while waiting:
            await asyncio.sleep(0)  # Yield control to browser
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                elif event.type == pg.KEYDOWN:
                    waiting = False
            self.clock.tick(60)

    async def show_game_over_screen(self):
        """Display game over screen."""
        self.screen.fill((0, 0, 0))

        # Title
        font_title = pg.font.Font(None, 72)
        title_text = font_title.render("GAME OVER", True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        self.screen.blit(title_text, title_rect)

        # Message - use level-specific message if configured
        game_over_message = self.level_config.get(
            "game_over_message",
            "Better luck next time! No highscore for you..."
        )
        game_over_message_color = self.level_config.get(
            "game_over_message_color",
            (255, 255, 255)  # Default: White
        )
        
        font_message = pg.font.Font(None, 32)
        # Handle multi-line messages
        message_lines = game_over_message.split('\n')
        y_offset = HEIGHT // 2 + 20
        for line in message_lines:
            message_text = font_message.render(line, True, game_over_message_color)
            message_rect = message_text.get_rect(center=(WIDTH // 2, y_offset))
            self.screen.blit(message_text, message_rect)
            y_offset += 40  # Space between lines

        # Instruction
        instruction_font = pg.font.Font(None, 24)
        instruction = instruction_font.render(
            "Press any key to return to level selection", True, (200, 200, 200)
        )
        instruction_rect = instruction.get_rect(center=(WIDTH // 2, HEIGHT - 15))
        self.screen.blit(instruction, instruction_rect)

        pg.display.flip()

        # Wait for key press
        waiting = True
        while waiting:
            await asyncio.sleep(0)  # Yield control to browser
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.return_to_level_selection = (
                        False  # User wants to quit entirely
                    )
                elif event.type == pg.KEYDOWN:
                    waiting = False
            self.clock.tick(60)

    def show_encounter_message(self, message, color=None):
        """Display an encounter message when player first sees an enemy."""
        self.encounter_message = message
        self.encounter_message_color = color  # Store custom color
        self.encounter_message_timer = self.encounter_message_duration

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
        # Go up from core/ to platformer/
        sounds_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets",
            "sounds",
        )
        for name, filename in sound_effects.items():
            full_path = os.path.join(sounds_dir, filename)
            sound_manager.load_sound_effect(name, full_path)

    def load_background_image(self, preserve_background_index=False):
        """Load level-specific background image.

        Args:
            preserve_background_index: If True, keep the current background index (for sub-level transitions)
        """
        saved_index = self.current_background_index if preserve_background_index else 0

        self.background_image = None
        self.background_scroll_speed = 1  # Default parallax scroll speed
        self.alternative_backgrounds = []  # Reset alternative backgrounds
        self.current_background_index = saved_index

        # Load background scroll speed from config (applies to all backgrounds)
        if "background_scroll_speed" in self.level_config:
            self.background_scroll_speed = self.level_config["background_scroll_speed"]
            print(f"🎨 Background scroll speed set to: {self.background_scroll_speed}")

        if (
            "background_image" in self.level_config
            and self.level_config["background_image"]
        ):
            bg_path = self.level_config["background_image"]

            # Check if it's an absolute path or relative to platformer directory
            if not os.path.isabs(bg_path):
                # Try relative to platformer directory (where assets now lives)
                # Go up from core/ to platformer/
                bg_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), bg_path
                )

            # Load background image
            if os.path.exists(bg_path):
                try:
                    self.background_image = pg.image.load(bg_path).convert()
                    print(f"🖼️ Loaded background image: {os.path.basename(bg_path)}")

                except pg.error as e:
                    print(f"❌ Error loading background image: {e}")
                    self.background_image = None
            else:
                print(f"❌ Background image not found: {bg_path}")

        # Load alternative backgrounds if specified
        if "alternative_backgrounds" in self.level_config:
            for alt_bg_path in self.level_config["alternative_backgrounds"]:
                if not os.path.isabs(alt_bg_path):
                    # Go up from core/ to platformer/
                    alt_bg_path = os.path.join(
                        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        alt_bg_path,
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
                # Reset debug flag so we see the new background's position
                if hasattr(self, "_bg_debug_shown"):
                    delattr(self, "_bg_debug_shown")
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

    def _apply_pixelation(self):
        """Apply pixelation/rasterization effect to the entire screen."""
        # Use a stronger pixelation factor if the player has a joint-specific override
        factor = getattr(self.player, "joint_pixelation_factor", PIXELATION_FACTOR)
        # Downscale the screen by the selected factor
        small_width = max(1, WIDTH // factor)
        small_height = max(1, HEIGHT // factor)

        # Create a small surface with the downscaled image
        small_surface = pg.transform.scale(self.screen, (small_width, small_height))

        # Scale it back up to original size without smoothing (creates pixelated look)
        pixelated_surface = pg.transform.scale(small_surface, (WIDTH, HEIGHT))

        # Blit the pixelated version back to the screen
        self.screen.blit(pixelated_surface, (0, 0))

    def reset_fps(self):
        """Reset FPS to default value."""
        self.current_fps = FPS
        print(f"🕐 FPS reset to {FPS}")

    def on_timer_expired(self):
        """Called when the level timer reaches zero."""
        print("⏱️ Timer expired! Game Over")
        
        # Get custom game over message from level config
        timeout_message = self.level_config.get(
            "timeout_message", 
            "Time's up!"
        )
        timeout_message_color = self.level_config.get(
            "timeout_message_color",
            (255, 0, 0)  # Default: Red
        )
        
        # Display the timeout message
        self.show_encounter_message(timeout_message, timeout_message_color)
        
        # Set game over flag
        self.game_over_flag = True

    def start_screen(self):
        """Hook for displaying start screen. Currently unused."""
        pass

    def loose_screen(self):
        """Called when player loses a life. Stores gems for reset."""
        self.player_gems = self.player.gems

    async def game_over(self):
        """Called when game is over. Returns to level selection screen."""
        print("Game Over! Returning to level selection...")

        # Display game over screen
        await fade_to_black(
            screen=self.screen,
            draw_callback=self.draw,
            width=WIDTH,
            height=HEIGHT,
            duration=60,
        )

        # Show game over message
        await self.show_game_over_screen()

        # Set flags to return to level selection
        self.keep_going = False
        self.return_to_level_selection = True
