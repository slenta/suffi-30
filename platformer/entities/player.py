"""Player character class with movement, combat, and interaction."""

import pygame as pg
import os
import math
import random
from ..config.settings import (
    IMAGEPATH,
    GRIDSIZE,
    PLAYER_SPEED,
    JUMP_POWER,
    GRAVITY,
    MAX_VELOCITY,
    KEYBINDINGS,
)
from .bullet import Bullet, ExplodingObject, SprayStream
from ..core.sound_manager import sound_manager
from ..config.weapon_config import WEAPON_CONFIG
from ..config.constants import (
    PLAYER_KNOCKBACK_DISTANCE,
    PLAYER_KNOCKBACK_TIMER,
    PLAYER_KNOCKBACK_STEPS,
    PLAYER_KNOCKBACK_LIFT,
    SPIKE_KNOCKBACK_DISTANCE,
    SPIKE_DAMAGE_COOLDOWN,
    EXPLODING_OBJECT_COOLDOWN,
    EXPLODING_OBJECT_DAMAGE,
    LADDER_MOVE_SPEED,
    WATERFALL_MOVE_SPEED,
    MELEE_ATTACK_DURATION,
    WEAPON_SCALE_FACTOR,
    FALL_DEATH_THRESHOLD,
    FALL_SEARCH_RANGE,
)


class Player(pg.sprite.Sprite):
    """Player character with movement, combat, and world interaction."""

    def __init__(self, _x, _y, world, start_gems=0, trophies_collected=0, health=80):
        super().__init__()
        # Load and scale the player image to fit within one grid cell
        original_image = pg.image.load(
            os.path.join(IMAGEPATH, "player/suffi.png")
        ).convert_alpha()
        # Scale to GRIDSIZE (18x18 pixels for size of 1)
        self.image = pg.transform.scale(original_image, (2 * GRIDSIZE, 2 * GRIDSIZE))
        self.rect = self.image.get_rect()
        self.rect.x = _x * GRIDSIZE
        self.rect.bottom = _y * GRIDSIZE
        self.speed = PLAYER_SPEED
        self.jump_power = JUMP_POWER
        self.vx = 0
        self.vy = 0
        self.gems = start_gems
        self.max_health = health  # Maximum health
        self.health = health  # Current health
        self.world = world
        self.knockback_timer = 0  # Timer to track incapacitation
        self.is_knocked_back = False  # Flag to indicate knockback state
        self.knockback_animation_steps = 0  # Counter for knockback animation
        self.knockback_step_distance = 0  # Distance per knockback step
        self.active_powerups = {}
        self.trophies_collected = trophies_collected
        self.weapons = {}  # {weapon_name: cooldown_timer}
        self.active_weapon = None
        self.weapon_image = None
        self.weapon_rect = None
        # Active spray stream (if using continuous spray weapons)
        self.spray_stream = None
        self.controls_reversed = False
        self.spike_damage_cooldown = 0
        self.exploding_object_cooldown = EXPLODING_OBJECT_COOLDOWN
        self.damage_dealt = 0  # Track total damage dealt to enemies
        self.radial_blur_active = False  # Track if radial blur effect is active

        # Ladder mechanics
        self.on_ladder = False
        self.ladder_grip = False
        self.ladder_move_speed = LADDER_MOVE_SPEED

        # Waterfall mechanics
        self.in_waterfall = False
        self.waterfall_grip = False
        self.waterfall_move_speed = WATERFALL_MOVE_SPEED

        # Melee attack animation
        self.is_attacking = False
        self.attack_frame = 0
        self.attack_duration = MELEE_ATTACK_DURATION

    def jump(self):
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.world.platforms, False)
        self.rect.y -= 2
        if len(hits) > 0:
            self.vy = -1 * self.jump_power
            sound_manager.play_sound_effect("jump")  # Play jump sound

    def apply_gravity(self):
        # Only apply gravity when not gripping a ladder
        if not self.ladder_grip:
            self.vy += GRAVITY
            if self.vy > MAX_VELOCITY:
                self.vy = MAX_VELOCITY

    def move(self):
        keys = pg.key.get_pressed()

        # Handle horizontal movement (with potential reversal)
        left_pressed = keys[KEYBINDINGS.get("left")]
        right_pressed = keys[KEYBINDINGS.get("right")]

        # Swap left/right if controls are reversed
        if self.controls_reversed:
            left_pressed, right_pressed = right_pressed, left_pressed

        if left_pressed:
            self.vx = -1 * self.speed
        elif right_pressed:
            self.vx = self.speed
        else:
            self.vx = 0

        # Handle jumping independently of horizontal movement
        if keys[KEYBINDINGS.get("jump")]:
            self.jump()

        # Check if standing on a moving platform BEFORE movement
        # This needs to happen before any position changes
        standing_on_platform = None
        self.rect.y += 2  # Check slightly below
        platform_hits = pg.sprite.spritecollide(
            self, self.world.moving_platforms, False
        )
        self.rect.y -= 2  # Restore position
        if platform_hits:
            standing_on_platform = platform_hits[0]

        # Horizontal collision
        self.rect.x += self.vx
        hits = pg.sprite.spritecollide(self, self.world.platforms, False)
        for hit in hits:
            # Skip collision with platform we're standing on to avoid side collision issues
            if hit == standing_on_platform:
                continue
            if self.vx > 0:
                self.rect.right = hit.rect.left
            elif self.vx < 0:
                self.rect.left = hit.rect.right

        # Vertical collision
        self.rect.y += self.vy
        # Special-case: check for invisible poppable blocks (not yet added to platforms)
        # when the player is moving upward (vy < 0). These blocks should react when
        # hit from below even though they are not solid yet.
        if self.vy < 0:
            inv_hits = [b for b in pg.sprite.spritecollide(self, self.world.poppable_blocks, False) if b not in self.world.platforms]
            for hit in inv_hits:
                # Treat as a collision from below: stop upward movement and trigger pop
                self.rect.top = hit.rect.bottom
                try:
                    hit.pop()
                except Exception:
                    pass
                sound_manager.play_sound_effect("enemy_hit")
                self.vy = 0
                break
        hits = pg.sprite.spritecollide(self, self.world.platforms, False)
        for hit in hits:
            if self.vy > 0:
                self.rect.bottom = hit.rect.top
                standing_on_platform = (
                    hit if hit in self.world.moving_platforms else standing_on_platform
                )
            elif self.vy < 0:
                self.rect.top = hit.rect.bottom
                # Check if this is a poppable block
                if hit in self.world.poppable_blocks:
                    hit.pop()
                    sound_manager.play_sound_effect("enemy_hit")  # Play pop sound
            self.vy = 0

        # Apply moving platform velocity if standing on one
        # This happens AFTER all collision resolution
        if standing_on_platform and standing_on_platform in self.world.moving_platforms:
            vel_x, vel_y = standing_on_platform.get_velocity()
            self.rect.x += vel_x
            # Don't apply vertical velocity if player is on top (would cause bouncing)
            # But apply it for checking if still on platform

        # Check if player has fallen too far below the nearest platform
        self.check_fall_death()

    def check_fall_death(self):
        """Check if player has fallen too far below the nearest platform."""
        nearest_platform_bottom = None
        search_range = GRIDSIZE * FALL_SEARCH_RANGE

        for platform in self.world.platforms:
            if abs(platform.rect.centerx - self.rect.centerx) <= search_range:
                if platform.rect.top >= self.rect.top:
                    if (
                        nearest_platform_bottom is None
                        or platform.rect.top < nearest_platform_bottom
                    ):
                        nearest_platform_bottom = platform.rect.top

        if nearest_platform_bottom is not None:
            death_threshold = nearest_platform_bottom + GRIDSIZE * FALL_DEATH_THRESHOLD
            if self.rect.top > death_threshold:
                self.loose()
        else:
            if self.rect.y > self.world.top + GRIDSIZE * FALL_DEATH_THRESHOLD:
                self.loose()

    def check_edges(self):
        left_edge = self.world.ground_start
        right_edge = self.world.ground_end
        if self.rect.left < left_edge:
            self.rect.left = left_edge
        elif self.rect.right > right_edge:
            self.rect.right = right_edge

    def check_items(self):
        hits = pg.sprite.spritecollide(self, self.world.items, True)
        for item in hits:
            # Track collected item to prevent respawning
            item_x = item.rect.centerx // GRIDSIZE
            item_y = item.rect.centery // GRIDSIZE
            gem_id = f"{self.world.current_level_name}_gem_{item_x}_{item_y}"
            self.world.collected_items.add(gem_id)
            print(f"💎 Collected gem at ({item_x}, {item_y}) - ID: {gem_id}")
            print(f"📋 Currently collected items: {self.world.collected_items}")
            item.apply(self)
            sound_manager.play_sound_effect("gem_collect")  # Play gem collection sound

    def check_powerups(self):
        hits = pg.sprite.spritecollide(self, self.world.powerups, True)
        for powerup in hits:
            # Track collected powerup to prevent respawning
            powerup_x = powerup.rect.centerx // GRIDSIZE
            powerup_y = powerup.rect.centery // GRIDSIZE
            self.world.collected_items.add(
                f"{self.world.current_level_name}_powerup_{powerup_x}_{powerup_y}"
            )
            powerup.apply_effect(self)
            # Type 3 powerup lasts 4 seconds (240 frames), type 5 lasts 15 seconds (900 frames), others last 8 seconds (480 frames)
            if powerup.power_type == 3:
                from ..config.constants import POWERUP_CHAOS_DURATION

                duration = random.randint(
                    POWERUP_CHAOS_DURATION // 2, POWERUP_CHAOS_DURATION
                )
            elif powerup.power_type == 5:
                from ..config.constants import PIXELATION_DURATION

                duration = random.randint(PIXELATION_DURATION // 2, PIXELATION_DURATION)
            else:
                duration = 480
            self.active_powerups[powerup.power_type] = [duration, powerup]
            sound_manager.play_sound_effect(
                "powerup_collect"
            )  # Play powerup collection sound

    def check_trophies(self):
        hits = pg.sprite.spritecollide(self, self.world.trophies, True)
        if len(hits) > 0:
            sound_manager.play_sound_effect(
                "trophy_collect"
            )  # Play trophy collection sound
        for trophy in hits:
            # Track collected trophy to prevent respawning
            trophy_x = trophy.rect.centerx // GRIDSIZE
            trophy_y = trophy.rect.centery // GRIDSIZE
            self.world.collected_items.add(
                f"{self.world.current_level_name}_trophy_{trophy_x}_{trophy_y}"
            )
        self.trophies_collected += len(hits)

    def check_exit(self):
        # If the current level has no exit (e.g., parent level delegates finishing to a sub-level), do nothing
        if not getattr(self.world, "exit", None):
            return

        # Exit is always open - no need to collect all trophies
        try:
            self.world.exit.open()
        except Exception:
            return

        if pg.sprite.collide_rect(self, self.world.exit):
            sound_manager.play_sound_effect("level_complete")
            self.world.level_complete_flag = True

    def check_pipes(self):
        """Check if player is trying to enter a pipe."""
        keys = pg.key.get_pressed()

        for pipe in self.world.pipes:
            if pipe.can_enter(self, keys):
                # Enter the sub-level
                self.world.enter_sub_level(pipe)
                break

    def check_spikes(self):
        """Check if player collides with spikes and take damage."""
        # Invincible in marvin mode
        if self.world.marvin_mode:
            return

        # Decrease spike damage cooldown
        if self.spike_damage_cooldown > 0:
            self.spike_damage_cooldown -= 1
            return

        for spike in self.world.spikes:
            if spike.check_collision(self):
                # Take damage from the spike
                self.take_damage(spike.damage)
                self.apply_spike_knockback(spike)
                self.spike_damage_cooldown = SPIKE_DAMAGE_COOLDOWN
                break

    def apply_spike_knockback(self, spike):
        """Apply knockback effect when hit by spikes."""
        if not self.is_knocked_back:
            self.is_knocked_back = True
            self.knockback_timer = 20

            knockback_distance = GRIDSIZE * SPIKE_KNOCKBACK_DISTANCE

            # Push player in opposite direction of spike
            if spike.direction == "up":
                # Spikes point up, push player up
                self.rect.y -= knockback_distance
            elif spike.direction == "down":
                # Spikes point down, push player down
                self.rect.y += knockback_distance
            elif spike.direction == "left":
                # Spikes point left, push player left
                self.rect.x -= knockback_distance
            elif spike.direction == "right":
                # Spikes point right, push player right
                self.rect.x += knockback_distance

    def handle_powerup_timers(self):
        expired = []
        for ptype in self.active_powerups:
            self.active_powerups[ptype][0] -= 1
            if self.active_powerups[ptype][0] <= 0:
                # Timer expired, power down and mark for removal
                self.active_powerups[ptype][1].power_down(self)
                expired.append(ptype)
        for ptype in expired:
            del self.active_powerups[ptype]

    def take_damage(self, damage):
        # Invincible in marvin mode
        if self.world.marvin_mode:
            return

        sound_manager.play_sound_effect("player_hurt")  # Play hurt sound
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.loose()  # Call the loose function when health is 0

    def loose(self):
        # In marvin mode, respawn without losing a life
        if self.world.marvin_mode:
            self.world.reset()
            return

        sound_manager.play_sound_effect("player_death")  # Play death/fall sound
        if self.gems >= 1:
            self.gems -= 1
            self.world.loose_screen()
            self.world.reset()
        else:
            self.world.game_over_flag = True

    def check_weapons(self):
        """Check for weapon pickup collisions"""
        hits = pg.sprite.spritecollide(self, self.world.weapon_pickups, True)
        for weapon in hits:
            # Track collected weapon to prevent respawning
            weapon_x = weapon.rect.centerx // GRIDSIZE
            weapon_y = weapon.rect.centery // GRIDSIZE
            self.world.collected_items.add(
                f"{self.world.current_level_name}_weapon_{weapon_x}_{weapon_y}"
            )
            self.pick_up_weapon(weapon.weapon_name)

    def pick_up_weapon(self, weapon_name):
        """Add weapon to player's inventory"""
        self.weapons[weapon_name] = 0
        if self.active_weapon is None:
            self.active_weapon = weapon_name
            self.load_weapon_image()

    def load_weapon_image(self):
        """Load the image for the active weapon"""
        if not self.active_weapon:
            self.weapon_image = None
            return

        weapon_data = WEAPON_CONFIG.get(self.active_weapon)
        if not weapon_data:
            return

        image_path = os.path.join(IMAGEPATH, weapon_data["image"])
        loaded_image = pg.image.load(image_path).convert_alpha()
        weapon_size = (
            int(weapon_data["size"] * GRIDSIZE * WEAPON_SCALE_FACTOR),
            int(weapon_data["size"] * GRIDSIZE * WEAPON_SCALE_FACTOR),
        )
        self.weapon_image = pg.transform.scale(loaded_image, weapon_size)

    def has_weapon(self, weapon_name):
        """Check if player has a specific weapon"""
        return weapon_name in self.weapons

    def shoot_bullet(self):
        """Fire a bullet if player has a shooting weapon"""
        if not self.active_weapon:
            return
        weapon_data = WEAPON_CONFIG.get(self.active_weapon)
        if not weapon_data:
            return
        # Regular shooting weapons: fire a single bullet immediately
        if weapon_data.get("type") != "shooting":
            return

        direction_x = 1 if self.vx >= 0 else -1
        direction_y = 0

        # Pass gravity hint to Bullet if weapon requests it
        use_gravity = weapon_data.get("gravity", False)

        bullet = Bullet(
            self.rect.centerx,
            self.rect.centery,
            direction_x,
            direction_y,
            self.active_weapon,
            self.world,
            from_enemy=False,
            use_gravity=use_gravity,
        )
        self.world.bullets.add(bullet)
        self.world.all_sprites.add(bullet)
        # Set fire cooldown
        self.weapons[self.active_weapon] = weapon_data.get("fire_rate", 0)

    def start_shoot(self):
        """Begin firing: for spray weapons start the continuous emitter; for shooting weapons fire once."""
        if not self.active_weapon:
            return
        weapon_data = WEAPON_CONFIG.get(self.active_weapon)
        if not weapon_data:
            return

        if weapon_data.get("type") == "spray":
            # Start continuous spray if not already running
            if not (self.spray_stream and self.spray_stream.alive()):
                self.spray_stream = SprayStream(self, self.active_weapon, self.world)
                self.world.all_sprites.add(self.spray_stream)
        elif weapon_data.get("type") == "shooting":
            # Fire a single shot immediately on press
            self.shoot_bullet()

    def stop_shoot(self):
        """Stop firing: terminate any continuous spray emitter."""
        if self.spray_stream and self.spray_stream.alive():
            try:
                self.spray_stream.kill()
            except Exception:
                pass
            self.spray_stream = None

    def melee_attack(self):
        """Perform melee attack if player has a melee weapon"""

        if not self.active_weapon:
            return

        weapon_data = WEAPON_CONFIG.get(self.active_weapon)
        print(self.active_weapon, weapon_data["type"])
        if not weapon_data or weapon_data["type"] != "melee":
            return

        if self.weapons[self.active_weapon] > 0:
            return

        # Start attack animation
        self.is_attacking = True
        self.attack_frame = 0

        # Play melee attack sound
        sound_manager.play_sound_effect("enemy_hit")

        attack_range = weapon_data["range"] * GRIDSIZE
        for enemy in self.world.enemies:
            distance = math.hypot(
                enemy.rect.centerx - self.rect.centerx,
                enemy.rect.centery - self.rect.centery,
            )
            if distance <= attack_range:
                enemy.take_damage(weapon_data["damage"])

        # Set cooldown
        self.weapons[self.active_weapon] = weapon_data["cooldown"]

    def handle_ladder_mechanics(self):
        """Handle all ladder climbing mechanics"""
        keys = pg.key.get_pressed()

        # Check for ladder collision
        self.on_ladder = False
        for ladder in self.world.ladders:
            if ladder.can_climb(self):
                self.on_ladder = True
                # Start climbing when pressing up/down
                if (keys[pg.K_UP] or keys[pg.K_DOWN]) and not self.ladder_grip:
                    self.ladder_grip = True
                    self.vx = 0
                    self.vy = 0
                break

        # Handle ladder tops
        for ladder_top in self.world.ladder_tops:
            # Check if player can climb up through this top
            if ladder_top.can_climb_up(self):
                self.on_ladder = True
                if (keys[pg.K_UP] or keys[pg.K_DOWN]) and not self.ladder_grip:
                    self.ladder_grip = True
                    self.vx = 0
                    self.vy = 0
            # Check if player should be blocked by the top
            elif ladder_top.should_block(self):
                if ladder_top not in self.world.platforms:
                    self.world.platforms.add(ladder_top)
            elif ladder_top in self.world.platforms:
                self.world.platforms.remove(ladder_top)

            # Check for climbing down from top
            if ladder_top.can_climb_down(self):
                self.ladder_grip = True
                self.on_ladder = True
                # Remove from platforms to allow climbing down
                if ladder_top in self.world.platforms:
                    self.world.platforms.remove(ladder_top)

        # Handle ladder movement
        if self.on_ladder and self.ladder_grip:
            # Vertical movement (only when pressing up/down)
            if keys[pg.K_UP]:
                self.vy = -self.ladder_move_speed
            elif keys[pg.K_DOWN]:
                self.vy = self.ladder_move_speed
            else:
                self.vy = 0  # Stay in place when not pressing up/down

            # Slower horizontal movement
            if keys[pg.K_LEFT]:
                self.vx = -self.ladder_move_speed
            elif keys[pg.K_RIGHT]:
                self.vx = self.ladder_move_speed
            else:
                self.vx = 0

            # Can jump off
            if keys[pg.K_SPACE]:
                self.ladder_grip = False
                self.jump()
        elif not self.on_ladder:
            self.ladder_grip = False

    def handle_waterfall_mechanics(self):
        """Handle all waterfall flow mechanics"""
        keys = pg.key.get_pressed()

        # Check for waterfall collision
        self.in_waterfall = False
        for waterfall in self.world.waterfalls:
            if waterfall.can_flow(self):
                self.in_waterfall = True
                if (keys[pg.K_UP] or keys[pg.K_DOWN]) and not self.waterfall_grip:
                    self.waterfall_grip = True
                    self.vx = 0
                break

        # Handle waterfall tops
        for waterfall_top in self.world.waterfall_tops:
            if waterfall_top.is_platform_collision(self):
                if waterfall_top not in self.world.platforms:
                    self.world.platforms.add(waterfall_top)
            elif waterfall_top in self.world.platforms:
                self.world.platforms.remove(waterfall_top)

            if waterfall_top.can_flow_down(self):
                self.waterfall_grip = True
                self.in_waterfall = True

        # Handle waterfall movement
        if self.in_waterfall and self.waterfall_grip:
            # Always flow down unless climbing
            if keys[pg.K_UP]:
                self.vy = -self.waterfall_move_speed
            else:
                self.vy = self.waterfall_move_speed  # Always flow down

            # Slower horizontal movement
            if keys[pg.K_LEFT]:
                self.vx = -self.waterfall_move_speed
            elif keys[pg.K_RIGHT]:
                self.vx = self.waterfall_move_speed
            else:
                self.vx = 0

            # Can jump out
            if keys[pg.K_SPACE]:
                self.waterfall_grip = False
                self.jump()
        elif not self.in_waterfall:
            self.waterfall_grip = False

    def update(self):
        # Update knockback animation if active
        self.update_knockback_animation()

        if self.knockback_timer > 0:
            self.knockback_timer -= 1  # Decrease knockback timer
        else:
            self.is_knocked_back = False  # End knockback state

        if not self.is_knocked_back:
            # Handle ladder and waterfall mechanics
            self.handle_ladder_mechanics()
            self.handle_waterfall_mechanics()

            # Update attack animation
            if self.is_attacking:
                self.attack_frame += 1
                if self.attack_frame >= self.attack_duration:
                    self.is_attacking = False
                    self.attack_frame = 0

            self.apply_gravity()
            self.check_edges()
            self.move()
            self.check_items()
            self.check_powerups()
            self.handle_powerup_timers()
            self.check_trophies()
            self.check_exit()
            self.check_weapons()
            self.check_pipes()
            self.check_spikes()

            # Check for collisions with enemies
            enemy_hit = pg.sprite.spritecollideany(self, self.world.enemies)
            if enemy_hit:
                self.handle_enemy_collision()

        # Update weapon cooldowns
        for weapon_name in self.weapons:
            if self.weapons[weapon_name] > 0:
                self.weapons[weapon_name] -= 1

        # Update exploding object cooldown
        if self.exploding_object_cooldown > 0:
            self.exploding_object_cooldown -= 1

        # Update weapon position
        self.update_weapon_position()

    def update_weapon_position(self):
        """Update weapon position relative to player"""
        if not self.weapon_image:
            return

        # Determine facing direction (1 = right, -1 = left)
        facing = 1 if self.vx >= 0 else -1

        # Base position
        weapon_offset_x = GRIDSIZE * 0.5 * facing
        weapon_offset_y = 0

        # Add swing animation during attack
        if self.is_attacking:
            # Calculate swing progress (0.0 to 1.0)
            progress = self.attack_frame / self.attack_duration

            # Simple up-down motion: starts at 0, goes up (-GRIDSIZE), returns to 0
            # Using a sine wave for smooth motion
            swing_height = -GRIDSIZE * math.sin(progress * math.pi)
            weapon_offset_y = swing_height

        weapon_x = self.rect.centerx + weapon_offset_x
        weapon_y = self.rect.centery + weapon_offset_y

        self.weapon_rect = self.weapon_image.get_rect(center=(weapon_x, weapon_y))

    def draw(self, screen, camera_offset_x, camera_offset_y=0):
        """Draw player and weapon"""
        # Draw player
        offset_rect = self.rect.move(-camera_offset_x, -camera_offset_y)
        screen.blit(self.image, offset_rect)

        # Draw weapon
        if self.weapon_image and self.weapon_rect:
            weapon_offset_rect = self.weapon_rect.move(
                -camera_offset_x, -camera_offset_y
            )
            screen.blit(self.weapon_image, weapon_offset_rect)

    def handle_enemy_collision(self):
        # Get the enemy that was collided with
        enemy_hit = pg.sprite.spritecollideany(self, self.world.enemies)

        if not enemy_hit:
            return

        # Check if enemy is already dying
        if hasattr(enemy_hit, "is_dying") and enemy_hit.is_dying:
            return

        # Check if player is jumping on the enemy (from above)
        # Player must be falling (vy > 0) and player's bottom must be above enemy's center
        if self.vy > 0 and self.rect.bottom <= enemy_hit.rect.centery:
            # Stomp on enemy
            if hasattr(enemy_hit, "is_minion") and enemy_hit.is_minion:
                # Minion: instant kill
                enemy_hit.take_damage(enemy_hit.health)
            else:
                # Regular enemy: deal 10 damage
                enemy_hit.take_damage(10)

            # Determine which direction to push the enemy based on where player jumped from
            player_relative_x = self.rect.centerx - enemy_hit.rect.centerx

            # Bounce the player up
            self.vy = -10

            # Push enemy in the opposite direction of the jump
            if player_relative_x < 0:
                # Player jumped from the left side, push enemy to the right
                if hasattr(enemy_hit, "rect"):
                    enemy_hit.rect.x += 100
            else:
                # Player jumped from the right side, push enemy to the left
                if hasattr(enemy_hit, "rect"):
                    enemy_hit.rect.x -= 100

            sound_manager.play_sound_effect("jump")  # Play bounce sound
            return

        # Invincible in marvin mode - no damage or knockback
        if self.world.marvin_mode:
            return

        # Otherwise, take damage from collision
        if not self.is_knocked_back:  # Prevent repeated knockback during incapacitation
            # Take damage
            self.take_damage(1)

            # Start knockback
            self.is_knocked_back = True
            self.knockback_timer = PLAYER_KNOCKBACK_TIMER

            knockback_distance = GRIDSIZE * PLAYER_KNOCKBACK_DISTANCE
            if self.vx > 0:  # Moving right
                self.knockback_direction = -1  # Throw left
            elif self.vx < 0:  # Moving left
                self.knockback_direction = 1  # Throw right
            else:
                self.knockback_direction = -1  # Default to left if no movement

            self.knockback(knockback_distance)

    def knockback(self, distance):
        """Start knockback animation (non-blocking, updates each frame)."""
        steps = PLAYER_KNOCKBACK_STEPS
        self.knockback_step_distance = distance // steps
        self.knockback_animation_steps = steps
        # Initial upward velocity for knockback
        self.vy = -PLAYER_KNOCKBACK_LIFT

    def update_knockback_animation(self):
        """Update knockback animation each frame (called from update())."""
        if self.knockback_animation_steps <= 0:
            return

        # Move horizontally
        self.rect.x += self.knockback_direction * self.knockback_step_distance

        # Check for horizontal collisions
        hits = pg.sprite.spritecollide(self, self.world.platforms, False)
        for hit in hits:
            if self.knockback_direction > 0:  # Moving right
                self.rect.right = hit.rect.left
            elif self.knockback_direction < 0:  # Moving left
                self.rect.left = hit.rect.right

        # Apply gravity during knockback
        self.vy += GRAVITY
        if self.vy > MAX_VELOCITY:
            self.vy = MAX_VELOCITY

        # Apply vertical movement
        self.rect.y += self.vy

        # Check for vertical collisions
        hits = pg.sprite.spritecollide(self, self.world.platforms, False)
        for hit in hits:
            if self.vy > 0:  # Falling
                self.rect.bottom = hit.rect.top
            elif self.vy < 0:  # Jumping
                self.rect.top = hit.rect.bottom
            self.vy = 0  # Stop vertical movement on collision

        # Ensure the player doesn't move out of bounds
        self.check_edges()

        # Decrement animation counter
        self.knockback_animation_steps -= 1

    def throw_exploding_object(self):
        """Throw an exploding object if cooldown has elapsed."""
        if self.exploding_object_cooldown > 0:
            return

        direction_x = 1 if self.vx >= 0 else -1
        direction_y = 0

        exploding_object = ExplodingObject(
            self.rect.centerx,
            self.rect.centery,
            direction_x,
            direction_y,
            EXPLODING_OBJECT_DAMAGE,
            self.world,
        )
        self.world.bullets.add(exploding_object)
        self.world.all_sprites.add(exploding_object)

        self.exploding_object_cooldown = EXPLODING_OBJECT_COOLDOWN
