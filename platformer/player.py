import pygame as pg
import os
from .settings import *
from .bullet import Bullet, ExplodingObject  # Import the ExplodingObject class
from .sound_manager import sound_manager  # Import the sound manager
from .weapon_stats import WEAPON_CONFIG
import math


## Class Player
class Player(pg.sprite.Sprite):

    def __init__(self, _x, _y, world, start_gems=0, trophies_collected=0, health=100):
        super().__init__()
        self.img = []
        for i in range(2):
            player_image = pg.image.load(
                os.path.join(IMAGEPATH, "suffi_0" + str(i) + ".png")
            ).convert_alpha()
            self.img.append(player_image)
        self.image = self.img[0]
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
        self.active_powerups = {}
        self.trophies_collected = trophies_collected
        self.weapons = {}  # {weapon_name: cooldown_timer}
        self.active_weapon = None
        self.weapon_image = None
        self.weapon_rect = None
        self.controls_reversed = False  # Flag for reversed controls powerup
        self.spike_damage_cooldown = 0  # Cooldown to prevent repeated spike damage
        
        # Ladder mechanics
        self.on_ladder = False  # Flag to track if player is on a ladder
        self.ladder_grip = False  # Flag to track if player is gripping the ladder
        self.ladder_move_speed = 2  # Speed when moving on ladder
        
        # Waterfall mechanics
        self.in_waterfall = False  # Flag to track if player is in waterfall
        self.waterfall_grip = False  # Flag to track if player is gripping waterfall
        self.waterfall_move_speed = 2  # Speed when moving in waterfall

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

        # Horizonfale Kollision
        self.rect.x += self.vx
        hits = pg.sprite.spritecollide(self, self.world.platforms, False)
        for hit in hits:
            if self.vx > 0:
                self.rect.right = hit.rect.left
            elif self.vx < 0:
                self.rect.left = hit.rect.right

        # Vertikale Kollision
        self.rect.y += self.vy
        hits = pg.sprite.spritecollide(self, self.world.platforms, False)
        for hit in hits:
            if self.vy > 0:
                self.rect.bottom = hit.rect.top
                # If standing on a moving platform, move with it
                if hit in self.world.moving_platforms:
                    vel_x, vel_y = hit.get_velocity()
                    self.rect.x += vel_x
            elif self.vy < 0:
                self.rect.top = hit.rect.bottom
            self.vy = 0

        # Von der Plattform runterfallen
        if self.rect.y > self.world.top + 20:
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
            item.apply(self)
            sound_manager.play_sound_effect("gem_collect")  # Play gem collection sound

    def check_powerups(self):
        hits = pg.sprite.spritecollide(self, self.world.powerups, True)
        for powerup in hits:
            powerup.apply_effect(self)
            # Type 3 powerup lasts 8 seconds (480 frames at 60 FPS), others last 5 seconds (300 frames)
            duration = 240 if powerup.power_type == 3 else 480
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
        self.trophies_collected += len(hits)

    def check_exit(self):
        if self.trophies_collected == self.world.total_trophies:
            self.world.exit.open()
            # All trophies collected
        if pg.sprite.collide_rect(self, self.world.exit) and self.world.exit.is_open:
            sound_manager.play_sound_effect(
                "level_complete"
            )  # Play level complete sound
            self.world.level_complete()

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
        # Decrease spike damage cooldown
        if self.spike_damage_cooldown > 0:
            self.spike_damage_cooldown -= 1
            return

        for spike in self.world.spikes:
            if spike.check_collision(self):
                # Take damage from the spike
                self.take_damage(spike.damage)
                # Apply knockback away from the spike
                self.apply_spike_knockback(spike)
                # Set cooldown to prevent repeated damage
                self.spike_damage_cooldown = 30  # ~0.5 seconds at 60 FPS
                break  # Only process one spike hit per frame

    def apply_spike_knockback(self, spike):
        """Apply knockback effect when hit by spikes - push player back 2-3 blocks."""
        if not self.is_knocked_back:
            self.is_knocked_back = True
            self.knockback_timer = 20  # Brief invulnerability period

            # Knockback distance (2.5 blocks)
            knockback_distance = GRIDSIZE * 2.5

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
        sound_manager.play_sound_effect("player_hurt")  # Play hurt sound
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.loose()  # Call the loose function when health is 0

    def loose(self):
        sound_manager.play_sound_effect("player_death")  # Play death/fall sound
        if self.gems >= 1:
            self.gems -= 1
            self.world.loose_screen()
            self.world.reset()
        else:
            self.world.game_over()

    def check_weapons(self):
        """Check for weapon pickup collisions"""
        hits = pg.sprite.spritecollide(self, self.world.weapon_pickups, True)
        for weapon in hits:
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
        # Scale weapon to be smaller (1/3 of player size)
        weapon_size = (
            weapon_data["size"] * GRIDSIZE // 2,
            weapon_data["size"] * GRIDSIZE // 2,
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
        if not weapon_data or weapon_data["type"] != "shooting":
            return

        direction_x = 1 if self.vx >= 0 else -1
        direction_y = 0

        bullet = Bullet(
            self.rect.centerx,
            self.rect.centery,
            direction_x,
            direction_y,
            self.active_weapon,
            self.world,
            from_enemy=False,
        )
        self.world.bullets.add(bullet)
        self.world.all_sprites.add(bullet)
        self.weapons[self.active_weapon] = weapon_data["fire_rate"]

    def melee_attack(self):
        """Perform melee attack if player has a melee weapon"""
        if not self.active_weapon:
            return

        weapon_data = WEAPON_CONFIG.get(self.active_weapon)
        if not weapon_data or weapon_data["type"] != "melee":
            return

        if self.weapons[self.active_weapon] > 0:
            return

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

    def update(self):
        if self.knockback_timer > 0:
            self.knockback_timer -= 1  # Decrease knockback timer
        else:
            self.is_knocked_back = False  # End knockback state

        if not self.is_knocked_back:  # Only allow normal updates if not incapacitated
            # Handle ladder mechanics
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
                
            # Handle waterfall mechanics (continuous downward flow)
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

        # Update weapon position
        self.update_weapon_position()

    def update_weapon_position(self):
        """Update weapon position relative to player"""
        if not self.weapon_image:
            return

        # Position weapon on player's right side (or left if facing left)
        offset_x = 12 if self.vx >= 0 else -12
        offset_y = 0

        # Determine facing direction (1 = right, -1 = left)
        facing = 1 if self.vx >= 0 else -1

        # Idle: weapon at player's side
        weapon_offset_x = GRIDSIZE * 0.5 * facing
        weapon_x = self.rect.centerx + weapon_offset_x
        weapon_y = self.rect.centery

        weapon_rect = self.weapon_image.get_rect(center=(weapon_x, weapon_y))
        offset_rect = weapon_rect.move(-self.world.camera_offset_x, 0)
        self.world.screen.blit(self.weapon_image, offset_rect)
        self.weapon_rect = self.weapon_image.get_rect(
            center=(self.rect.centerx + offset_x, self.rect.centery + offset_y)
        )

    def draw(self, screen, camera_offset_x):
        """Draw player and weapon"""
        # Draw player
        offset_rect = self.rect.move(-camera_offset_x, 0)
        screen.blit(self.image, offset_rect)

        # Draw weapon
        if self.weapon_image and self.weapon_rect:
            weapon_offset_rect = self.weapon_rect.move(-camera_offset_x, 0)

            # Rotate weapon during attack
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

            # Bounce the player up
            self.vy = -10
            sound_manager.play_sound_effect("jump")  # Play bounce sound
            return

        # Otherwise, take damage from collision
        if not self.is_knocked_back:  # Prevent repeated knockback during incapacitation
            # Take damage
            self.take_damage(1)

            # Start knockback
            self.is_knocked_back = True
            self.knockback_timer = (
                30  # Incapacitated for 30 frames (~0.5 seconds at 60 FPS)
            )

            # Determine the direction to throw the player
            knockback_distance = GRIDSIZE * 6
            if self.vx > 0:  # Moving right
                self.knockback_direction = -1  # Throw left
            elif self.vx < 0:  # Moving left
                self.knockback_direction = 1  # Throw right
            else:
                self.knockback_direction = -1  # Default to left if no movement

            self.knockback(knockback_distance)

    def knockback(self, distance):
        # Smoothly move the player during knockback
        steps = 30  # Number of steps for the knockback animation
        step_distance = distance // steps

        for _ in range(steps):
            # Apply horizontal knockback
            self.rect.x += self.knockback_direction * step_distance
            self.rect.y -= 2  # Slightly lift the player during knockback

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

            # Update the camera to follow the player
            self.world.update_camera()

            # Redraw the game world to show the knockback animation
            self.world.draw()
            pg.display.flip()
            pg.time.delay(10)  # Delay for smooth animation

    def throw_exploding_object(self):
        # Determine the direction of the throw based on the player's facing direction
        direction_x = 1 if self.vx >= 0 else -1
        direction_y = 0  # Exploding objects are thrown horizontally
        damage = 5  # Set the damage dealt by the exploding object

        # Create the exploding object
        exploding_object = ExplodingObject(
            self.rect.centerx,
            self.rect.centery,
            direction_x,
            direction_y,
            damage,
            self.world,
        )
        self.world.bullets.add(exploding_object)
        self.world.all_sprites.add(exploding_object)


## End Class Player
