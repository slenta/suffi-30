"""Enemy AI and behavior."""

import math
import random
import pygame as pg
from .bullet import Bullet, ExplodingObject
from ..config.settings import GRIDSIZE, GRAVITY, MAX_VELOCITY, WIDTH, HEIGHT
from ..core.sound_manager import sound_manager
from ..config.constants import (
    ENEMY_MINION_SUMMON_CHANCE,
    ENEMY_EXPLOSIVE_THROW_CHANCE,
    ENEMY_DEATH_TIMER_MAX,
    ENEMY_DEATH_INITIAL_VY,
    ENEMY_DEATH_ROTATION_SPEED_MIN,
    ENEMY_DEATH_ROTATION_SPEED_MAX,
    ENEMY_MINION_SIZE,
    ENEMY_MINION_HEALTH,
    ENEMY_MINION_DAMAGE,
    ENEMY_MINION_MELEE_DAMAGE,
    ENEMY_MINION_PATROL_RANGE,
    ENEMY_MINION_SHOOT_RANGE,
    ENEMY_MINION_CHASE_RANGE,
)


class Enemy(pg.sprite.Sprite):
    """Enemy sprite with AI behavior, combat, and death animations."""

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
        is_minion=False,  # Default to False for regular enemies
        can_summon_minions=False,  # Default to False - must be explicitly enabled in level config
        encounter_message=None,  # Optional message to display when first encountered
        shoot_cooldown=60,  # Cooldown for shooting in frames (default: 60 = 1 second at 60 FPS)
        spawn_on_death=None,  # Optional dict with enemy config to spawn on death
        no_clip=False,  # If True, enemy can pass through blocks
        encounter_message_color=None,  # Optional RGB tuple for message color (e.g., (255, 0, 0) for red)
        explosive_image=None,  # Optional custom image for thrown explosives
        explosive_size=15,  # Size of explosive in pixels (default: 15)
    ):
        super().__init__()
        # Store the image path
        self.image_path = _image_path

        # Load and scale the image
        original_image = pg.image.load(_image_path).convert_alpha()
        self.original_image = pg.transform.scale(
            original_image, (GRIDSIZE * size_multiplier, GRIDSIZE * size_multiplier)
        )
        self.image = self.original_image.copy()
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
        self.last_direction = 1  # Track last direction for flipping
        self.size_multiplier = size_multiplier
        self.health = health
        self.max_health = health
        self.damage = damage
        self.shoot_range = shoot_range * GRIDSIZE
        self.chase_range = chase_range * GRIDSIZE
        self.melee_damage = melee_damage
        self.world = world
        self.shoot_timer = 0
        self.shoot_cooldown = shoot_cooldown  # Store the cooldown duration
        self.can_throw_explosives = can_throw_explosives  # Add this flag
        self.is_minion = is_minion  # Store minion status
        self.can_summon_minions = can_summon_minions  # Store minion summoning ability
        self.spawn_on_death = spawn_on_death  # Enemy config to spawn on death
        self.no_clip = no_clip  # Can pass through blocks

        # Encounter message attributes
        self.encounter_message = encounter_message  # Message to display
        self.encounter_message_color = encounter_message_color  # Optional custom color
        self.has_been_encountered = False  # Track if player has seen this enemy
        
        # Explosive customization
        self.explosive_image = explosive_image  # Custom image for thrown explosives
        self.explosive_size = explosive_size  # Size of explosive in pixels

        # Add gravity-related attributes
        self.vy = 0  # Vertical velocity
        self.on_ground = False  # Flag to check if the enemy is on the ground

        # Death animation attributes
        self.is_dying = False
        self.death_rotation = 0  # Rotation angle for tumbling effect
        self.death_rotation_speed = 15  # Degrees per frame
        self.death_horizontal_velocity = 3  # Horizontal movement when tumbling
        self.death_timer = 0  # Timer to remove enemy after falling off screen
        self.original_image = self.image.copy()  # Store original image for rotation

    def update(self, player):
        # If enemy is dying, only handle death animation
        if self.is_dying:
            self.update_death_animation()
            return

        # Check if enemy is visible to player for the first time
        if not self.has_been_encountered and self.encounter_message:
            # Check if player is very close to the enemy (within 3 tiles)
            distance_to_player = abs(player.rect.centerx - self.rect.centerx)
            if distance_to_player <= GRIDSIZE * 10 and self.is_visible_to_player():
                self.has_been_encountered = True
                # Trigger the encounter message in the world
                if self.world:
                    self.world.show_encounter_message(
                        self.encounter_message, self.encounter_message_color
                    )

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
        # Determine which direction we want to move
        move_right = player.rect.centerx > self.rect.centerx
        move_left = player.rect.centerx < self.rect.centerx

        # Temporarily set direction for hole detection
        if move_right:
            old_direction = self.direction
            self.direction = 1
            if self.detect_hole():
                self.direction = old_direction
                return  # Stop moving if a hole is detected
            self.direction = old_direction
        elif move_left:
            old_direction = self.direction
            self.direction = -1
            if self.detect_hole():
                self.direction = old_direction
                return  # Stop moving if a hole is detected
            self.direction = old_direction

        # Move toward the player horizontally
        if move_right:
            self.rect.x += self.speed
            self.direction = 1
        elif move_left:
            self.rect.x -= self.speed
            self.direction = -1

        # Flip image if direction changed
        self.update_sprite_direction()

        # Check for horizontal collisions with platforms (prevents climbing vertical walls)
        # Skip collision check if no_clip is enabled
        if not self.no_clip:
            hits = pg.sprite.spritecollide(self, self.world.platforms, False)
            for hit in hits:
                # Check if this is a vertical wall collision (not the platform we're standing on)
                # If enemy moved right and hit something on the right side
                if (
                    move_right
                    and self.rect.right > hit.rect.left
                    and self.rect.left < hit.rect.left
                ):
                    self.rect.right = hit.rect.left
                # If enemy moved left and hit something on the left side
                elif (
                    move_left
                    and self.rect.left < hit.rect.right
                    and self.rect.right > hit.rect.right
                ):
                    self.rect.left = hit.rect.right

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
            self.shoot_timer = self.shoot_cooldown  # Use the configured cooldown

        # Decrease the shoot timer
        if self.shoot_timer > 0:
            self.shoot_timer -= 1

    def melee_attack(self, player):
        # Don't attack if dying
        if self.is_dying:
            return
        # Deal melee damage to the player
        player.take_damage(self.melee_damage)

    def take_damage(self, damage):
        sound_manager.play_sound_effect("enemy_hit")  # Play enemy hit sound
        self.health -= damage

        # Track damage dealt by player for scoring
        if hasattr(self.world, "player") and hasattr(self.world.player, "damage_dealt"):
            self.world.player.damage_dealt += damage

        if self.health <= 0:
            self.start_death_animation()

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

        # Flip image if direction changed
        self.update_sprite_direction()

    def update_sprite_direction(self):
        """Flip the sprite image based on direction."""
        if self.direction != self.last_direction:
            self.image = pg.transform.flip(self.original_image, True, False)
            if self.direction == 1:  # Facing right - use original
                self.image = self.original_image.copy()
            self.last_direction = self.direction

    def reset_position(self):
        # Reset the enemy's position to its initial position
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y
        self.start_x = self.initial_x  # Reset patrol range reference

    def draw_health_bar(self, screen, camera_offset_x, camera_offset_y=0):
        # Define the position and size of the health bar
        bar_width = self.rect.width
        bar_height = 5
        bar_x = self.rect.x - camera_offset_x
        bar_y = self.rect.y - camera_offset_y - 10  # Position above the enemy

        # Calculate the width of the filled portion based on enemy's health
        fill_width = int((self.health / self.max_health) * bar_width)

        # Draw the health bar background (gray)
        pg.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))

        # Draw the filled portion of the health bar (red)
        pg.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, fill_width, bar_height))

        # Optionally, draw a border around the health bar (white)
        pg.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)

    def summon_minion(self, player):
        """Summon a smaller minion enemy (if ability is enabled)."""
        if not self.can_summon_minions or self.health <= 0:
            return

        distance_to_player = abs(player.rect.centerx - self.rect.centerx)

        if distance_to_player <= WIDTH and random.random() < ENEMY_MINION_SUMMON_CHANCE:
            minion = Enemy(
                self.rect.x // GRIDSIZE,
                self.rect.y // GRIDSIZE,
                _image_path=self.image_path,
                speed=self.speed,
                patrol_range=ENEMY_MINION_PATROL_RANGE,
                size_multiplier=ENEMY_MINION_SIZE,
                health=ENEMY_MINION_HEALTH,
                damage=ENEMY_MINION_DAMAGE,
                shoot_range=ENEMY_MINION_SHOOT_RANGE,
                world=self.world,
                chase_range=ENEMY_MINION_CHASE_RANGE,
                melee_damage=ENEMY_MINION_MELEE_DAMAGE,
                can_throw_explosives=False,
                is_minion=True,
            )
            self.world.enemies.add(minion)
            self.world.all_sprites.add(minion)

    def throw_exploding_object(self, player):
        """Throw an exploding object at the player (if ability is enabled)."""
        if not self.can_throw_explosives:
            return

        if random.random() < ENEMY_EXPLOSIVE_THROW_CHANCE:
            direction_x = player.rect.centerx - self.rect.centerx
            direction_y = player.rect.centery - self.rect.centery
            magnitude = math.hypot(direction_x, direction_y)
            direction_x /= magnitude
            direction_y /= magnitude

            exploding_object = ExplodingObject(
                self.rect.centerx,
                self.rect.centery - 15,
                direction_x,
                direction_y,
                damage=20,
                world=self.world,
                explosive_image=self.explosive_image,  # Pass custom image if set
                explosive_size=self.explosive_size,  # Pass custom size
            )
            self.world.bullets.add(exploding_object)
            self.world.all_sprites.add(exploding_object)

    def detect_hole(self):
        # Check the tile in front of the enemy based on its direction
        # Check slightly ahead of the enemy's edge to detect holes before walking off
        if self.direction > 0:  # Moving right
            check_x = self.rect.right + 5  # Check a bit ahead of the right edge
        else:  # Moving left
            check_x = self.rect.left - 5  # Check a bit ahead of the left edge

        check_y = self.rect.bottom + 5  # Check just below the bottom of the enemy

        # Create a small rect to check for platforms
        temp_rect = pg.Rect(check_x - 2, check_y, 4, 4)

        # Check if there is a platform below the next step
        return not any(
            temp_rect.colliderect(platform.rect) for platform in self.world.platforms
        )

    def is_visible_to_player(self):
        """Check if the enemy is currently visible on the screen (in player's sight)"""
        if not self.world:
            return False

        # Calculate the enemy's position relative to the camera
        screen_x = self.rect.x - self.world.camera_offset_x
        screen_y = self.rect.y - self.world.camera_offset_y

        # Check if enemy is within the visible screen area
        # Adding some margin to detect enemies just entering the screen
        margin = 50
        return (
            -margin <= screen_x <= WIDTH + margin
            and -margin <= screen_y <= HEIGHT + margin
        )

    def spawn_replacement_enemy(self):
        """Spawn a new enemy at this enemy's position when it dies."""
        import os
        from ..config.enemy_config import get_enemy_config
        from ..config.settings import IMAGEPATH

        print(
            f"🔍 spawn_replacement_enemy called. spawn_on_death config: {self.spawn_on_death}"
        )

        # Get the enemy type and any overrides from spawn_on_death config
        spawn_config = self.spawn_on_death.copy()
        enemy_type = spawn_config.pop("type")

        print(f"🔍 Enemy type to spawn: {enemy_type}")
        print(f"🔍 Additional config: {spawn_config}")

        # Get base config for the new enemy type
        new_enemy_config = get_enemy_config(enemy_type, **spawn_config)

        print(f"🔍 Full enemy config: {new_enemy_config}")

        # Create the new enemy at the current death position (not original spawn)
        new_enemy = Enemy(
            self.rect.x // GRIDSIZE,
            self.rect.y // GRIDSIZE,
            _image_path=os.path.join(IMAGEPATH, new_enemy_config["image"]),
            speed=new_enemy_config["speed"],
            patrol_range=new_enemy_config["patrol_range"],
            size_multiplier=new_enemy_config["size_multiplier"],
            health=new_enemy_config["health"],
            damage=new_enemy_config["damage"],
            shoot_range=new_enemy_config["shoot_range"],
            world=self.world,
            chase_range=new_enemy_config["chase_range"],
            melee_damage=new_enemy_config["melee_damage"],
            can_throw_explosives=new_enemy_config.get("can_throw_explosives", True),
            can_summon_minions=new_enemy_config.get("can_summon_minions", False),
            encounter_message=new_enemy_config.get("encounter_message"),
            shoot_cooldown=new_enemy_config.get("shoot_cooldown", 60),
            spawn_on_death=new_enemy_config.get("spawn_on_death"),
        )

        print(
            f"🔍 New enemy created at ({self.rect.x // GRIDSIZE}, {self.rect.y // GRIDSIZE})"
        )

        # Add to world sprite groups
        self.world.enemies.add(new_enemy)
        self.world.all_sprites.add(new_enemy)

        print(
            f"🔄 Spawned {enemy_type} at death position ({self.rect.x // GRIDSIZE}, {self.rect.y // GRIDSIZE})"
        )
        print(f"🔍 Total enemies in world now: {len(self.world.enemies)}")

    def start_death_animation(self):
        """Initialize the death animation (Mario-style tumble)."""
        self.is_dying = True
        self.vy = ENEMY_DEATH_INITIAL_VY
        self.death_horizontal_velocity = random.choice([-3, 3])
        self.death_rotation_speed = random.randint(
            ENEMY_DEATH_ROTATION_SPEED_MIN, ENEMY_DEATH_ROTATION_SPEED_MAX
        )

        # Spawn replacement enemy immediately at death position (before falling off screen)
        if self.spawn_on_death and self.world:
            self.spawn_replacement_enemy()

    def update_death_animation(self):
        """Handle the tumbling death animation"""
        # Apply gravity
        self.vy += GRAVITY
        if self.vy > MAX_VELOCITY:
            self.vy = MAX_VELOCITY

        # Update position
        self.rect.y += self.vy
        self.rect.x += self.death_horizontal_velocity

        # Rotate the sprite for tumbling effect
        self.death_rotation += self.death_rotation_speed
        if self.death_rotation >= 360:
            self.death_rotation -= 360

        # Create rotated image
        self.image = pg.transform.rotate(self.original_image, self.death_rotation)
        # Update rect to keep it centered during rotation
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        # Increase timer
        self.death_timer += 1

        # Remove enemy after falling off screen or after timeout
        if self.rect.top > HEIGHT + 100 or self.death_timer > ENEMY_DEATH_TIMER_MAX:
            # Track this enemy as killed in the world (only for non-minions)
            if self.world and hasattr(self, "enemy_id") and not self.is_minion:
                self.world.killed_enemies.add(self.enemy_id)
                print(f"💀 Enemy {self.enemy_id} killed and tracked")
            elif not hasattr(self, "enemy_id"):
                print(f"⚠️ Enemy died but has no enemy_id attribute!")
            elif self.is_minion:
                print(f"⏩ Minion died (not tracked)")
            self.kill()
