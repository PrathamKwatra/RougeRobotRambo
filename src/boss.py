# Name: boss.py
# Purpose: Defines the boss character that hovers at the top of the screen and tries to damage the player
# Version: 2.1
# Date: 5 June 2020
# Author(s): Khoa Hoang, Matt Innaurato, Adrienne Lhuc Estrella
# Dependencies: pygame, settings, projectiles, paths, utils, and random modules

import pygame as pg
from settings import *
from projectiles import *
from paths import *
from utils import *
from random import choice, randint


class BossBloodFX(FX):
    def __init__(self, game, x, y):
        """
        Blood effects that spawn when boss dies
        Initialize position of fx
        :param game: reference to game instance
        :param x: x-position
        :param y: y-position
        """
        super().__init__(game, x, y)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

    def load_frames(self):
        # Blood splat
        for file in bloodsplat:
            bloodimg = pg.image.load(file).convert_alpha()
            bloodimg = pg.transform.scale(bloodimg, (100, 100))
            self.frames.append(bloodimg)


class Boss(pg.sprite.Sprite):
    def __init__(self, game):
        """
        Main boss character sprite that flies above and tries to hit player with fireballs and ice shards
        Initialize animation frames, sprites, animation state variables, Pygame variable
        :param game: reference to game instance
        """
        super().__init__()
        self.game = game

        # Add to sprite groups
        self.game.char_sprites.add(self)
        self.game.all_sprites.add(self)

        # Frame lists
        self.flight_frames_r = []
        self.flight_frames_l = []
        self.attack1_frames_r = []
        self.attack1_frames_l = []
        self.attack2_frames_r = []
        self.attack2_frames_l = []
        self.takehit_frames_r = []
        self.takehit_frames_l = []
        self.death_frames = []
        self.land_frames = []
        self.load_sprite_sheets()

        # Initialize pygame elements
        self.image = self.flight_frames_r[0]
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, 36))
        hitbox_size = (80, 60)
        self.hitbox = pg.Rect(
            (SCREEN_WIDTH // 2 - hitbox_size[0] // 2, SCREEN_HEIGHT // 2), hitbox_size)
        self.hitbox.center = self.rect.center

        # Initialize vectors for realistic movements
        self.pos = pg.Vector2(self.rect.center)
        self.vel = pg.Vector2(0, 0)
        self.acc = pg.Vector2(0, 0)

        # Physics constants
        self.BASE_ACC = 1
        self.FRICTION = -0.08

        # Animations
        self.last_frame_update = 0
        self.current_frame = -1
        self.current_attack_frame = -1
        self.current_takehit_frame = -1
        self.current_land_frame = -1
        self.is_facing_right = True
        self.is_attacking = True
        self.attack_choice = None
        self.is_hit = False
        self.is_landing = False

        # Shooting
        self.last_shot_time = 0

        # Stats
        self.health = 10
        self.is_alive = True
        self.is_dying = False

        # Death timer that decides when boss should respawn if it is killed
        self.deathtime = 0  # Reassign this to the time the boss died
        # This decides the minimum amount of time before the boss is allowed to respawn
        self.respawntime = 10000

    def load_sprite_sheets(self):
        """
        Load spritesheet images into sprite frames for animation
        :return: None
        """
        # Flight
        flight_sheet = SpriteSheet(flyeye_flight)
        # Attack
        attack1_sheet = SpriteSheet(flyeye_attack1)
        attack2_sheet = SpriteSheet(flyeye_attack2)
        for i in range(0, 8):
            # Flight
            self.flight_frames_r.append(
                flight_sheet.get_sprite(i * 150, 0, 150, 150))
            self.flight_frames_l.append(pg.transform.flip(
                self.flight_frames_r[i], True, False))
            # Attack
            self.attack1_frames_r.append(
                attack1_sheet.get_sprite(i * 150, 0, 150, 150))
            self.attack1_frames_l.append(pg.transform.flip(
                self.attack1_frames_r[i], True, False))
            self.attack2_frames_r.append(
                attack2_sheet.get_sprite(i * 150, 0, 150, 150))
            self.attack2_frames_l.append(pg.transform.flip(
                self.attack2_frames_r[i], True, False))
        # Take hit
        takehit_sheet = SpriteSheet(flyeye_takehit)
        for i in range(0, 4):
            # Take hit
            self.takehit_frames_r.append(
                takehit_sheet.get_sprite(i * 150, 0, 150, 150))
            self.takehit_frames_l.append(pg.transform.flip(
                self.takehit_frames_r[i], True, False))

        # Death
        death_sheet = SpriteSheet(flyeye_death)
        for i in range(1, 4):
            if i == 1:
                self.death_frames.append(
                    death_sheet.get_sprite(i * 150, 0, 150, 150))
            elif i > 1:
                self.land_frames.append(
                    death_sheet.get_sprite(i * 150, 0, 150, 150))

    def animate(self):
        """
        Animate boss based on state variables initialized in constructor
        :return: None
        """
        current_time = pg.time.get_ticks()
        if self.is_alive:
            if current_time - self.last_frame_update > 100:
                # Flight
                if self.is_facing_right and not self.is_attacking and not self.is_hit:
                    self.last_frame_update = current_time
                    self.current_frame = (
                        self.current_frame + 1) % len(self.flight_frames_r)
                    self.image = self.flight_frames_r[self.current_frame]
                elif not self.is_facing_right and not self.is_attacking and not self.is_hit:
                    self.last_frame_update = current_time
                    self.current_frame = (
                        self.current_frame + 1) % len(self.flight_frames_l)
                    self.image = self.flight_frames_l[self.current_frame]

                # Take hit
                if self.is_facing_right and self.is_hit:
                    self.last_frame_update = current_time
                    self.current_takehit_frame = (
                        self.current_takehit_frame + 1) % len(self.takehit_frames_r)
                    self.image = self.takehit_frames_r[self.current_takehit_frame]
                elif not self.is_facing_right and self.is_hit:
                    self.last_frame_update = current_time
                    self.current_takehit_frame = (
                        self.current_takehit_frame + 1) % len(self.takehit_frames_l)
                    self.image = self.takehit_frames_l[self.current_takehit_frame]
                if self.current_takehit_frame >= len(self.takehit_frames_r) - 1:
                    self.is_hit = False
                    self.current_takehit_frame = 0

            if current_time - self.last_frame_update > 50 and self.attack_choice:
                # Attack
                if self.is_attacking:
                    self.last_frame_update = current_time
                    self.current_attack_frame = (
                        self.current_attack_frame + 1) % len(self.attack_choice)
                    self.image = self.attack_choice[self.current_attack_frame]
                if self.current_attack_frame >= len(self.attack_choice) - 1:
                    self.last_frame_update = current_time
                    self.is_attacking = False
                    self.current_attack_frame = 0

        if current_time - self.last_frame_update > 100 and not self.is_alive and self.is_dying:
            # Death
            if not self.is_landing:
                self.last_frame_update = current_time
                self.image = self.death_frames[0]
            else:
                self.last_frame_update = current_time
                self.current_land_frame += 1
                self.image = self.land_frames[self.current_land_frame]
            if self.current_land_frame >= len(self.land_frames) - 1:
                self.last_frame_update = current_time
                self.is_landing = False
                self.is_dying = False
                self.current_land_frame = 0

    def track_player(self):
        """
        Track the player's x-position so that AI tries to center toward the player
        :return: None
        """
        # Predict and follow player (AI)
        # x-distance from boss to player's x coordinate
        dist_to_player_x = self.game.player.ft_pos.x - self.pos.x
        dist_to_player_x_norm = dist_to_player_x / (SCREEN_WIDTH / 2)
        if dist_to_player_x < 0:
            self.is_facing_right = False
        elif dist_to_player_x > 0:
            self.is_facing_right = True
        self.acc.x += dist_to_player_x_norm * self.BASE_ACC

    def shoot(self):
        """
        Randomly shoot fireball or ice shard every 2 seconds vertically downwards
        :return: None
        """
        now = pg.time.get_ticks()
        if now - self.last_shot_time > 2000:
            self.last_shot_time = now
            # Shoot fireblast or iceshard depending on random
            attack = choice(("attack1", "attack2"))
            if attack == "attack1":
                pg.mixer.Sound(fireball_sound).play().set_volume(0.5)
                FireBall(self.game, self.pos, (0, 5))
            elif attack == "attack2":
                pg.mixer.Sound(iceshard_sound).play().set_volume(0.75)
                IceShard(self.game, self.pos, (0, 10))

            # Choose animation depending on attack
            self.is_attacking = True
            if self.is_facing_right:
                if attack == "attack1":
                    self.attack_choice = self.attack1_frames_r
                elif attack == "attack2":
                    self.attack_choice = self.attack2_frames_r
            elif not self.is_facing_right:
                if attack == "attack1":
                    self.attack_choice = self.attack1_frames_l
                elif attack == "attack2":
                    self.attack_choice = self.attack2_frames_l

    def scroll_with_screen(self):
        """
        Move up the screen if below certain threshold; ensures boss stays at top of screen
        :return: None
        """
        if self.is_alive:
            # Boss moves up screen if it is below certain threshold
            if self.pos.y > 60:
                self.acc.y -= self.BASE_ACC / 3
            if self.pos.y < 30:
                self.acc.y = self.BASE_ACC / 2

    def take_hit(self):
        """
        Sounds and effects for when boss gets hit; also updates health and checks if boss has died from hit
        :return: None
        """
        # Plays hurt animation and updates health if player bullets collide with boss's hitbox
        for proj in self.game.player_proj_sprites:
            if self.hitbox.colliderect(proj.hitbox):
                self.is_hit = True
                BulletImpact(self.game, proj.pos.x, proj.pos.y)
                proj.kill()
                pg.mixer.Sound(fireball_hit_sound).play()
                self.health -= .5
                if self.health < 1:
                    self.is_alive = False
                    self.is_dying = True
                    self.game.score += 1000
                    self.deathtime = pg.time.get_ticks()
                    BossBloodFX(self.game, self.pos.x, self.pos.y)

    def collide_platform(self):
        """
        Used for when boss has died so that boss falls onto the nearest platform below and doesn't clip through;
        called by test_if_dead()
        :return: None
        """
        for platform in self.game.plat_sprites:
            if self.hitbox.colliderect(platform.rect) and self.hitbox.bottom > platform.rect.top:
                if platform.rect.left < self.pos.x < platform.rect.right:
                    self.hitbox.h = 107
                    self.pos.y = platform.rect.top - self.hitbox.h // 2
                    self.vel.y = 0
                    self.is_landing = True

    def test_if_dead(self):
        """
        Applies gravity to boss if dead and respawns boss after a certain amount of time
        :return: None
        """
        if not self.is_alive:
            self.acc = pg.Vector2(0, GRAVITY_ACC)
            self.collide_platform()

            now = pg.time.get_ticks()
            # If the boss is below the screen and the time since its death is greater than respawntime
            if self.pos.y > SCREEN_HEIGHT + self.rect.h // 2 and now - self.deathtime > self.respawntime:
                # Respawn
                self.respawn()

    def respawn(self):
        """
        Respawn boss as a random location outside of visible screen and resets health and state variables
        :return: None
        """
        self.is_alive = True
        self.is_dying = False
        self.health = 10

        spawn_x = randint(0, SCREEN_WIDTH)   # Used for spawning from top and bottom
        spawn_y = randint(0, SCREEN_HEIGHT)  # Used for spawning from left and right
        spawn_loc = choice(((spawn_x, -200),                  # Spawns from top
                            (-200, spawn_y),                  # Spawns from left
                            (SCREEN_WIDTH + 200, spawn_y),    # Spawns from right
                            (spawn_x, SCREEN_HEIGHT + 200)))  # Spawns from bottom
        self.pos = pg.Vector2(spawn_loc)

    def update(self):
        """
        Called in main loop for updating everything (animations, variables, position, etc.)
        :return: None
        """
        self.acc = pg.Vector2(0, 0)
        if self.is_alive:  # Only use these functions if boss health > 0
            self.track_player()
            self.shoot()
            self.take_hit()
        self.scroll_with_screen()
        self.animate()
        self.test_if_dead()

        # Update movement
        self.acc += self.vel * self.FRICTION
        self.vel += self.acc
        self.pos += self.vel + (0.5 * self.acc)

        # Center of rect will be taken as pos
        self.rect.center = self.pos
        self.hitbox.center = self.pos
