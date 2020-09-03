# Name: powerups.py
# Purpose: Controls the spawning and methods/attributes related to the powerups that spawn on platforms
# Version: 1.2
# Date: 5 June 2020
# Author(s): Khoa Hoang
# Dependencies: pygame, random, settings, and paths modules

import pygame as pg
from random import randint, choice
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from paths import health_path, ammo_path


class PowerSpawner:
    def __init__(self, game):
        """
        Used to spawn platforms after player has moved up a certain distance
        :param game: reference to game instance
        """
        self.game = game
        # Determines how far up the player has to travel for powerups to spawn
        self.spawn_dist = randint(1000, 1500)

    def spawn(self):
        """
        Spawn platform at random position
        :return: None
        """
        if self.game.player.scroll_dist_pow > self.spawn_dist:
            self.game.player.scroll_dist_pow = 0
            pow_choice_str = choice(("ammo", "health"))
            pow_choice = None
            if pow_choice_str == "ammo":
                pow_choice = Ammo(self.game)
            elif pow_choice_str == "health":
                pow_choice = Health(self.game)
            pow_choice.rect.center = (randint(0, SCREEN_WIDTH), -pow_choice.rect.h)
            # Ensures powerups don't spawn inside platforms
            collision = pg.sprite.spritecollideany(pow_choice, self.game.plat_sprites)
            if collision:
                pow_choice.rect.bottom = collision.rect.top - 10

            self.spawn_dist = randint(1000, 1500)


# This class is to be inherited by different powerup types
class PowerUp(pg.sprite.Sprite):
    def __init__(self, game):
        """
        PowerUp class to be inherited that update player statistics when player touches them
        :param game: reference to game instance
        """
        super().__init__()
        self.game = game
        self.game.all_sprites.add(self)
        self.game.pow_sprites.add(self)

        self.frames = []
        self.load_frames()

        self.last_frame_update = 0
        self.current_frame = 0
        self.frame_delay = 100

        self.image = pg.Surface((24, 24))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()

    def load_frames(self):
        """
        load images into frame list
        :return:
        """
        pass

    def animate(self):
        """
        Animate frames (if applicable)
        :return:
        """
        pass

    def cleanup(self):
        """
        If platform is below screen, delete from memory
        :return: None
        """
        if self.rect.top >= SCREEN_HEIGHT:
            self.kill()

    def give_player(self):
        """
        Update player stats when player touches
        :return:
        """
        pass

    def update(self):
        """
        Update powerup with functions initalized before
        :return:
        """
        self.cleanup()
        self.animate()
        self.give_player()


class Ammo(PowerUp):
    def __init__(self, game):
        """
        Increase player ammo
        :param game: reference to game instance
        """
        super().__init__(game)
        self.image = pg.image.load(ammo_path)
        self.image = pg.transform.scale(self.image, (24, 24))
        self.image.set_colorkey((255, 255, 255))

    def give_player(self):
        """
        Increase player ammo by 5
        :return: None
        """
        player_collide = pg.sprite.collide_rect(self, self.game.player)
        if player_collide:
            self.game.player.gun.ammo += 5
            if self.game.player.gun.ammo > self.game.player.gun.maxammo:
                self.game.player.gun.ammo = self.game.player.gun.maxammo
            self.kill()


class Health(PowerUp):
    def __init__(self, game):
        """
        Increase player health
        :param game: reference to game instance
        """
        super().__init__(game)
        self.image = pg.image.load(health_path)
        self.image = pg.transform.scale(self.image, (24, 24))
        self.image.set_colorkey((255, 255, 255))

    def give_player(self):
        """
        Increase player health by 5
        :return: None
        """
        player_collide = pg.sprite.collide_rect(self, self.game.player)
        if player_collide:
            self.game.player.health += 5
            if self.game.player.health > self.game.player.maxhealth:
                self.game.player.health = self.game.player.maxhealth
            self.kill()


"""
class HigherJump(PowerUp):
    def give_player(self):
        player_collide = pg.sprite.collide_rect(self, self.game.player)
        if player_collide:
            self.game.player.higher_jump = True
            self.kill()


class TripleJump(PowerUp):
    def give_player(self):
        player_collide = pg.sprite.collide_rect(self, self.game.player)
        if player_collide:
            self.game.player.triple_jump = True
            self.kill()
"""

