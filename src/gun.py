# Name: gun.py
# Purpose: Implements the gun's visible effects and handles all gun related actions/attributes/graphics
# Version: 1.7
# Date: 5 June 2020
# Author(s): Khoa Hoang
# Dependencies: pygame, settings, paths, and projectiles modules

import pygame as pg
from settings import *
from paths import *
from projectiles import *


# Unlike other FX classes, this one sticks to the "gun"
class GunFX(pg.sprite.Sprite):
    def __init__(self, game, gun):
        """
        Fire effect that is attached to the "gun" (Not a child of FX class because animation loops
        :param game: reference to game instance
        :param gun: gun sprite object
        """
        super().__init__()
        self.game = game
        self.gun = gun

        self.game.gun_sprites.add(self)
        self.game.all_sprites.add(self)

        # Animation frames
        self.frames = []
        self.load_frames()

        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom=(self.gun.pos.x, self.gun.pos.y - self.gun.rect.h / 5))

        # Animation frames
        self.last_frame_update = 0
        self.frame_delay = 50
        self.current_frame = -1

    def load_frames(self):
        """
        Load frame images into frame list
        :return: None
        """
        for filepath in fire:
            img = pg.image.load(filepath).convert_alpha()
            img = pg.transform.scale(img, (40, 40))
            self.frames.append(img)

    def update(self):
        """
        Update frame animation using frame list and variables
        :return: None
        """
        current_time = pg.time.get_ticks()
        if current_time - self.last_frame_update > self.frame_delay:
            self.last_frame_update = current_time
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

        # Attach midbottom to top of gun sprite
        self.rect.midbottom = (self.gun.pos.x, self.gun.pos.y - self.gun.rect.h / 5)


class Gun(pg.sprite.Sprite):
    # Can be attached to a character sprite
    def __init__(self, game, char):
        """
        Gun sprite class to be used by player for shooting bullet projectiles
        :param game: reference to game instance
        :param char: character to attach to (currently only player)
        """
        super().__init__()
        self.game = game
        self.char = char

        self.game.gun_sprites.add(self)
        self.game.all_sprites.add(self)

        # Frame list
        self.frames = []
        self.load_frames()
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(char.pos.x, char.pos.y - char.rect.h/2))

        # For animations
        self.last_frame_update = 0
        self.current_frame = -1

        self.rect = self.image.get_rect(center=(char.pos.x, char.pos.y - char.rect.h/2))
        # Position relative to character (NOT the actual coordinate position of gun); used as direction
        self.attach_pos = pg.Vector2(1, 1)
        # Actual position (center of sprite)
        self.pos = pg.Vector2((char.pos.x, char.pos.y - char.rect.h/2))

        # For shooting
        self.shot_delay = 200
        self.last_shot_time = pg.time.get_ticks()
        self.bullet_speed = 6
        self.ammo = 10
        self.maxammo = 10

        # FX
        GunFX(self.game, self)

    def load_frames(self):
        """
        Load frame images into frame list
        :return: None
        """
        for filepath in bullet_path:
            img = pg.image.load(filepath).convert_alpha()
            img = pg.transform.scale(img, (30, 30))
            self.frames.append(img)

    def animate(self):
        """
        Animate spinning animation while player is holding
        :return: None
        """
        current_time = pg.time.get_ticks()
        if current_time - self.last_frame_update > 100:
            self.last_frame_update = current_time
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def shoot(self):
        """
        Shoot bullet sprite out of gun with direction depending on position relative to player
        :return: None
        """
        pressed = pg.key.get_pressed()
        current_time = pg.time.get_ticks()
        if self.ammo > 0 and (pressed[pg.K_UP] or pressed[pg.K_LEFT] or pressed[pg.K_DOWN] or pressed[pg.K_RIGHT]) \
                and (current_time - self.last_shot_time > self.shot_delay):
            self.last_shot_time = current_time

            Bullet(self.game, self.rect.center, self.attach_pos)
            self.ammo -= 1

    def update(self):
        """
        Update gun position based on keys; gun will circle around player char
        :return: None
        """
        pressed = pg.key.get_pressed()
        self.animate()

        # Moves gun with player (WASD)
        if not pressed[pg.K_UP] and not pressed[pg.K_LEFT] and not pressed[pg.K_DOWN] and not pressed[pg.K_RIGHT]:
            if pressed[pg.K_w]:
                self.attach_pos += (0, -1)
            if pressed[pg.K_a]:
                self.attach_pos += (-1, 0)
            if pressed[pg.K_s]:
                self.attach_pos += (0, 1)
            if pressed[pg.K_d]:
                self.attach_pos += (1, 0)

        # Moves gun when aiming (Arrow keys)
        if pressed[pg.K_LEFT]:
            self.attach_pos += (-3, 0)
        if pressed[pg.K_RIGHT]:
            self.attach_pos += (3, 0)
        if pressed[pg.K_UP]:
            self.attach_pos += (0, -1)
        if pressed[pg.K_DOWN]:
            self.attach_pos += (0, 1)

        # Normalization ensures consistent movement
        if self.attach_pos.length() > 0.1:
            self.attach_pos.scale_to_length(40)

        # Adjust num in (self.pos[i] * num) for distance from player
        self.pos.x = self.char.pos.x + self.attach_pos[0]
        self.pos.y = self.char.pos.y - self.char.rect.h/2 + self.attach_pos[1]

        # Shoot
        if self.attach_pos.length() > 0.1:
            self.attach_pos.scale_to_length(self.bullet_speed)
            self.shoot()
            self.attach_pos.scale_to_length(3)  # Make this number smaller to increase gun move speed

        # Center of rect will be taken as pos
        self.rect.center = self.pos
