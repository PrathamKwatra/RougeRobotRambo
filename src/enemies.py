# Name: enemies.py
# Purpose: Handles the slime enemy that randomly spawns on some platforms
# Version: 3.0
# Date: 5 June 2020
# Author(s): Khoa Hoang
# Dependencies: pygame, settings, random, paths, and projectiles modules

import pygame as pg
from settings import *
from random import randint, choice
from paths import *
from projectiles import BulletImpact


class EnemySpawner:
    def __init__(self, game):
        """
        Spawner for spawning an enemy on a platform
        :param game: reference to game instance
        """
        self.game = game

    def spawn(self, platform):
        """
        Called by platform spawner that species which platform to spawn enemy on
        :param platform: platform for enemy to spawn on
        :return: None
        """
        Enemy(self.game, platform)


# Slime enemy
class Enemy(pg.sprite.Sprite):
    # Pass in platform instance as argument so that enemy spawn on that platform
    def __init__(self, game, platform):
        """
        Slime enemy that randomly spawns on platforms
        Frame lists for animation, physics variables
        :param game: reference to game instance
        :param platform: platform to spawn
        """
        super().__init__()
        self.game = game

        # Add to sprite groups for updating and drawing
        self.game.char_sprites.add(self)
        self.game.enemy_sprites.add(self)
        self.game.all_sprites.add(self)

        # Frames for animations
        self.move_frames_r = []
        self.move_frames_l = []
        self.hurt_frames_r = []
        self.hurt_frames_l = []
        self.die_frames_r = []
        self.die_frames_l = []
        self.attack_frames_r = []
        self.attack_frames_l = []
        self.load_frames()

        # For drawing through pygame
        self.image = self.move_frames_r[0]
        self.rect = self.image.get_rect(midbottom=(randint(platform.rect.centerx - platform.rect.w // 3,
                                                           platform.rect.centerx + platform.rect.w // 3),
                                                   platform.rect.top))

        # Vectors for realistic movement
        self.pos = pg.Vector2(self.rect.midbottom)
        self.vel = pg.Vector2(0, 0)
        self.acc = pg.Vector2(0, 0)

        # For movement
        self.base_acc = 0.25
        self.friction = -0.12

        # For animations
        self.last_frame_update = 0
        self.current_frame = -1
        self.curr_hurt_frame = -1
        self.curr_attk_frame = -1
        self.curr_die_frame = -1
        self.is_hurt = False
        self.is_attacking = False
        self.is_dying = False

        # Hitbox for getting hit
        self.hitbox = None

        # Stats
        self.maxhealth = 3
        self.health = 3
        self.attk_rate = 1000
        self.last_attk_time = 0

        # Current platform
        self.current_platform = platform

        self.face_direction = choice((-1, 1))  # -1 -> left, 1 -> right

        self.init_hitbox(self.rect.w - 20, self.rect.h)

    def init_hitbox(self, w, h):
        """
        Initialize hitbox to be used for collisions; Used for easy inheritance to other enemies
        :param w: width of hitbox
        :param h: height of hitbox
        :return: None
        """
        self.hitbox = pg.Rect((self.rect.centerx - w // 2, self.rect.centery - h // 2),
                              (w, h))  # Center the hitbox on the projectile sprite

    def load_frames(self):
        """
        Load images for sprite frames for animations onto frame lists declared in constructor
        :return: None
        """
        for i in range(0, 4):
            # Move sprite
            moveimg = pg.image.load(slime_move[i]).convert_alpha()
            moveimg = pg.transform.scale(moveimg, (64, 64))
            self.move_frames_l.append(moveimg)
            self.move_frames_r.append(pg.transform.flip(self.move_frames_l[i], True, False))
            # Hurt sprite
            hurtimg = pg.image.load(slime_hurt[i]).convert_alpha()
            hurtimg = pg.transform.scale(hurtimg, (64, 64))
            self.hurt_frames_l.append(hurtimg)
            self.hurt_frames_r.append(pg.transform.flip(self.hurt_frames_l[i], True, False))
            # Die sprite
            dieimg = pg.image.load(slime_die[i]).convert_alpha()
            dieimg = pg.transform.scale(dieimg, (64, 64))
            self.die_frames_l.append(dieimg)
            self.die_frames_r.append(pg.transform.flip(self.die_frames_l[i], True, False))
            # Attack sprite
            attackimg = pg.image.load(slime_attack[i]).convert_alpha()
            attackimg = pg.transform.scale(attackimg, (64, 64))
            self.attack_frames_l.append(attackimg)
            self.attack_frames_r.append(pg.transform.flip(self.attack_frames_l[i], True, False))

    def animate(self):
        """
        Animation enemy sprite based on state variables and frame lists declared in constructor
        :return: None
        """
        curr_time = pg.time.get_ticks()
        if curr_time - self.last_frame_update > 100:
            self.last_frame_update = curr_time
            # Move left
            if self.face_direction == -1 and not self.is_hurt:
                self.current_frame = (self.current_frame + 1) % len(self.move_frames_l)
                self.image = self.move_frames_l[self.current_frame]
            # Move right
            elif self.face_direction == 1 and not self.is_hurt:
                self.current_frame = (self.current_frame + 1) % len(self.move_frames_r)
                self.image = self.move_frames_r[self.current_frame]
            # Hurt left
            if self.face_direction == -1 and self.is_hurt:
                self.curr_hurt_frame = (self.curr_hurt_frame + 1) % len(self.hurt_frames_l)
                self.image = self.hurt_frames_l[self.current_frame]
            # Hurt right
            elif self.face_direction == 1 and self.is_hurt:
                self.curr_hurt_frame = (self.curr_hurt_frame + 1) % len(self.hurt_frames_r)
                self.image = self.hurt_frames_r[self.current_frame]
            # Cancel hurt animation if played once
            if self.curr_hurt_frame >= len(self.hurt_frames_l) - 1:
                self.is_hurt = False
                self.curr_hurt_frame = 0
            # Attack left
            if self.face_direction == -1 and self.is_attacking:
                self.curr_attk_frame += 1
                self.image = self.attack_frames_l[self.current_frame]
            # Attack right
            elif self.face_direction == 1 and self.is_attacking:
                self.curr_attk_frame += 1
                self.image = self.attack_frames_r[self.current_frame]
            # Cancel attack animation if played once
            if self.curr_attk_frame >= len(self.attack_frames_l) - 1:
                self.is_attacking = False
                self.curr_attk_frame = 0
            # Die left
            if self.face_direction == -1 and self.is_dying:
                self.curr_die_frame += 1
                self.image = self.die_frames_l[self.curr_die_frame]
            # Die right
            elif self.face_direction == 1 and self.is_dying:
                self.curr_die_frame += 1
                self.image = self.die_frames_r[self.curr_die_frame]
            # Delete slime from memory if last die frame is reached
            if self.curr_die_frame >= len(self.attack_frames_l) - 1:
                # Increase player score
                self.game.score += 100
                self.kill()

    def cleanup(self):
        """
        Kill slime and update point if slime is below the screen
        :return: None
        """
        if self.pos.y > SCREEN_HEIGHT + self.rect.h // 2:
            # If slime is falling, this means player has knocked slime off
            if self.vel.y > 5 and self.health < self.maxhealth:
                self.game.score += 100  # Player gets points for killing slime
            self.kill()

    def collide_platform(self):
        """
        Allows slime to stand on platform while being affected by gravity without clipping through
        :return: None
        """
        self.rect.y += 1
        collisions = pg.sprite.spritecollide(self, self.game.plat_sprites, False)
        self.rect.y -= 1
        if collisions:
            lowest_platform = collisions[0]
            for platform in collisions:
                if platform.rect.y > lowest_platform.rect.y:
                    lowest_platform = platform
            if lowest_platform != self.current_platform:
                self.current_platform = lowest_platform

            if self.current_platform.rect.left < self.pos.x < self.current_platform.rect.right:
                self.pos.y = lowest_platform.rect.top
                self.vel.y = 0
                self.friction = self.current_platform.friction

    def move(self):
        """
        Move slime back and forth on platform
        :return: None
        """
        # This method makes enemy pace back and forth on platform
        # Turn around
        if self.pos.x < self.current_platform.rect.centerx - self.current_platform.rect.w // 3:
            self.face_direction = 1   # will face to the right
        if self.pos.x > self.current_platform.rect.centerx + self.current_platform.rect.w // 3:
            self.face_direction = -1  # Will face to the left

        # Move
        self.acc.x += self.face_direction * self.base_acc

    def take_hit(self):
        """
        Updates health if player hits slime and spawns bullet impact effect
        :return: None
        """
        for proj in self.game.player_proj_sprites:
            if self.hitbox.colliderect(proj.hitbox):
                if proj.pos.x < self.pos.x:  # Hit from the left
                    self.vel.x += 10
                elif proj.pos.x > self.pos.x:  # Hit from the right
                    self.vel.x -= 10
                self.health -= 1
                BulletImpact(self.game, proj.pos.x, proj.pos.y)
                proj.kill()
                self.is_hurt = True

    def hit_player(self):
        """
        Tests for collision with player and decreases player health if colliding
        :return: None
        """
        curr_time = pg.time.get_ticks()
        # If player is touching slime
        if self.hitbox.colliderect(self.game.player.hitbox) and curr_time - self.last_attk_time > self.attk_rate:
            self.last_attk_time = curr_time
            # Slime plays attacking animation
            self.is_attacking = True
            # Player loses health
            self.game.player.health -= .5
            # If player is left of slime
            if self.game.player.pos.x < self.pos.x:
                # Knock player to the left
                self.game.player.vel.x = -20
            # Player is right of slime
            elif self.game.player.pos.x > self.pos.x:
                # Knock player to the right
                self.game.player.vel.x = 20
            self.game.player.sound_fx.hurt.play()

    def test_if_dead(self):
        """
        Tests if health is at zero; set animation state variable is_dying to True so that dying animation plays
        :return: None
        """
        if self.health < 1:
            self.is_dying = True

    def update(self):
        """
        Update slime position, health, state, etc.; called by main loop
        :return: None
        """
        self.acc = pg.Vector2(0, GRAVITY_ACC)
        if not self.is_dying:
            self.cleanup()
            self.move()
            self.take_hit()
            self.hit_player()
            self.test_if_dead()
        self.animate()
        self.collide_platform()

        # Update movement
        self.acc.x += self.vel.x * self.friction
        self.vel += self.acc
        self.pos += self.vel + (0.5 * self.acc)

        # Midbottom of rect will be taken as pos
        self.rect.midbottom = self.pos
        self.hitbox.midbottom = self.pos

