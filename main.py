#!/usr/bin/python

import sys
import pygame
import random
from time import sleep

from gobject import *
from gresource import *
from fighter import *
from enemy import *
from bullet import *

TITLE_STR = "Galaga"

class player :
    SCORE_UNIT = 10
    LIFE_COUNT = 3

    STATUS_XOFFSET = 10
    STATUS_YOFFSET = 5

    def __init__(self) :
        self.life = player.LIFE_COUNT
        self.score = 0

        self.img_fighter = pygame.image.load(get_img_resource('id_fighter'))

    def update_score(self) :
        self.score += player.SCORE_UNIT

    def kill_life(self) :
        self.life -= 1

    def is_game_over(self) :
        if self.life <= 0 :
            return True
        else : 
            return False

    def draw_life(self, count) :
        # gctrl.draw_string("Life : " + str(count), player.STATUS_XOFFSET, player.STATUS_YOFFSET, ALIGN_RIGHT)
        x = player.STATUS_XOFFSET
        y = gctrl.height - self.img_fighter.get_height() - player.STATUS_YOFFSET
        for i in range(count - 1) :
            gctrl.surface.blit(self.img_fighter, (x, y))
            x += self.img_fighter.get_width()

    def draw_stage(self, stage) :
        gctrl.draw_string("Stage : " + str(stage), player.STATUS_XOFFSET, player.STATUS_YOFFSET, ALIGN_RIGHT)

    def draw_score(self, count) :
        gctrl.draw_string("Score : " + str(count), player.STATUS_XOFFSET, player.STATUS_YOFFSET, ALIGN_LEFT)

class stage :
    STATE_WAIT = 0
    STATE_RUN = 1

    def __init__(self) :
        self.stage_no = 1
        self.stage_state = stage.STATE_WAIT
        self.stage_timer = 0

        self.enemy_count = 0
        self.max_enemy_count = 40
        self.kill_enemy_count = 0

    def is_run(self) :
        if self.stage_state == stage.STATE_RUN :
            return True
        else :
            return False

    def update_kill_enemy(self) :
        self.kill_enemy_count += 1

    def draw(self) :
        if self.stage_state == stage.STATE_WAIT :
            gctrl.draw_string("Stage " + str(self.stage_no), 0, gctrl.height / 2, ALIGN_CENTER | ALIGN_TOP, 30, COLOR_WHITE)
            
            self.stage_timer += 1
            if self.stage_timer >= 3 * FPS : 
                self.stage_state = stage.STATE_RUN
                self.stage_timer = 0

class galaga_game :
    def __init__(self) :
        # initialize pygame
        pygame.init()
        self.clock = pygame.time.Clock()
    
        # backgroud and screen
        #self.bg_img = pygame.image.load(get_img_resource('id_background'))

        pad_width = 800
        pad_height = 600

        gctrl.set_surface(pygame.display.set_mode((pad_width, pad_height)))
        pygame.display.set_caption(TITLE_STR)

    def terminate(self) :
        pygame.quit()
        sys.exit()

    def game_over(self) :
        gctrl.draw_string('Game Over', 0, 0, ALIGN_CENTER, 60, COLOR_RED)
        pygame.display.update()
        sleep(2)
        self.run()

    def start(self) :
        # Clear gamepad
        gctrl.surface.fill(COLOR_WHITE)
        gctrl.draw_string(TITLE_STR, 0, 0, ALIGN_CENTER, 60, COLOR_BLACK)
        gctrl.draw_string("press any key", 0, gctrl.height / 2 + 60, ALIGN_CENTER | ALIGN_TOP, 30, COLOR_RED)

        while True :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.terminate()
                    return

            pygame.display.update()
            self.clock.tick(FPS)    

    def run(self) :
        self.start()

        # sound resource
        snd_shot = pygame.mixer.Sound(get_snd_resource('snd_shot'))
        snd_explosion = pygame.mixer.Sound(get_snd_resource('snd_explosion'))   

        # game player
        game_player = player()
        stage_mgr = stage()

        # aircraft
        fighter = fighter_object(0, 0, 'id_fighter')
        bullets = bulles_group()

        enemy_ctrl = enemy_group()

        bullet_pressed = False
        bullet_timer = 0
        crashed = False
        while not crashed :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    crashed = True

                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_LEFT:
                        fighter.set_speed(-1 * fighter_object.FIGHTER_SPEED, 0)
                    elif event.key == pygame.K_RIGHT :
                        fighter.set_speed(fighter_object.FIGHTER_SPEED, 0)
                    elif event.key == pygame.K_SPACE :
                        bullet_pressed = True
                        bullet_timer = 0
                    if event.key == pygame.K_F10 :
                        gctrl.save_scr_capture(TITLE_STR)

                if event.type == pygame.KEYUP :
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        fighter.set_speed(0, 0)
                    elif event.key == pygame.K_SPACE :
                        bullet_pressed = False

            if bullet_pressed == True :
                bullet_timer += 1
                if bullet_timer >= 5 :
                    bullet_x = fighter.x + fighter.width / 2
                    bullet_y = fighter.y
                    bullets.add(bullet_x, bullet_y)
                    bullet_timer = 0

            # Clear gamepad
            gctrl.surface.fill(COLOR_BLACK)

            if stage_mgr.is_run() == True :
                # Draw background
                #gctrl.surface.blit(self.bg_img, (0, 0))

                # Create and move enemy
                enemy_ctrl.create()
                if enemy_ctrl.move() == True :
                    game_player.kill_life()

                # Draw enemy
                enemy_ctrl.draw()

                # Draw bullet
                for i, enemy in enumerate(enemy_ctrl.enemies) :
                    if bullets.move(enemy) == bulles_group.SHOT_ENEMY :
                        enemy_ctrl.kill(enemy)
                        game_player.update_score()

                bullets.draw()

                # Update aircraft
                fighter.move()

                # Check crash
                for i, enemy in enumerate(enemy_ctrl.enemies) :
                    if fighter.check_crash(enemy, snd_explosion) == True :
                        enemy_ctrl.kill(enemy)
                        game_player.life = fighter.life_count

                fighter.draw()
            else :
                stage_mgr.draw()

            # Draw Score
            game_player.draw_score(game_player.score)
            game_player.draw_life(game_player.life)
            game_player.draw_stage(stage_mgr.stage_no)

            pygame.display.update()
            self.clock.tick(FPS)

            if game_player.is_game_over() == True :
                self.game_over()
                crashed = True

        self.terminate()

if __name__ == '__main__' :
    game = galaga_game() 
    game.run()

