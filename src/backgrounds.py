# Name: backgrounds.py
# Purpose: Defines class structures and related methods/attributes for the backgrounds of the game
# Version: 1.1
# Date: 5 June 2020
# Author(s): Khoa Hoang, Adrienne Lhuc Estrella, Pratham Kwatra
# Dependencies: pygame, paths, settings, and random modules

import pygame
from paths import *
from settings import *
from random import randint


class GlacialBackground:
    def __init__(self, game):
        """
        Initalize layers and their corresponding positions on the screen
        :param game: reference to game instance
        """
        self.game = game
        self.layers = []
        self.layer_pos = []  # Position to blit
        self.load_images()

    def load_images(self):
        """
        Load all background layers images into layers list
        :return: None
        """
        image = pygame.image.load(glacial_sky_path).convert_alpha()
        self.layers.append(image)
        image = pygame.image.load(glacial_mountains_path).convert_alpha()
        self.layers.append(image)
        image = pygame.image.load(glacial_clouds_bg_path).convert_alpha()
        self.layers.append(image)
        image = pygame.image.load(glacial_clouds_lonely_path).convert_alpha()
        self.layers.append(image)
        image = pygame.image.load(glacial_clouds_mg_3_path).convert_alpha()
        self.layers.append(image)
        image = pygame.image.load(glacial_clouds_mg_2_path).convert_alpha()
        self.layers.append(image)
        image = pygame.image.load(glacial_clouds_mg_1_path).convert_alpha()
        self.layers.append(image)
        for i in range(0, len(self.layers)):
            if i == 2 or 4 <= i <= 6:
                self.layers[i] = pygame.transform.scale(self.layers[i], (int(SCREEN_WIDTH * 1.3),
                                                                         int(SCREEN_HEIGHT * 1.3)))
                self.layer_pos.append(pygame.Vector2((SCREEN_WIDTH * 1.3 - SCREEN_WIDTH) // -2, 0))
            else:
                self.layers[i] = pygame.transform.scale(self.layers[i], (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.layer_pos.append(pygame.Vector2(0, 0))

    def update(self):
        """
        Update certain layers so that they move
        :return: None
        """
        self.layer_pos[3].x += 0.8  # Move clouds_lonely to the right
        if self.layer_pos[3].x > SCREEN_WIDTH // 2:  # Move clouds_lonely to left of screen
            self.layer_pos[3].x = -SCREEN_WIDTH
            self.layer_pos[3].y = randint(-100, 100)

        # Parallax effect
        # Center parallax layers on player x-position
        self.game.true_scroll[0] += (self.game.player.pos.x - SCREEN_WIDTH * 1.3 // 2 - self.game.true_scroll[0]) // 100
        # Prevent clouds from moving too far left or right
        if self.game.true_scroll[0] > 0:
            self.game.true_scroll[0] = 0
        elif self.game.true_scroll[0] + SCREEN_WIDTH * 1.3 < SCREEN_WIDTH:
            self.game.true_scroll[0] = SCREEN_WIDTH - SCREEN_WIDTH * 1.3
        self.game.true_scroll[1] += int((self.game.player.pos.y-self.game.true_scroll[1]-14-600)/40)

        self.layer_pos[1].x = self.game.true_scroll[0] * 0.0625
        self.layer_pos[2].x = self.game.true_scroll[0] * 0.125
        self.layer_pos[4].x = self.game.true_scroll[0] * 0.25
        self.layer_pos[5].x = self.game.true_scroll[0] * 0.5
        self.layer_pos[6].x = self.game.true_scroll[0]
        self.layer_pos[1].y = self.game.true_scroll[1] * 0.0625
        self.layer_pos[2].y = self.game.true_scroll[1] * 0.125 + 50
        self.layer_pos[4].y = self.game.true_scroll[1] * 0.25 - 125
        self.layer_pos[5].y = self.game.true_scroll[1] * 0.5 - 75
        self.layer_pos[6].y = self.game.true_scroll[1]

    def draw(self):
        """
        Blit all layers onto game screen in correct order at updated positions
        :return: None
        """
        for i in range(len(self.layers)):
            self.game.screen.blit(self.layers[i], self.layer_pos[i])

    def reset(self):
        """
        Used for when the player dies; Resets all layers to original positions
        :return: None
        """
        for i in range(len(self.layer_pos)):
            if i == 2 or 4 <= i <= 6:
                self.layer_pos[i] = pygame.Vector2((SCREEN_WIDTH * 1.3 - SCREEN_WIDTH) // -2, 0)
            else:
                self.layer_pos[i] = pygame.Vector2(0, 0)


"""
class GrassyBackground:
    def __init__(self, game):
        self.game = game
        self.layers = []
        self.load_images()

    def load_images(self):
        image = pygame.image.load(grassy_sky_path).convert_alpha()
        self.layers.append(image)
        image = pygame.image.load(grassy_far_mountains_path).convert_alpha()
        self.layers.append(image)
        image = pygame.image.load(grassy_mountains_path).convert_alpha()
        self.layers.append(image)
        image = pygame.image.load(grassy_clouds_mid_path).convert_alpha()
        self.layers.append(image)
        image = pygame.image.load(grassy_hill_path).convert_alpha()
        self.layers.append(image)
        image = pygame.image.load(grassy_clouds_front_path).convert_alpha()
        self.layers.append(image)
        for i in range(0, len(self.layers)):
            self.layers[i] = pygame.transform.scale(self.layers[i], (SCREEN_WIDTH, SCREEN_HEIGHT))

    def update(self):
        pass
"""
