# Name: paths.py
# Purpose: Defines all file paths for resources used in the game
# Version: 4.0
# Date: 5 June 2020
# Author(s): Khoa Hoang, Adrienne Lhuc Estrella, Pratham Kwatra, Matt Innaurato
# Dependencies: pathlib module


""" USE THIS MODULE TO STORE FILE PATHS """
from pathlib import Path  # This module ensures that file paths work for all operating systems

# EX: parent_path = /home/khoa/PycharmProjects/667
current_path = Path(__file__).resolve().parents[0]
parent_path = Path(__file__).resolve().parents[1]


# NOTE: make sure to convert each Path() to string

# High score
high_score_path = str(parent_path / "bin/high_score.txt")

# Icons
icon_path = str(parent_path / "res/icons/gun.png")
health_path = str(parent_path / "res/icons/health_icon.png")
ammo_path = str(parent_path / "res/icons/bullet_icon.png")

# Menu Backgrounds
header_path = str(parent_path / "res/extra/startmenu.gif")
background_start = str(parent_path / "res/backgrounds/menus/start_menu.png")
background_pause = str(parent_path / "res/backgrounds/menus/pause_menu.png")
background_over = str(parent_path / "res/backgrounds/menus/over_menu.png")
background_about = str(parent_path / "res/backgrounds/menus/about_menu.png")
background_score = str(parent_path / "res/backgrounds/menus/score_menu.png")

# Our Pics
adrienne_path = str(parent_path / "res/extra/adriennepic.jpeg")
khoa_path = str(parent_path / "res/extra/khoapic.jpeg")
matt_path = str(parent_path / "res/extra/mattpic.jpg")
pk_path = str(parent_path / "res/extra/pkpic.jpg")

# Player sprite sheet paths
p = parent_path / "res/sprites/player"
# Idle sprite is 32x28, 8 frames
player_idle_path = str(p / "idle_sheet.png")
# Walk sprite is 32x32, 8 frames
player_walk_path = str(p / "walk_sheet.png")
# Jump sprite is 28x28, 6 frames
player_jump_path = str(p / "jump_sheet.png")
# Jump fx sprite is 28x28, 6 frames
player_jump_fx_path = str(p / "jump_fx_sheet.png")
# Death sprite is 52x28, 11 frames
player_death_path = str(p / "death_sheet.png")
# Fall sprite is 32x28, 2 frames
player_fall_path = str(p / "fall_sheet.png")
# Hurt sprite is 32x28, 9 frames
player_hurt_path = str(p / "hurt_sheet.png")
# Land dust sprite is 44x32, 4 frames
player_land_dust_path = str(p / "land_dust_sheet.png")
# Land fx sprite is 44x32, 4 frames
player_land_fx_path = str(p / "land_fx_sheet.png")
# Land no dust sprite is 44x32, 4 frames
player_land_no_dust_path = str(p / "land_no_dust_sheet.png")

# Backgrounds
# Glacial Mountains (384x216)
p = parent_path / "res/backgrounds/glacial_mountains/Layers"
# sky < glacial_mountains < clouds_bg = clouds_lonely < clouds_mg_3 < clouds_mg_2 < clouds_mg_1
glacial_sky_path = str(p / "sky.png")
glacial_mountains_path = str(p / "glacial_mountains.png")
glacial_clouds_bg_path = str(p / "clouds_bg.png")
glacial_clouds_lonely_path = str(p / "cloud_lonely.png")
glacial_clouds_mg_3_path = str(p / "clouds_mg_3.png")
glacial_clouds_mg_2_path = str(p / "clouds_mg_2.png")
glacial_clouds_mg_1_path = str(p / "clouds_mg_1.png")

# Grassy Mountains (384x216)
p = parent_path / "res/backgrounds/grassy_mountains/layers_fullcolor"
# sky < far_mountains < grassy_mountains < clouds_mid < hill < clouds_front
grassy_sky_path = str(p / "sky_fc.png")
grassy_far_mountains_path = str(p / "far_mountains_fc.png")
grassy_mountains_path = str(p / "grassy_mountains_fc.png")
grassy_clouds_mid_path = str(p / "clouds_mid_fc.png")
grassy_hill_path = str(p / "hill.png")
grassy_clouds_front_path = str(p / "clouds_front_fc.png")

# Sounds
# Jump
jump_sound_path = str(parent_path / "res/sounds/jump1.ogg")
# Pain
pain_sound_path  = str(parent_path / "res/sounds/pain.ogg")

fireball_sound = str(parent_path / "res/sounds/fireball.wav")
fireball_hit_sound = str(parent_path / "res/sounds/fire_ball_collision.wav")

iceshard_sound = str(parent_path / "res/sounds/iceshard.wav")
iceshard_hit_sound = str(parent_path / "res/sounds/ice_shard_collision.wav")



# Platforms
grass_tile_flat_path = str(parent_path / "res/platforms/Grass_Tile_Flat.png")

# Gun
gun_path = str(parent_path / "res/sprites/gun/gun.png")

""" PROJECTILES """
# FireBall (Boss)
p = parent_path / "res/sprites/projectiles/fireball"
fireball = (str(p / "FB001.png"),
            str(p / "FB002.png"),
            str(p / "FB003.png"),
            str(p / "FB004.png"),
            str(p / "FB005.png"))
fireballimpact = str(p / "fbimpact1.png")
fireballfx = str(p / "fbfx1.png")

# IceShard (Boss)
p = parent_path / "res/sprites/projectiles/iceshard"
iceshardfx = (str(p / "I5050-1.png"),
              str(p / "I5050-2.png"),
              str(p / "I5050-3.png"),
              str(p / "I5050-4.png"),
              str(p / "I5050-5.png"),
              str(p / "I5050-6.png"))
iceshardimpact = (str(p / "I5050-8.png"),
                  str(p / "I5050-9.png"),
                  str(p / "I5050-10.png"),
                  str(p / "I5050-11.png"))
iceshard = str(p / "I5050-7.png")

# Bullet (Player)
p = parent_path / "res/sprites/projectiles/bullet"
bullet_path = (str(p / "FB500-1.png"),
               str(p / "FB500-2.png"),
               str(p / "FB500-3.png"),
               str(p / "FB500-4.png"),
               str(p / "FB500-5.png"))
bulletbounce = (str(p / "B500-2.png"),
                str(p / "B500-3.png"),
                str(p / "B500-4.png"))
bulletimpact = str(p / "bimpact.png")

# Lightning (Boss)
p = parent_path / "res/sprites/projectiles/lightning"
lightning = (str(p / "LT100.png"),
             str(p / "LT101.png"),
             str(p / "LT102.png"),
             str(p / "LT103.png"),
             str(p / "LT104.png"),
             str(p / "LT105.png"),
             str(p / "LT106.png"))

""" GENERAL FX """
# Fire
p = parent_path / "res/sprites/fx/fire"
fire = (str(p / "1.png"),
        str(p / "2.png"),
        str(p / "3.png"),
        str(p / "4.png"),
        str(p / "5.png"))
p = parent_path / "res/sprites/fx/blood_splat"
bloodsplat = (str(p / "B100.png"),
              str(p / "B101.png"),
              str(p / "B102.png"))

""" ENEMY SPRITES """
# Flying eye
flyeye_flight = str(parent_path / "res/sprites/enemies/flying_eye/Flight.png")
flyeye_attack1 = str(parent_path / "res/sprites/enemies/flying_eye/Attack.png")
flyeye_attack2 = str(parent_path / "res/sprites/enemies/flying_eye/Attack2.png")
flyeye_takehit = str(parent_path / "res/sprites/enemies/flying_eye/Take Hit.png")
flyeye_death = str(parent_path / "res/sprites/enemies/flying_eye/Death.png")
# Slime
p = parent_path / "res/sprites/enemies/slime/Individual Sprites"
slime_idle = (str(p / "slime-idle-0.png"),
              str(p / "slime-idle-1.png"),
              str(p / "slime-idle-2.png"),
              str(p / "slime-idle-3.png"))
slime_move = (str(p / "slime-move-0.png"),
              str(p / "slime-move-1.png"),
              str(p / "slime-move-2.png"),
              str(p / "slime-move-3.png"))
slime_die = (str(p / "slime-die-0.png"),
             str(p / "slime-die-1.png"),
             str(p / "slime-die-2.png"),
             str(p / "slime-die-3.png"))
slime_hurt = (str(p / "slime-hurt-0.png"),
              str(p / "slime-hurt-1.png"),
              str(p / "slime-hurt-2.png"),
              str(p / "slime-hurt-3.png"))
slime_attack = (str(p / "slime-attack-0.png"),
                str(p / "slime-attack-1.png"),
                str(p / "slime-attack-2.png"),
                str(p / "slime-attack-3.png"),
                str(p / "slime-attack-4.png"))
