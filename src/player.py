# Name: player.py
# Purpose: Controls all methods/attributes related to the player. Also controls the graphics and FX of the player.
# Version: 3.0
# Date: 5 June 2020
# Author(s): Khoa Hoang, Matt Innaurato, Adrienne Lhuc Estrella
# Dependencies: pygame, paths, settings, utils, projectiles, gun, and fx modules


import pygame
from paths import *
from settings import *
from utils import *
from projectiles import *
from gun import *
from fx import *


class PlayerJumpFX(FX):
    def __init__(self, game, x, y):
        """
        Jump dash effect when player lifts off the ground after jumping
        :param game: reference to game instance
        :param x: x-position to spawn
        :param y: y-position to spawn
        """
        super().__init__(game, x, y)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.frame_delay = 50

    def load_frames(self):
        """
        Load frame images onto frame list
        :return: None
        """
        sheet = SpriteSheet(player_jump_fx_path)
        for i in range(0, 6):
            self.frames.append(sheet.get_sprite(i * 28, 0, 28, 28))


class PlayerLandFX(FX):
    def __init__(self, game, x, y):
        """
        Jump dust effect that plays when player lands
        :param game: reference to game instance
        :param x: x-position to spawn
        :param y: y-position to spawn
        """
        super().__init__(game, x, y)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom=(x, y))

    def load_frames(self):
        """
        Load frame images in frame list
        :return: None
        """
        # Land FX
        sheet = SpriteSheet(player_land_fx_path)
        for i in range(0, 4):
            self.frames.append(sheet.get_sprite(i * 44, 0, 44, 32))


class PlayerSoundFX:
    def __init__(self):
        """
        Contains sound effects to play when jumping and hurt
        """
        self.jump = pygame.mixer.Sound(jump_sound_path)
        self.hurt = pygame.mixer.Sound(pain_sound_path)


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        """
        Player class to be controlled by player
        :param game: reference to game instance
        """
        super().__init__()
        self.game = game

        # Add to sprite groups
        self.game.char_sprites.add(self)
        self.game.all_sprites.add(self)

        self.sound_fx = PlayerSoundFX()

        # Initialize sprite sheets and frame lists
        self.idle_frames_r = []
        self.idle_frames_l = []
        self.walk_frames_r = []
        self.walk_frames_l = []
        self.jump_frames_r = []
        self.jump_frames_l = []
        self.fall_frames_r = []
        self.fall_frames_l = []
        self.land_frames_r = []
        self.land_frames_l = []
        self.hurt_frames_r = []
        self.hurt_frames_l = []
        self.load_sprite_sheets()

        # Initialize pygame elements
        self.image = self.idle_frames_r[0]
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 60))

        # Initialize vectors for realistic movement
        self.pos = pygame.Vector2(self.rect.midbottom)
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, GRAVITY_ACC)
        self.friction = -0.12  # Make sure friction is ALWAYS negative

        # Hitbox
        hitbox_size = (self.rect.w, self.rect.h)
        self.hitbox = pg.Rect(self.rect.topleft, hitbox_size)

        # Player Stats and PowerUps (ammo is stored in Gun class)
        self.health = 10
        self.maxhealth = 10
        # PowerUps
        self.higher_jump = False    # Higher jumps for a certain time interval
        self.triple_jump = False    # Triple jumps for a certain time interval
        self.rapid_fire = False     # Increased fire rate for a certain time interval
        self.increased_dmg = False  # Increased damage for a certain time interval

        # Double jumping
        self.can_doublejump = True

        # These variables are used for jumping mechanics and sprite animations
        self.is_jumping = False
        self.can_jump = False
        self.is_descending = False  # Not to be confused with falling; this refers to going down a platform
        self.is_falling = False
        self.is_landing = False
        self.can_land = False  # Used to regulate landing animation
        self.is_walking = False
        self.is_facing_right = True
        self.is_hurt = False
        self.last_jump_time = 0
        self.last_descend_time = 0
        self.current_frame = -1  # Used for looping animations
        self.current_jump_frame = -1  # Used for jumping animation
        self.current_land_frame = -1  # Used for landing animation
        self.current_hurt_frame = -1
        self.last_frame_update = 0

        # USE THESE VARIABLES FOR CHANGE AI AS PLAYER PROGRESSES
        # Future player interval decreases as player score increases
        self.ft_player_interval = 3000  # Can go negative (degree of negativity does not matter)
        # Future speed scalar moves toward 1 as player score increases
        self.ft_spd_scalar = 3  # Cannot go below 1

        # Future (ft) invisible player used for AI to determine where to shoot
        self.last_ft_time = 0
        self.ft_rect = pygame.Rect(self.rect.center, (28, 28))
        self.ft_pos = pygame.Vector2(self.rect.center)  # AI tracks this
        self.ft_vel = pygame.Vector2(self.vel.xy * self.ft_spd_scalar)

        """ UNCOMMENT THIS TO SHOW INVISIBLE FUTURE PLAYER """
        """
        self.ft_image = pg.Surface((28, 28))
        self.ft_image.fill((0, 0, 255))
        """

        # Constants
        self.BASE_ACC = 0.5
        self.JUMP_VEL = -20
        self.JUMP_DELAY = 500
        self.DESCEND_DELAY = 750

        # Give player a gun
        self.gun = Gun(self.game, self)

        # Scrolling
        self.scroll_dist_plat = 0  # Use to spawn platforms
        self.scroll_dist_pow = 0   # Use to spawn powerups

    def tweak_ai(self):
        """
        Change Boss AI based on player score (higher score => better score)
        :return: None
        """
        # Dynamic AI algorithm
        # ft_player_interval == 0 when score == 4000
        self.ft_player_interval = 3000 - self.game.score
        self.ft_spd_scalar = 3 - self.game.score * 0.01
        if self.ft_spd_scalar < 1:
            self.ft_spd_scalar = 1

    def send_future_player(self, current_time):
        """
        Send out the future player rect that the boss AI will track to predict player movement
        :param current_time: pg.time.get_ticks()
        :return: None
        """
        if current_time - self.last_ft_time > self.ft_player_interval:  # Tweak this time interval to modify AI prediction
            self.last_ft_time = current_time
            player_center = (self.pos.x, self.pos.y - self.rect.h/2)
            self.ft_rect.center = player_center
            self.ft_pos = pygame.Vector2(player_center)
            self.ft_vel = pygame.Vector2(self.vel.xy * self.ft_spd_scalar)

    def update_future_player(self):
        """
        Move future player rect
        :return: None
        """
        # Wrap around sides of screen
        if self.ft_pos.x < -self.ft_rect.width / 2:
            self.ft_pos.x = SCREEN_WIDTH + self.ft_rect.width / 2
        if self.ft_pos.x > SCREEN_WIDTH + self.ft_rect.width / 2:
            self.ft_pos.x = -self.ft_rect.width / 2
        # Move
        self.ft_pos += self.ft_vel
        self.rect.midbottom = self.ft_pos

    def load_sprite_sheets(self):
        """
        Load sprite sheet images into frame lists
        :return: None
        """
        # Idle
        sheet = SpriteSheet(player_idle_path)
        for i in range(0, 8):  # Add all frames of sprite sheet into a list (8 sprites in this case)
            self.idle_frames_r.append(sheet.get_sprite(i * 32, 0, 32, 28))
        for frame in self.idle_frames_r:
            self.idle_frames_l.append(pygame.transform.flip(frame, True, False))

        # Walk
        sheet = SpriteSheet(player_walk_path)
        for i in range(0, 8):
            self.walk_frames_r.append(sheet.get_sprite(i * 32, 0, 32, 32))
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pygame.transform.flip(frame, True, False))

        # Jump
        sheet = SpriteSheet(player_jump_path)
        for i in range(0, 6):
            self.jump_frames_r.append(sheet.get_sprite(i * 28, 0, 28, 28))
        for frame in self.jump_frames_r:
            self.jump_frames_l.append(pygame.transform.flip(frame, True, False))

        # Fall
        sheet = SpriteSheet(player_fall_path)
        for i in range(0, 2):
            self.fall_frames_r.append(sheet.get_sprite(i * 32, 0, 32, 28))
        for frame in self.fall_frames_r:
            self.fall_frames_l.append(pygame.transform.flip(frame, True, False))

        # Land
        sheet = SpriteSheet(player_land_no_dust_path)
        for i in range(0, 4):
            self.land_frames_r.append(sheet.get_sprite(i * 44, 0, 44, 32))
        for frame in self.land_frames_r:
            self.land_frames_l.append(pygame.transform.flip(frame, True, False))

        # Hurt
        sheet = SpriteSheet(player_hurt_path)
        for i in range(0, 9):
            self.hurt_frames_r.append(sheet.get_sprite(i * 32, 0, 32, 28))
        for frame in self.hurt_frames_r:
            self.hurt_frames_l.append(pygame.transform.flip(frame, True, False))

    def animate(self):
        """
        Animate frames using frame lists and state variables
        :return: None
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_update > 100 and not self.is_hurt:
            self.last_frame_update = current_time
            # Land
            if self.is_landing and self.is_facing_right:
                self.current_land_frame = (self.current_land_frame + 1) % len(self.land_frames_r)
                self.image = self.land_frames_r[self.current_land_frame]
            elif self.is_landing and not self.is_facing_right:
                self.current_land_frame = (self.current_land_frame + 1) % len(self.land_frames_l)
                self.image = self.land_frames_l[self.current_land_frame]
            if self.current_land_frame >= len(self.land_frames_r) - 1:
                self.is_landing = False
                self.current_land_frame = 0
            # Idle
            if not self.is_walking and not self.is_jumping and self.is_facing_right \
                    and not self.is_landing and not self.is_falling:
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_r)  # Make the frames loopy loop
                self.image = self.idle_frames_r[self.current_frame]
            elif not self.is_walking and not self.is_jumping and not self.is_facing_right \
                    and not self.is_landing and not self.is_falling:
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_l)
                self.image = self.idle_frames_l[self.current_frame]
            # Walk
            if self.is_walking and not self.is_jumping and self.is_facing_right \
                    and not self.is_landing and not self.is_falling:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                self.image = self.walk_frames_r[self.current_frame]
            elif self.is_walking and not self.is_jumping and not self.is_facing_right \
                    and not self.is_landing and not self.is_falling:
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                self.image = self.walk_frames_l[self.current_frame]
            # Jump
            if self.is_jumping and not self.is_falling and self.is_facing_right and not self.is_landing:
                self.current_jump_frame = (self.current_jump_frame + 1) % len(self.jump_frames_r)
                self.image = self.jump_frames_r[self.current_jump_frame]
            elif self.is_jumping and not self.is_falling and not self.is_facing_right and not self.is_landing:
                self.current_jump_frame = (self.current_jump_frame + 1) % len(self.jump_frames_l)
                self.image = self.jump_frames_l[self.current_jump_frame]
            elif not self.is_jumping:
                self.current_jump_frame = 0
            # Fall
            if self.is_falling and self.is_facing_right and not self.is_landing:
                self.current_frame = (self.current_frame + 1) % len(self.fall_frames_r)
                self.image = self.fall_frames_r[self.current_frame]
            elif self.is_falling and not self.is_facing_right and not self.is_landing:
                self.current_frame = (self.current_frame + 1) % len(self.fall_frames_l)
                self.image = self.fall_frames_l[self.current_frame]

        # Hurt
        elif current_time - self.last_frame_update > 50 and self.is_hurt:
            if self.is_facing_right:
                self.last_frame_update = current_time
                self.current_hurt_frame = (self.current_hurt_frame + 1) % len(self.hurt_frames_r)
                self.image = self.hurt_frames_r[self.current_hurt_frame]
            elif not self.is_facing_right:
                self.last_frame_update = current_time
                self.current_hurt_frame = (self.current_hurt_frame + 1) % len(self.hurt_frames_l)
                self.image = self.hurt_frames_l[self.current_hurt_frame]
            if self.current_hurt_frame >= len(self.hurt_frames_r) - 1:
                self.is_hurt = False
                self.current_hurt_frame = 0


        # Adjust sprite height so that sprite doesn't clip into platform
        bottom = self.rect.bottom
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom

    def apply_platform_collisions(self):
        """
        Check and apply collisions with platforms
        :return: None
        """
        # WARNING: The smaller the platform width, the higher the chance of player falling through platform
        # ... at high y-velocities. Nothing can be done about this because of how pygame calls the update() method
        self.rect.y += 1
        collisions = pygame.sprite.spritecollide(self, self.game.plat_sprites, False)
        self.rect.y -= 1
        # Only applies collision if player is falling, adjusts to ensure the floating doesn't float at edges
        if collisions:
            lowest_platform = collisions[0]
            for platform in collisions:  # This handles chance of player falling & colliding with 2 platform
                if platform.rect.y > lowest_platform.rect.y:
                    lowest_platform = platform
            if not self.is_descending and self.vel.y > 0 and lowest_platform.rect.left - 10 < self.pos.x < lowest_platform.rect.right + 10:
                if self.pos.y < lowest_platform.rect.centery:  # This makes player teleport up platforms realistically
                    # Change "lowest_platform.rect.centery" to a y-value higher inside the platform sprite if we decide
                    # ... to make platforms with large widths (ex: lowest_platform.rect.centery - 10)
                    # ... or lower for low widths
                    self.pos.y = lowest_platform.rect.top
                    self.vel.y = 0

                    # Change friction depending on platform
                    self.friction = lowest_platform.friction  # Set player friction equal to platform friction

                    # Allow jumping
                    if not self.is_jumping:
                        self.can_jump = True
                        self.can_doublejump = True

                    self.is_jumping = False
                    self.is_falling = False
                    if self.can_land:  # This ensures the landing animation and fx plays only once
                        self.can_land = False
                        self.is_landing = True
                        # Trigger land fx
                        PlayerLandFX(self.game, self.pos.x, self.pos.y)
            elif self.pos.y > lowest_platform.rect.bottom:
                self.is_descending = False
            else:
                self.friction = -0.1  # If player is in air, set back to base

    def scroll_with_screen(self):
        """
        When player reaches top half of screen, scroll up (move all objects down)
        :return: None
        """
        if self.pos.y - self.rect.height <= SCREEN_HEIGHT // 2:
            # Used for determining when to spawn new platforms
            self.scroll_dist_plat += abs(self.vel.y)
            self.scroll_dist_pow += abs(self.vel.y)

            # Player moves down
            self.pos.y += abs(self.vel.y)
            # Boss moves down
            self.game.boss.pos.y += abs(self.vel.y)
            # Platforms move down
            for plat in self.game.plat_sprites:
                plat.rect.y += abs(self.vel.y)
            # Effects move down
            for fx in self.game.fx_sprites:
                fx.rect.y += abs(self.vel.y)
            # Future player moves down
            self.ft_pos.y += abs(self.vel.y)
            # Projectiles move down
            for bullet in self.game.player_proj_sprites:
                bullet.pos.y += abs(self.vel.y)
            for bullet in self.game.boss_proj_sprites:
                bullet.pos.y += abs(self.vel.y)
            # PowerUps move down
            for power in self.game.pow_sprites:
                power.rect.y += abs(self.vel.y)
            # Enemies move down
            for enemy in self.game.enemy_sprites:
                enemy.pos.y += abs(self.vel.y)

    def check_death_eligibility(self):
        """
        Test is player is dead or should be dead
        :return: None
        """
        # If player falls below bottom of screen, screen scrolls down suddenly ...
        if self.pos.y - self.rect.height > SCREEN_HEIGHT:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= max(self.vel.y, 10)
                if sprite.rect.bottom < 0:
                    # ... and dies
                    sprite.kill()
        # Game over
        if len(self.game.plat_sprites) == 0 or self.health <= 0:
            self.game.is_playing = False
            self.game.gui.draw_game_over_menu()

    def take_hit(self):
        """
        Interact with enemy projectiles and enemy hitboxes and update health
        :return: None
        """
        for proj in self.game.boss_proj_sprites:
            if self.hitbox.colliderect(proj.hitbox):
                self.is_hurt = True
                if isinstance(proj, IceShard):
                    self.health -= 1
                    pg.mixer.Sound(iceshard_hit_sound).play(0, 1750).set_volume(0.25)
                    IceShardImpact(self.game, proj.pos.x, proj.pos.y)
                elif isinstance(proj, FireBall):
                    self.health -= 2
                    pg.mixer.Sound(fireball_hit_sound).play()
                    FireBallImpact(self.game, proj.pos.x, proj.pos.y)
                proj.kill()
                #self.sound_fx.hurt.play()

                if self.vel.y < 0:
                    # Player gets bumped down a bit if jumping
                    self.vel.y = 5
                    # Also can't doublejump
                    self.can_doublejump = False

        # Take damage and gets bumped down if touching boss
        if self.hitbox.colliderect(self.game.boss.hitbox) and self.vel.y < 0 and self.game.boss.is_alive:
            self.health -= .5
            self.is_hurt = True
            self.vel.y = 5
            # Also can't doublejump
            self.can_doublejump = False
            self.sound_fx.hurt.play()

    def update_solo(self):
        """
        Update everything (movement, controls, death state, animations, etc.)
        :return: None
        """
        keys = pygame.key.get_pressed()
        self.acc = pygame.Vector2(0, GRAVITY_ACC)
        self.apply_platform_collisions()
        current_time = pygame.time.get_ticks()
        self.animate()
        self.take_hit()
        self.scroll_with_screen()
        self.check_death_eligibility()
        # Future player
        self.send_future_player(current_time)
        self.update_future_player()
        self.tweak_ai()

        for event in self.game.events:
            # Jumping
            if event.type == pygame.KEYDOWN and self.can_jump and current_time - self.last_jump_time >= self.JUMP_DELAY:
                # Jump controls (Higher the longer you hold W)
                if event.key == pygame.K_w:
                    # Full jump
                    self.vel.y = self.JUMP_VEL
                    self.is_jumping = True  # This does not become false until player lands
                    self.last_jump_time = current_time
                    # Trigger jump fx and jump sound fx
                    PlayerJumpFX(self.game, self.pos.x, self.pos.y)
                    self.sound_fx.jump.play()
                    self.can_jump = False
            # Partial jump
            if event.type == pygame.KEYUP and self.is_jumping:
                if event.key == pygame.K_w:
                    partial_vel = self.vel.y / 2
                    if self.vel.y < partial_vel:
                        self.vel.y = partial_vel
            # Double jumping
            if event.type == pygame.KEYDOWN and self.can_doublejump and self.is_jumping \
                    and current_time - self.last_jump_time >= self.JUMP_DELAY/2:
                if event.key == pygame.K_w:
                    self.last_jump_time = current_time
                    self.can_doublejump = False
                    self.vel.y = self.JUMP_VEL
                    PlayerJumpFX(self.game, self.pos.x, self.pos.y)
                    self.sound_fx.jump.play()

        # Descend controls
        if keys[pygame.K_s] and current_time - self.last_descend_time >= self.DESCEND_DELAY:
            self.last_descend_time = current_time
            self.is_descending = True

        # Falling animation condition
        if self.vel.y > 0:
            self.is_falling = True
            self.can_land = True

        # Horizontal controls
        if keys[pygame.K_a]:
            self.acc.x += -self.BASE_ACC
            self.is_facing_right = False
            self.is_walking = True
        if keys[pygame.K_d]:
            self.acc.x += self.BASE_ACC
            self.is_facing_right = True
            self.is_walking = True
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.is_walking = False

        # Update movement
        self.acc.x += self.vel.x * self.friction  # Apply friction
        self.vel += self.acc
        self.pos += self.vel + (0.5 * self.acc)  # Kinematic equation

        # Wrap around sides of screen
        if self.pos.x < -self.rect.width/2:
            self.pos.x = SCREEN_WIDTH + self.rect.width/2
        if self.pos.x > SCREEN_WIDTH + self.rect.width/2:
            self.pos.x = -self.rect.width/2

        # Calculated position will always represent midbottom of player sprite
        self.rect.midbottom = self.pos
        self.hitbox.midbottom = self.pos