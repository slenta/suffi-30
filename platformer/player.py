import pygame as pg
import os
from .settings import *
from .bullet import ExplodingObject  # Import the ExplodingObject class


## Class Player
class Player(pg.sprite.Sprite):

    def __init__(self, _x, _y, world, start_gems=0, health=100):
        super().__init__()
        self.img = []
        for i in range(2):
            player_image = pg.image.load(
                os.path.join(IMAGEPATH, "alien_green_0" + str(i) + ".png")
            ).convert_alpha()
            self.img.append(player_image)
        self.image = self.img[0]
        self.rect = self.image.get_rect()
        self.rect.x = _x * GRIDSIZE
        self.rect.bottom = _y * GRIDSIZE
        # self.rect.topleft = (self.rect.x, self.rect.y)
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

    def jump(self):
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.world.platforms, False)
        self.rect.y -= 2
        if len(hits) > 0:
            self.vy = -1 * self.jump_power

    def apply_gravity(self):
        self.vy += GRAVITY
        if self.vy > MAX_VELOCITY:
            self.vy = MAX_VELOCITY

    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:  # LEFT
            self.vx = -1 * self.speed
        elif keys[pg.K_d]:  # RIGHT
            self.vx = self.speed
        elif keys[pg.K_w]:  # JUMP
            self.jump()
        else:
            self.vx = 0

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

    def check_powerups(self):
        hits = pg.sprite.spritecollide(self, self.world.powerups, True)
        for powerup in hits:
            powerup.apply_effect(self)
            self.active_powerups[powerup.power_type] = [300, powerup]

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
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.loose()  # Call the loose function when health is 0

    def loose(self):
        if self.gems >= 1:
            self.gems -= 1
            self.world.loose_screen()
            self.world.reset()
        else:
            self.world.game_over()

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

            # Check for collisions with enemies
            enemy_hit = pg.sprite.spritecollideany(self, self.world.enemies)
            if enemy_hit:
                self.handle_enemy_collision()

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
