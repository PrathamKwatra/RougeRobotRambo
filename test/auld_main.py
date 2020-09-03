import pygame
from random import randint
from file_paths import *
from settings import *
from player import *
from platforms import *
from gui import *
from score import *
from backgrounds import *
# NOTE: In PyCharm, there will be red highlights in import statements
# Resolve by right-clicking on src/ folder and Mark Directory as -> Sources Root
# WARNING: Do NOT use .mp3 files as there is limited support in pygame
# ... It's okay to use .wav files, but they are uncompressed and can get large
# ... OGG files are best because audio is compressed, but as a result the sounds might now be best

true_scroll=[0,0]


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
        pygame.display.set_caption(SCREEN_TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.events = pygame.event.get()

        self.is_running = True  # Keeps the game running
        self.is_playing = True  # Keeps track of whether they player is playing while game is running

        # Sprites
        self.all_sprites = pygame.sprite.Group()  # Used mainly for drawing and updating all sprites
        self.platform_sprites = pygame.sprite.Group()
        self.character_sprites = pygame.sprite.Group()
        self.fx_sprites = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.character_sprites.add(self.player)

        # Score
        self.high_score = 0
        self.score = 0

        # Menus and GUI
        self.gui = GUI(self)

        self.background = GlacialBackground(self)

    def run(self):
        self.gui.draw_start_menu()

        """ GAME LOOP """
        while self.is_running:
            # TODO: purge this trash
            for plat_args in PLATFORM_LIST:
                plat = Platform(*plat_args)
                self.all_sprites.add(plat)
                self.platform_sprites.add(plat)

            """ INNER LOOP """
            while self.is_playing:
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(MAX_FPS)
            self.reset()

    # Methods below are all contained within game loop

    def reset(self):
        """ Start new game """
        self.is_playing = True
        self.all_sprites.empty()
        self.player.reset()

        for plat_args in PLATFORM_LIST:
            plat = Platform(*plat_args)
            self.all_sprites.add(plat)
            self.platform_sprites.add(plat)

        self.all_sprites.add(self.player)
        self.character_sprites.add(self.player)

    def handle_events(self):
        """ Handle pygame events"""
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.is_playing = False
                self.is_running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_h:
                    pass
                    self.gui.draw_score_menu()
                elif event.key == pygame.K_p:
                    self.gui.draw_pause_menu()

    def update(self):
        """ Update sprites"""
        # If player reaches top quarter of screen, scroll screen up
        if self.player.rect.top <= SCREEN_HEIGHT / 4:
            # Move player down
            self.player.pos.y += abs(self.player.vel.y)
            # Move platforms down
            for platform in self.platform_sprites:
                platform.rect.y += abs(self.player.vel.y)
                if platform.rect.top >= SCREEN_HEIGHT:
                    platform.kill()
                    # self.score += Score(10, ScoreType.FALL_DEATH)
            # Move fx sprites down
            for fx in self.fx_sprites:
                fx.rect.y += abs(self.player.vel.y)
            # Update background
            # TODO: Make backgound change slightly every time screen scrolls up to simulate climbing feeling

        # Spawn new platforms to keep similar number of platforms
        while len(self.platform_sprites) < 6:
            platform_width = randint(500, 1000)
            platform = Platform((randint(0, SCREEN_WIDTH - platform_width), randint(-30, -10)),
                                (platform_width, 32))
            self.platform_sprites.add(platform)
            self.all_sprites.add(platform)
        # If player falls below bottom of screen, player dies
        if self.player.rect.top > SCREEN_HEIGHT:
            # Camera scrolls down suddenly
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platform_sprites) == 0:
            self.is_playing = False
            self.gui.draw_game_over_menu()

        self.all_sprites.update()

    def draw(self):
        """ Draw updated screen """
        for layer in self.background.layers:
            self.screen.blit(layer, (true_scroll[0], true_scroll[1]))
        self.gui.draw_text("Score: {}".format(self.score), 22, (255, 255, 255), (SCREEN_WIDTH/2, 15))
        
        self.gui.draw_health_bar()
        self.gui.draw_ammo_bar()

        true_scroll[0] += int((self.player.rect.x-true_scroll[0]-16-595)/20)
        true_scroll[1] += int((self.player.rect.y-true_scroll[1]-14-380)/20)
        self.platform_sprites.draw(self.screen)
        self.fx_sprites.draw(self.screen)
        self.character_sprites.draw(self.screen)
        pygame.display.update()


def main():
    game = Game()
    game.run()
    pygame.quit()


if __name__ == "__main__":
    main()
