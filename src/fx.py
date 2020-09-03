# Name: fx.py
# Purpose: Implements the abstract base class for most FX-related classes
# Version: 1.9
# Date: 5 June 2020
# Author(s): Khoa Hoang
# Dependencies: pygame and abc modules

import pygame as pg
import abc


# FX sprites only play animation once and then get killed
class FX(pg.sprite.Sprite, abc.ABC):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game

        self.game.all_sprites.add(self)
        self.game.fx_sprites.add(self)

        # Animation frames
        self.frames = []
        self.load_frames()

        self.image = pg.Surface((16, 16))
        self.image.fill((0, 0, 0))
        self.rect = pg.Rect(x, y, 16, 16)

        # Animation variables
        self.last_frame_update = 0
        self.current_frame = 0
        self.frame_delay = 100

    @abc.abstractmethod
    def load_frames(self):
        # To be implemented by children
        pass

    def update(self):
        """
        Update frames and kill once last frame is drawn
        :return:
        """
        current_time = pg.time.get_ticks()
        if current_time - self.last_frame_update > self.frame_delay:
            self.last_frame_update = current_time
            self.image = self.frames[self.current_frame]
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.kill()
