# Name: main.py
# Purpose: 
#   Handles all initialization of game-related objects, attributes, and events. Controls the main game loop used for updating
#   the game. Houses the Game object used to control all aspects of the game (physics, guns, player, enemies, AI, and graphics)
# Version: 4.0
# Date: 5 June 2020
# Author(s): Khoa Hoang, Adrienne Lhuc Estrella, Pratham Kwatra, Matt Innaurato
# Dependencies: 
#   sys, pygame, random, datetime, paths, settings, 
#   player, boss, platforms, backgrounds, gui, projectiles, 
#   powerups, and enemies modules.


""" RUN GAME FROM THIS MODULE """
# TRY TO AVOID PUTTING GAME LOGIC HERE; USE OTHER MODULES
import sys
import pygame as pg
from random import seed
from datetime import datetime
from paths import *        # File paths
from settings import *     # Constants
from player import *       # Player
from boss import *         # Boss
from platforms import *    # Platformsaa
from backgrounds import *  # Backgrounds
from gui import *          # GUI and menus
from projectiles import *  # Projectiles
from powerups import *     # PowerUps
from enemies import *      # Enemies (not including boss)

""" GAME INFO """
"""
Score increases by 5 for each platform the player passes (below screen)
Score increases by 100 for each enemy slime killed
Score increases by 1000 every time boss is killed
Slimes have 3 health
Boss has 10 health
"""


class Game:
    def __init__(self):
        """
        Main class for running the game; create instance of this class in main script and call run()
        """
        seed(datetime.now())

        pg.init()
        icon = pg.image.load(icon_path)
        pg.display.set_icon(icon)
        pg.display.set_caption(SCREEN_TITLE)
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.events = pg.event.get()

        self.is_running = True  # Used to keep program running
        self.is_playing = True  # Used to track whether player is playing

        # Sprite groups
        self.all_sprites = pg.sprite.Group()          # All
        self.plat_sprites = pg.sprite.Group()         # Platforms
        self.char_sprites = pg.sprite.Group()         # Characters
        self.fx_sprites = pg.sprite.Group()           # Effects
        self.player_proj_sprites = pg.sprite.Group()  # Player bullets
        self.boss_proj_sprites = pg.sprite.Group()    # Boss bullets
        self.gun_sprites = pg.sprite.Group()          # Guns
        self.pow_sprites = pg.sprite.Group()          # PowerUps
        self.enemy_sprites = pg.sprite.Group()        # Enemies (not including boss)

        # Character sprites
        self.player = Player(self)
        self.boss = Boss(self)

        # Spawners for platforms and powerups
        self.power_spawner = PowerSpawner(self)
        self.plat_spawner = PlatformSpawner(self)
        self.enemy_spawner = EnemySpawner(self)

        # Score
        self.score = 0
        self.high_score = 0

        # Background
        self.background = GlacialBackground(self)
        self.true_scroll = [0, 0]

        # GUI
        self.gui = GUI(self)

    def run(self):
        """
        Used to start the run the game; calls all essential functions inside game loop
        :return: None
        """
        with open(high_score_path, "w") as file:
            file.write("0")
        self.gui.draw_start_menu()
        self.plat_spawner.init_game()
        # Game loop for running
        while self.is_running:
            # Inner loop for playing
            while self.is_playing:
                # Main drivers
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(MAX_FPS)
            # Player died; reset game
            self.reset()
        pg.quit()
        sys.exit(0)

    def handle_events(self):
        """
        Handle pygame events like quitting and certain menu keys
        :return: None
        """
        self.events = pg.event.get()
        for event in self.events:
            # Exiting
            if event.type == pg.QUIT:
                self.is_playing = False
                self.is_running = False
            # Bring up menus
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.gui.draw_pause_menu()

    def update(self):
        """
        Update the states and positions of all objects and variables
        :return: None
        """
        self.background.update()
        self.all_sprites.update()
        # self.music.update()
        self.power_spawner.spawn()
        self.plat_spawner.spawn()
        # Player update() is separate to ensure player doesn't clip through stuff
        self.player.update_solo()

    def draw(self):
        """
        Drawing everything in correct order onto the screen
        :return: None
        """
        # Background
        self.background.draw()
        # Sprites
        self.plat_sprites.draw(self.screen)
        for plat in self.plat_sprites:
            plat.draw_inner()
        self.char_sprites.draw(self.screen)
        self.gun_sprites.draw(self.screen)
        self.pow_sprites.draw(self.screen)
        self.fx_sprites.draw(self.screen)
        self.player_proj_sprites.draw(self.screen)
        self.boss_proj_sprites.draw(self.screen)
        # GUI
        self.gui.draw_text("Score: {}".format(self.score),
                           22, (255, 255, 255), (SCREEN_WIDTH/2, 15))
        self.gui.draw_text("Player", 22, (255, 255, 255), (92, 15))
        self.gui.draw_text("Boss", 22, (255, 255, 255), (1160, 15))
        self.gui.draw_health_bar()
        self.gui.draw_ammo_bar()
        self.gui.boss_health_bar()

        """ UNCOMMENT THIS TO SHOW INVISIBLE FUTURE PLAYER"""
        """
        self.screen.blit(self.player.ft_image,
                         (self.player.ft_pos.x - self.player.ft_rect.w/2,
                          self.player.ft_pos.y - self.player.ft_rect.h/2))
        """

        # Update screen
        pg.display.update()

    def reset(self):
        """
        Used for resetting game when player dies
        :return: None
        """
        self.is_playing = True
        for sprite in self.all_sprites:
            sprite.kill()
        self.player = Player(self)  # TODO: Make reset() method for Player
        self.boss = Boss(self)  # TODO: Make reset() method for Boss
        self.score = 0
        self.plat_spawner.init_game()
        self.background.reset()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
