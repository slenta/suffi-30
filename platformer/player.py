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

    def jump(self):
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.world.platforms, False)
        self.rect.y -= 2
        if len(hits) > 0:
            self.vy = -1 * self.jump_power
            sound_manager.play_sound_effect("jump")  # Play jump sound

    def apply_gravity(self):
        self.vy += GRAVITY
        if self.vy > MAX_VELOCITY:
            self.vy = MAX_VELOCITY

    def move(self):
        keys = pg.key.get_pressed()

        # Handle horizontal movement
        if keys[KEYBINDINGS.get("left")]:
            self.vx = -1 * self.speed
        elif keys[KEYBINDINGS.get("right")]:
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
            self.active_powerups[powerup.power_type] = [300, powerup]
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
            self.apply_gravity()
            self.check_edges()
            self.move()
            self.check_items()
            self.check_powerups()
            self.handle_powerup_timers()
            self.check_trophies()
            self.check_exit()
            self.check_weapons()

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
        damage = 20  # Set the damage dealt by the exploding object

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
