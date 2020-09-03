# Name: platforms.py
# Purpose: Handles the platforms that the player will stand on. This module dictates all methods/attributes associated with the platforms
# Version: 2.1
# Date: 5 June 2020
# Author(s): Khoa Hoang, Matt Innaurato
# Dependencies: pygame, settings, and random modules


import pygame as pg
from settings import *
from random import randint, choice


class PlatformSpawner:
    def __init__(self, game):
        """
        Spawner that determines when and where to spawn new platforms
        :param game: reference to game instance
        """
        self.game = game
        # Determines how far up the player has to travel for powerups to spawn
        self.spawn_dist = randint(120, 360)

    def spawn(self):
        """
        Spawn platform with random position, width, and height after a player has moved up a certain distance
        determined by randint(120, 360); also randomly spawns slime on new platforms
        :return: None
        """
        if self.game.player.scroll_dist_plat > self.spawn_dist:
            self.game.player.scroll_dist_plat = 0
            plat_width = randint(SCREEN_WIDTH // 5, SCREEN_WIDTH // 2)
            plat_pos_x = randint(10, SCREEN_WIDTH - plat_width - 10)
            plat_pos_y = -48
            ptype = choice(("grassy", "icy", "sandy"))
            plat = Platform(self.game, plat_pos_x,
                            plat_pos_y, plat_width, 48, ptype)
            # 25% chance of enemy spawning on platform
            if randint(0, 4) == 0:
                self.game.enemy_spawner.spawn(plat)
            Platform.spawn_dist = randint(120, 360)

    def init_game(self):
        """
        Spawn initial platforms for when player starts the playing the game; Separate from spawn() because player has
        not moved any distance yet
        :return: None
        """
        Platform(self.game, -100, SCREEN_HEIGHT - 48,
                 SCREEN_WIDTH + 200, 96, "grassy")  # Ground
        plat_pos_y = SCREEN_HEIGHT
        # Spawn i more platforms
        for i in range(0, 4):
            plat_width = randint(SCREEN_WIDTH // 5, SCREEN_WIDTH // 2)
            plat_pos_x = randint(10, SCREEN_WIDTH - 10 - plat_width)
            plat_pos_y -= randint(200, 300)
            # New platform created and automatically added to sprite groups
            ptype = choice(("grassy", "icy", "sandy"))
            Platform(self.game, plat_pos_x, plat_pos_y, plat_width, 48, ptype)


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, ptype):
        """
        Platforms for player and enemies to land on; has different type with different colors and friction values
        :param game: reference to game class
        :param x: x-position of topleft of platform
        :param y: y-position of topleft of platform
        :param w: width of platform
        :param h: height of platform
        :param ptype: type of platform as a string that determines the platform's friction and color
        """
        super().__init__()
        self.game = game

        # Add to sprite groups
        self.game.plat_sprites.add(self)
        self.game.all_sprites.add(self)

        # Different platforms have different frictions and colors
        if ptype == "grassy":
            self.friction = -0.1
            color = pg.Color("#417b43")
        elif ptype == "icy":
            self.friction = -0.05
            color = pg.Color("#A5F2F3")
        elif ptype == "sandy":
            self.friction = -0.15
            color = pg.Color("#c2b280")
        else:
            raise ValueError(
                "Invalid platform type. Options: \"grassy\", \"icy\", \"sandy\"")

        self.image = pg.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.margin = 10
        self.inner = pg.Surface((w - self.margin * 2, h - self.margin * 2))
        self.inner.fill(pg.Color("#855E42"))

    def cleanup(self):
        """
        Platforms below screen are removed
        :return: None
        """
        if self.rect.top >= SCREEN_HEIGHT:
            self.kill()
            self.game.score += 5

    def draw_inner(self):
        """
        Draw inner platform to clean up visuals
        :return: None
        """
        self.game.screen.blit(
            self.inner, (self.rect.x + self.margin, self.rect.y + self.margin))

    def update(self):
        """
        Checks for when platform is below screen to cleanup
        :return: None
        """
        self.cleanup()
