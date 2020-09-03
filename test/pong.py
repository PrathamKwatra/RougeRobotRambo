""" Made by Khoa Dang Hoang, professional software developer, student, gamer, professional """
from math import cos, sin, radians
from random import choice, uniform
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = (15, 50)
        self.INIT_POS = (20, Pong.RESOLUTION[1]/2 - size[1]/2)

        # Pygame
        self.image = pygame.Surface(size)
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(topleft=self.INIT_POS)

        # Physics
        self.pos = pygame.Vector2(self.rect.topleft)
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)

        # Score
        self.score = 0

        # Physics constants
        self.MAX_ACC = 1
        self.FRICTION = -0.12

    def reset(self):
        self.rect.topleft = self.INIT_POS
        self.pos = pygame.Vector2(self.INIT_POS)
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)

    def collide_edge(self):
        if self.pos.y < 0:
            self.pos.y = 0
            self.vel.y = 0
        elif self.pos.y > Pong.RESOLUTION[1] - self.rect.height:
            self.pos.y = Pong.RESOLUTION[1] - self.rect.height
            self.vel.y = 0

    def update(self):
        keys = pygame.key.get_pressed()
        self.acc = pygame.Vector2(0, 0)

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.acc.y -= self.MAX_ACC
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.acc.y += self.MAX_ACC

        self.collide_edge()

        self.acc += self.vel * self.FRICTION
        self.vel += self.acc
        self.pos += self.vel + (0.5 * self.acc)

        self.rect.topleft = self.pos


class Computer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = (15, 50)
        self.INIT_POS = (Pong.RESOLUTION[0] - size[0] - 20, Pong.RESOLUTION[1]/2 - size[1]/2)
        self.image = pygame.Surface(size)
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(topleft=self.INIT_POS)

        # Physics
        self.pos = pygame.Vector2(self.rect.topleft)
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)

        # Score
        self.score = 0

        # Constants
        self.MAX_ACC = 2
        self.FRICTION = -0.09

    def reset(self):
        self.rect.topleft = self.INIT_POS
        self.pos = pygame.Vector2(self.INIT_POS)
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)

    def collide_edge(self):
        if self.pos.y < 0:
            self.pos.y = 0
            self.vel.y = 0
        elif self.pos.y > Pong.RESOLUTION[1] - self.rect.height:
            self.pos.y = Pong.RESOLUTION[1] - self.rect.height
            self.vel.y = 0

    def track_ball(self):
        # Predict and follow ball (AI)
        for ball in Pong.ball_sprites:
            if ball.vel.x > 0 or ball.pos.x > Pong.RESOLUTION[0] / 2:
                distance_from_ball_y = (ball.future_pos.y + ball.future_rect.height / 2) - \
                                       (self.pos.y + self.rect.height / 2)
                normed_distance_y = distance_from_ball_y / (Pong.RESOLUTION[1] - self.rect.width/2 - ball.rect.width/2)
                self.acc.y += normed_distance_y * self.MAX_ACC

    def update(self):
        self.acc = pygame.Vector2(0, 0)

        self.track_ball()

        self.collide_edge()

        self.acc += self.vel * self.FRICTION
        self.vel += self.acc
        self.pos += self.vel + (0.5 * self.acc)

        self.rect.topleft = self.pos


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = (15, 15)
        self.CENTER_SCREEN = (Pong.RESOLUTION[0]/2 - size[0]/2, Pong.RESOLUTION[1]/2 - size[1]/2)

        self.image = pygame.Surface(size)
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(topleft=self.CENTER_SCREEN)

        # Misc.
        self.last_collision_time = 0
        self.reset_time = 0
        self.is_paused = False

        # Physics Constants
        self.MAX_SPEED = 12
        self.MAX_BOUNCE_ANGLE = 60

        # Physics
        self.pos = pygame.Vector2(self.rect.topleft)
        self.vel = pygame.Vector2(choice((-0.25, 0.25)) * self.MAX_SPEED,
                                  uniform(-0.25, 0.25) * self.MAX_SPEED)

        # Future invisible ball used for AI to predict ball path
        self.future_speed_scalar = 1.4  # Increase this to improve AI prediction
        self.future_rect = self.rect.copy()
        self.future_pos = pygame.Vector2(self.future_rect.topleft)
        self.future_vel = pygame.Vector2(self.vel.xy * self.future_speed_scalar)

        """ UNCOMMENT THIS TO SHOW INVISIBLE BALL """
        # self.future_image = pygame.Surface((15, 15))
        # self.future_image.fill((0, 255, 0))

    def reset(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.reset_time > 1000:
            self.is_paused = False
            # Paddles
            for paddle in Pong.paddle_sprites:
                paddle.reset()

            # Ball
            self.rect.topleft = self.CENTER_SCREEN
            self.pos = pygame.Vector2(self.CENTER_SCREEN)
            self.vel = pygame.Vector2(choice((-0.25, 0.25)) * self.MAX_SPEED,
                                      uniform(-0.25, 0.25) * self.MAX_SPEED)

            # Future ball
            self.future_rect.topleft = self.CENTER_SCREEN
            self.future_pos = pygame.Vector2(self.CENTER_SCREEN)
            self.future_vel = pygame.Vector2(self.vel.xy * self.future_speed_scalar)

    def collide_edge(self):
        if self.pos.x < 0:
            Pong.computer.score += 1
            self.is_paused = True
            self.reset_time = pygame.time.get_ticks()
        elif self.pos.x > Pong.RESOLUTION[0] - self.rect.width:
            Pong.player.score += 1
            self.is_paused = True
            self.reset_time = pygame.time.get_ticks()
        if self.pos.y < 0:
            self.pos.y = 0
            self.vel.y = -self.vel.y
        elif self.pos.y > Pong.RESOLUTION[1] - self.rect.height:
            self.pos.y = Pong.RESOLUTION[1] - self.rect.height
            self.vel.y = -self.vel.y

        # Future ball
        if self.future_pos.x < 0:
            self.future_pos.x = 0
            self.future_vel.x = 0
            self.future_vel.y = 0
        elif self.future_pos.x > Pong.RESOLUTION[0] - self.future_rect.width:
            self.future_pos.x = Pong.RESOLUTION[0] - self.future_rect.width
            self.future_vel.x = 0
            self.future_vel.y = 0
        if self.future_pos.y < 0:
            self.future_pos.y = 0
            self.future_vel.y = -self.future_vel.y
        elif self.future_pos.y > Pong.RESOLUTION[1] - self.future_rect.height:
            self.future_pos.y = Pong.RESOLUTION[1] - self.future_rect.height
            self.future_vel.y = -self.future_vel.y

    def collide_paddle(self):
        collision = pygame.sprite.spritecollideany(self, Pong.paddle_sprites, False)
        current_time = pygame.time.get_ticks()
        if collision and current_time - self.last_collision_time > 500:
            self.last_collision_time = current_time  # Fixes bug where ball gets stuck on paddle

            self.future_rect.topleft = self.rect.topleft

            # Bounce ball off paddle
            collision_point = collision.rect.clip(self.rect).center
            # Distance from center-y = Center-y of paddle - intersection point
            distance_from_center_y = (collision.pos.y + collision.rect.height / 2) - collision_point[1]
            # Normalized distance from center-y = distance from center-y / half of paddle height
            normed_distance_y = distance_from_center_y / (collision.rect.height / 2)
            # Hit ball at edge -> bigger angle, higher speed
            bounce_angle = normed_distance_y * self.MAX_BOUNCE_ANGLE
            speed = max(abs(normed_distance_y * self.MAX_SPEED), self.MAX_SPEED / 2)
            # Ball speed * cos(max bounce angle) = velocity
            if self.vel.x < 0:
                self.vel.x = speed * cos(radians(bounce_angle))
            else:
                self.vel.x = speed * -cos(radians(bounce_angle))
            self.vel.y = speed * -sin(radians(bounce_angle))

            # Future ball
            self.future_pos = pygame.Vector2(self.pos.xy)
            self.future_vel = pygame.Vector2(self.vel.xy) * self.future_speed_scalar

    def update(self):
        if self.is_paused:
            self.reset()
        else:
            self.collide_paddle()
            self.collide_edge()

            self.pos += self.vel
            self.rect.topleft = self.pos

            # Future ball
            self.future_pos += self.future_vel
            self.future_rect.topleft = self.future_pos


class Interface:
    def __init__(self):
        self.font_name = pygame.font.match_font("arial")

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        Pong.screen.blit(text_surface, text_rect)


class Pong:
    # Constants
    RESOLUTION = (800, 600)
    MAX_FPS = 60
    # Globals
    all_sprites = pygame.sprite.Group()
    paddle_sprites = pygame.sprite.Group()
    ball_sprites = pygame.sprite.Group()
    screen = None
    player = None
    computer = None

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pong")
        Pong.screen = pygame.display.set_mode(Pong.RESOLUTION)
        self.clock = pygame.time.Clock()

        self.is_running = True

        # Sprites
        Pong.player = Player()
        Pong.computer = Computer()
        ball = Ball()
        Pong.all_sprites.add(Pong.player, Pong.computer, ball)
        Pong.paddle_sprites.add(Pong.player, Pong.computer)
        Pong.ball_sprites.add(ball)

        self.interface = Interface()

    def run(self):
        # Game loop
        while self.is_running:
            self.draw()
            self.update()
            self.clock.tick(Pong.MAX_FPS)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    pygame.quit()

    def draw(self):
        Pong.screen.fill((0, 0, 0))
        self.interface.draw_text("{} | {}".format(self.player.score, self.computer.score), 48, (255, 255, 255), Pong.RESOLUTION[0]/2, 50)
        self.all_sprites.draw(Pong.screen)

        """ UNCOMMENT THIS TO SHOW INVISIBLE BALL """
        # for ball in Pong.ball_sprites:
        #    Pong.screen.blit(ball.future_image, ball.future_pos)

        pygame.display.update()

    def update(self):
        self.all_sprites.update()


def main():
    pong = Pong()
    pong.run()


if __name__ == "__main__":
    main()
