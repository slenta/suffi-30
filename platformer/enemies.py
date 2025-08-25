import math
import random
import pygame as pg
from .bullet import Bullet  # Import the Bullet class
from .settings import *
from .bullet import ExplodingObject


class Enemy(pg.sprite.Sprite):
    def __init__(
        self,
        _x,
        _y,
        _image_path,
        speed,
        patrol_range,
        size_multiplier=1,
        health=1,
        damage=1,
        shoot_range=5,
        world=None,
        chase_range=10,
        melee_damage=5,
        can_throw_explosives=True,  # Default to True for regular enemies
    ):
        super().__init__()
        # Store the image path
        self.image_path = _image_path

        # Load and scale the image
        original_image = pg.image.load(_image_path).convert_alpha()
        self.image = pg.transform.scale(
            original_image, (GRIDSIZE * size_multiplier, GRIDSIZE * size_multiplier)
        )
        self.rect = self.image.get_rect()
        self.rect.x = _x * GRIDSIZE
        self.rect.y = _y * GRIDSIZE

        # Store initial positions
        self.initial_x = self.rect.x
        self.initial_y = self.rect.y

        self.speed = speed
        self.start_x = self.rect.x
        self.patrol_range = patrol_range
        self.direction = 1  # 1 for right, -1 for left
        self.size_multiplier = size_multiplier
        self.health = health
        self.max_health = health
        self.damage = damage
        self.shoot_range = shoot_range * GRIDSIZE
        self.chase_range = chase_range * GRIDSIZE
        self.melee_damage = melee_damage
        self.world = world
        self.shoot_timer = 0
        self.can_throw_explosives = can_throw_explosives  # Add this flag

        # Add gravity-related attributes
        self.vy = 0  # Vertical velocity
        self.on_ground = False  # Flag to check if the enemy is on the ground

    def update(self, player):
        # Apply gravity
        self.vy += GRAVITY
        if self.vy > MAX_VELOCITY:
            self.vy = MAX_VELOCITY
        self.rect.y += self.vy

        # Check for collisions with platforms
        hits = pg.sprite.spritecollide(self, self.world.platforms, False)
        if hits:
            self.rect.bottom = hits[
                0
            ].rect.top  # Place the enemy on top of the platform
            self.vy = 0  # Stop vertical movement
            self.on_ground = True
        else:
            self.on_ground = False

        # Check if the player is within chasing range
        distance_to_player = math.hypot(
            player.rect.centerx - self.rect.centerx,
            player.rect.centery - self.rect.centery,
        )
        if distance_to_player <= self.chase_range:
            self.chase_player(player)
        else:
            self.patrol()

        # Check for melee attack
        if distance_to_player <= GRIDSIZE:  # Close range for melee attack
            self.melee_attack(player)

        # Shooting logic
        if distance_to_player <= self.shoot_range:
            self.shoot_at_player(player)

        # Summon minions
        self.summon_minion(player)
        if self.can_throw_explosives:  # Only throw explosives if the flag is set
            self.throw_exploding_object(player)  # Attempt to throw an exploding object

    def chase_player(self, player):
        # Check for holes in the ground
        if self.detect_hole():
            return  # Stop moving if a hole is detected

        # Move toward the player horizontally
        if player.rect.centerx > self.rect.centerx:
            self.rect.x += self.speed
        elif player.rect.centerx < self.rect.centerx:
            self.rect.x -= self.speed

        # Check for horizontal collisions with platforms
        hits = pg.sprite.spritecollide(self, self.world.platforms, False)
        for hit in hits:
            if self.rect.right > hit.rect.left and self.rect.left < hit.rect.right:
                if player.rect.centerx > self.rect.centerx:  # Moving right
                    self.rect.right = hit.rect.left
                elif player.rect.centerx < self.rect.centerx:  # Moving left
                    self.rect.left = hit.rect.right

        # Ignore vertical movement

    def shoot_at_player(self, player):
        if self.shoot_timer == 0:  # Only shoot if the timer is 0
            # Determine the direction of the bullet
            direction_x = player.rect.centerx - self.rect.centerx
            direction_y = player.rect.centery - self.rect.centery
            magnitude = math.hypot(direction_x, direction_y)
            direction_x /= magnitude  # Normalize the direction vector
            direction_y /= magnitude

            # Create a bullet and add it to the world's bullet group
            bullet = Bullet(
                self.rect.centerx,
                self.rect.centery,
                direction_x,
                direction_y,
                self.damage,
                self.world,
                from_enemy=True,  # Enemy bullet
            )
            self.world.bullets.add(bullet)
            self.world.all_sprites.add(bullet)
            self.shoot_timer = 60  # Cooldown for shooting (e.g., 1 second at 60 FPS)

        # Decrease the shoot timer
        if self.shoot_timer > 0:
            self.shoot_timer -= 1

    def melee_attack(self, player):
        # Deal melee damage to the player
        player.take_damage(self.melee_damage)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def patrol(self):
        # Check for holes in the ground
        if self.detect_hole():
            self.direction *= -1  # Reverse direction
            return  # Skip horizontal movement for this frame

        # Move the enemy back and forth within its patrol range
        self.rect.x += self.speed * self.direction

        # Check for horizontal collisions with platforms
        hits = pg.sprite.spritecollide(self, self.world.platforms, False)
        for hit in hits:
            if self.direction > 0:  # Moving right
                self.rect.right = hit.rect.left
                self.direction *= -1  # Reverse direction
            elif self.direction < 0:  # Moving left
                self.rect.left = hit.rect.right
                self.direction *= -1  # Reverse direction

        # Reverse direction if patrol range is exceeded
        if self.rect.x > self.start_x + self.patrol_range or self.rect.x < self.start_x:
            self.direction *= -1

    def reset_position(self):
        # Reset the enemy's position to its initial position
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y
        self.start_x = self.initial_x  # Reset patrol range reference

    def draw_health_bar(self, screen, camera_offset_x):
        # Define the position and size of the health bar
        bar_width = self.rect.width
        bar_height = 5
        bar_x = self.rect.x - camera_offset_x
        bar_y = self.rect.y - 10  # Position above the enemy

        # Calculate the width of the filled portion based on enemy's health
        fill_width = int((self.health / self.max_health) * bar_width)

        # Draw the health bar background (gray)
        pg.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))

        # Draw the filled portion of the health bar (red)
        pg.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, fill_width, bar_height))

        # Optionally, draw a border around the health bar (white)
        pg.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)

    def summon_minion(self, player):
        # Check if the enemy is alive and the player is within one game width
        distance_to_player = abs(player.rect.centerx - self.rect.centerx)

        if (
            self.health > 0
            and distance_to_player <= WIDTH
            and random.random() < 0.001  # 0.1% chance per frame to summon a minion
        ):
            minion = Enemy(
                self.rect.x // GRIDSIZE,
                self.rect.y // GRIDSIZE,
                _image_path=self.image_path,  # Use the same image
                speed=self.speed,
                patrol_range=50,  # Smaller patrol range for minions
                size_multiplier=0.5,  # Smaller size for minions
                health=3,  # Lower health for minions
                damage=1,  # Lower damage for minions
                shoot_range=3,  # Shorter shooting range
                world=self.world,
                chase_range=5,  # Smaller chase range
                melee_damage=2,  # Lower melee damage
                can_throw_explosives=False,  # Minions cannot throw explosives
            )
            self.world.enemies.add(minion)
            self.world.all_sprites.add(minion)

    def throw_exploding_object(self, player):
        if not self.can_throw_explosives:  # Minions cannot throw explosives
            return

        if random.random() < 0.01:  # 1% chance per frame to throw an object
            direction_x = player.rect.centerx - self.rect.centerx
            direction_y = player.rect.centery - self.rect.centery
            magnitude = math.hypot(direction_x, direction_y)
            direction_x /= magnitude  # Normalize the direction vector
            direction_y /= magnitude

            # Create the exploding object
            exploding_object = ExplodingObject(
                self.rect.centerx,
                self.rect.centery - 15,
                direction_x,
                direction_y,
                damage=20,  # Explosion damage
                world=self.world,
            )
            self.world.bullets.add(exploding_object)
            self.world.all_sprites.add(exploding_object)

    def detect_hole(self):
        # Check the tile in front of the enemy based on its direction
        next_x = self.rect.centerx + (self.direction * GRIDSIZE)
        next_y = self.rect.bottom + 1  # Check just below the bottom of the enemy

        # Create a temporary rect to check for platforms
        temp_rect = pg.Rect(next_x, next_y, GRIDSIZE, 1)

        # Check if there is a platform below the next step
        return not any(
            temp_rect.colliderect(platform.rect) for platform in self.world.platforms
        )
