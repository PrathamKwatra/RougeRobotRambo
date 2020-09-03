# Name: projectiles.py
# Purpose: Handles all projectile (bullets, fireballs, iceshards) movement and their collisions
# Version: 1.4
# Date: 5 June 2020
# Author(s): Khoa Hoang
# Dependencies: pygame, settings, utils, paths, fx, and abc modules


import pygame as pg
from settings import *
from utils import *
from paths import *
from fx import *
from abc import ABC, abstractmethod


# To be inherited
class Projectile(pg.sprite.Sprite, ABC):
    # vel includes both magnitude and direction
    def __init__(self, game, pos=(0, 0), vel=(0, 0)):
        """
        Abstract base class for different projectiles
        :param game: reference to game instance
        :param pos: initial spawn position
        :param vel: initial spawn position
        """
        super().__init__()
        self.game = game

        self.game.all_sprites.add(self)

        self.image = pg.Surface((8, 8))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=pos)

        self.pos = pg.Vector2(self.rect.center)
        self.vel = pg.Vector2(vel)

        # For animations and sprites images with child classes
        self.frames = []
        self.load_frames()
        self.last_frame_update = 0
        self.current_frame = -1

        # Hitbox (Change these statements to adjust hitbox)
        self.hitbox = None

    def init_hitbox(self, w, h):  # Width and height of hitbox: CALL THIS METHOD IN CHILD CLASS
        """
        Initialize size of hitbox
        :param w: width of hitbox
        :param h: height of hitbox
        :return: None
        """
        self.hitbox = pg.Rect((self.rect.centerx - w // 2, self.rect.centery - h // 2),
                              (w, h))  # Center the hitbox on the projectile sprite

    def load_frames(self):
        """
        Load images into frame lists
        :return: None
        """
        pass

    def cleanup(self):
        """
        Remove bullet from memory if it is above or below the top or bottom of screen, respectively
        :return: None
        """
        if self.pos.y < -self.rect.h/2 or self.pos.y > SCREEN_HEIGHT + self.rect.h/2:
            self.kill()

    def move(self):
        """
        Move projectile
        :return: None
        """
        self.pos += self.vel
        self.rect.center = self.pos
        self.hitbox.center = self.pos

    def animate(self):
        """
        Animate Projectile
        :return: None
        """
        pass

    def update(self):
        """
        Update projectile using initalized functions
        :return: None
        """
        self.cleanup()
        self.move()
        self.animate()


class BulletImpact(FX):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.frame_delay = 50

    def load_frames(self):
        sheet = SpriteSheet(bulletimpact)
        for i in range(0, 8):
            self.frames.append(sheet.get_sprite(i * 48, 0, 48, 48))
            self.frames[i] = pg.transform.scale(self.frames[i], (40, 40))


class BulletBounceFX(FX):
    # bounce_off is a string that determines whether the left or right sprite will be loaded
    def __init__(self, game, x, y, bounce_off):
        self.bounce_off = bounce_off
        super().__init__(game, x, y)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

    def load_frames(self):
        if self.bounce_off == "left":
            for filepath in bulletbounce:
                img = pg.image.load(filepath).convert_alpha()
                img = pg.transform.scale(img, (40, 40))
                img = pg.transform.flip(img, True, False)
                self.frames.append(img)
        elif self.bounce_off == "right":
            for filepath in bulletbounce:
                img = pg.image.load(filepath).convert_alpha()
                img = pg.transform.scale(img, (40, 40))
                self.frames.append(img)


class Bullet(Projectile):
    def __init__(self, game, pos=(0, 0), vel=(0, 0)):
        super().__init__(game, pos, vel)

        self.game.player_proj_sprites.add(self)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)

        self.init_hitbox(self.rect.w, self.rect.h)

    def load_frames(self):
        for filepath in bullet_path:
            img = pg.image.load(filepath).convert_alpha()
            img = pg.transform.scale(img, (20, 20))
            self.frames.append(img)

    def animate(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_frame_update > 100:
            self.last_frame_update = current_time
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def bounce(self):
        """ Bounce on sides of screen """
        if self.pos.x <= self.rect.w / 2:
            self.vel.x = -self.vel.x
            BulletBounceFX(self.game, self.pos.x, self.pos.y, "left")
            pg.mixer.Sound(fireball_hit_sound).play()
        if self.pos.x >= SCREEN_WIDTH - self.rect.w / 2:
            self.vel.x = -self.vel.x
            BulletBounceFX(self.game, self.pos.x, self.pos.y, "right")
            pg.mixer.Sound(fireball_hit_sound).play()

    def update(self):
        super().update()
        self.bounce()


class FireBallFX(FX):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(midtop=(x, y))

        self.frame_delay = 50

    def load_frames(self):
        sheet = SpriteSheet(fireballfx)
        for i in range(0, 12):
            self.frames.append(sheet.get_sprite(i * 128, 0, 128, 128))
            self.frames[i] = pg.transform.scale(self.frames[i], (80, 80))
            self.frames[i] = pg.transform.flip(self.frames[i], False, True)


class FireBallImpact(FX):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

    def load_frames(self):
        sheet = SpriteSheet(fireballimpact)
        for i in range(0, 8):
            self.frames.append(sheet.get_sprite(i * 64, 0, 64, 64))
            self.frames[i] = pg.transform.scale(self.frames[i], (80, 80))


class FireBall(Projectile):
    def __init__(self, game, pos=(0, 0), vel=(0, 0)):
        super().__init__(game, pos, vel)

        self.game.boss_proj_sprites.add(self)

        FireBallFX(game, pos[0], pos[1])

        self.image = self.frames[0]
        self.rect = self.image.get_rect(midtop=pos)

        self.init_hitbox(self.rect.w - 55, self.rect.h - 55)

    def load_frames(self):
        for filepath in fireball:
            img = pg.image.load(filepath).convert()
            img = pg.transform.scale2x(img)
            img = pg.transform.rotate(img, -90)
            self.frames.append(img)

    def animate(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_frame_update > 100:
            self.last_frame_update = current_time
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]


class IceShardFX(FX):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

    def load_frames(self):
        for filepath in iceshardfx:
            img = pg.image.load(filepath).convert_alpha()
            img = pg.transform.scale(img, (96, 96))
            img = pg.transform.rotate(img, -90)
            self.frames.append(img)


class IceShardImpact(FX):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.frame_delay = 200

    def load_frames(self):
        for filepath in iceshardimpact:
            img = pg.image.load(filepath).convert_alpha()
            img = pg.transform.scale(img, (96, 96))
            img = pg.transform.rotate(img, -90)
            self.frames.append(img)


class IceShard(Projectile):
    def __init__(self, game, pos=(0, 0), vel=(0, 0)):
        super().__init__(game, pos, vel)

        self.game.boss_proj_sprites.add(self)

        IceShardFX(game, pos[0], pos[1])

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)

        self.init_hitbox(self.rect.w - 100, self.rect.h - 60)

    def load_frames(self):
        img = pg.image.load(iceshard).convert_alpha()
        img = pg.transform.scale(img, (96, 96))
        img = pg.transform.rotate(img, -90)
        self.frames.append(img)

