# Name: utils.py
# Purpose: Stores the general tools needed for game functions
# Version: 1.1
# Date: 5 June 2020
# Author(s): Khoa Hoang, Adrienne Lhuc Estrella, Pratham Kwatra, Matt Innaurato
# Dependencies: pygame module

import pygame as pg

# NOTE: For .gif files, use an gif to sprite sheet converter (ex: ezgif.com)
class SpriteSheet:
    def __init__(self, image_name):
        """ Takes string argument of file path to sprite sheet"""
        self.image = pg.image.load(image_name).convert_alpha()

    def get_sprite(self, x, y, width, height):
        """
        Get sprite image out of spritesheet image
        :param x: topleft x of image
        :param y: topleft y of image
        :param width: width of image
        :param height: height of image
        :return: None
        """
        # Grab a sprite out of a larger sprite sheet
        sprite = pg.Surface((width, height))
        sprite.blit(self.image, (0, 0), (x, y, width, height))
        sprite = pg.transform.scale2x(sprite)
        sprite.set_colorkey((0, 0, 0))
        return sprite
