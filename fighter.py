#!/usr/bin/python

import sys
import pygame
import random

from gresource import *

SOUND_MUTE = True

class game_object :
    global gctrl

    FIGHTER_SPEED = 5

    def __init__(self, x, y, resource_id) :
        if resource_id != None :
            resource_path = get_img_resource(resource_id)
            self.object = pygame.image.load(resource_path)
            self.width = self.object.get_width()
            self.height = self.object.get_height()
        else :
            self.object = None
            self.width = 0
            self.height = 0

        self.set_position(x, y)

        self.dx = 0
        self.dy = 0
        self.life_count = 1

        self.boom = pygame.image.load(get_img_resource('id_boom'))
        self.boom_count = 0        

    def set_position(self, x, y) : 
        self.x = x
        self.y = y        
        self.ex = self.x + self.width - 1
        self.ey = self.y + self.height - 1
        
    def set_speed(self, del_x, del_y) :
        self.dx = del_x
        self.dy = del_y

    def move(self, del_x = 0, del_y = 0) :
        if del_x == 0 :
            del_x = self.dx
        if del_y == 0 :
            del_y = self.dy

        self.x += del_x
        self.y += del_y

        if self.x < 0 :
            self.x = 0
        elif self.x > (gctrl.width - self.width) :
            self.x = (gctrl.width - self.width)

        self.ex = self.x + self.width - 1
        self.ey = self.y + self.height - 1

    def draw(self) :
        if self.object != None :
            gctrl.surface.blit(self.object, (self.x, self.y))            

    def is_out_of_range(self) :
        if self.x <= 0 or self.x >= gctrl.width :
            return True
        elif self.y <= 0 or self.y >= gctrl.height :
            return True
        else :
            return False

    def is_life(self) :
        if self.life_count > 0 :
            return True
        else :
            return False
    
    def set_life_count(self, count) :
        self.life_count = count
        if self.life_count > 0 :
            self.life = True

    def get_life_count(self) :
        return self.life_count
    
    def kill_life(self) :
        self.boom_count = 10
        self.life_count -= 1
        if self.life_count == 0 :
            self.life = False
            return False
        else :
            return True

    def check_crash(self, enemy, sound_object) :       
        if self.object != None and enemy.object != None :
            if self.y < enemy.ey :
                if (self.x > enemy.x and self.x < enemy.ex) or (self.ex > enemy.x and self.ex < enemy.ex) :
                    #print("crashed1 : ",  self.x, self.y, self.ex, self.ey)
                    #print("crashed2 : ",  enemy.x, enemy.y, enemy.ex, enemy.ey)
                    if sound_object != None and SOUND_MUTE == False:
                        sound_object.play()
                    return True
        return False
    
class fighter_object(game_object) :
    def __init__(self, x, y, resource_id) :
        super().__init__(x, y, resource_id)

        self.init_position();
        self.set_life_count(3)

    def init_position(self) :
        self.set_position(gctrl.width / 2, gctrl.height * 0.85)

    def check_crash(self, enemy, sound_object) :
        is_crash = super().check_crash(enemy, sound_object)
        if is_crash == True :
            self.kill_life()
            #enemy.kill_life()
            self.boom_count = 10

        return is_crash
    
    def draw(self) :
        super().draw()
        if self.boom_count > 0 :
            gctrl.surface.blit(self.boom, (self.x, self.y))
            self.boom_count -= 1

class bulles_group :
    BULLET_SPEED = -15
    SHOT_ENEMY = 1

    def __init__(self, speed = BULLET_SPEED) :
        self.bullets = []
        self.snd_shot = pygame.mixer.Sound(get_snd_resource('snd_shot'))
        self.speed = speed

    def add(self, x, y) :
        self.bullets.append(game_object(x, y, 'id_bullet'))

    def move(self, enemy) :
        is_shot = 0

        for i, bullet in enumerate(self.bullets) :
            bullet.move(0, self.speed)

            if enemy != None :
                if bullet.check_crash(enemy, self.snd_shot) == True :
                    self.bullets.remove(bullet)
                    is_shot = self.SHOT_ENEMY

            if bullet.is_out_of_range() == True :
                try :
                    self.bullets.remove(bullet)
                except :
                    pass
        
        return is_shot

    def draw(self) :
        for i, bullet in enumerate(self.bullets) :
            bullet.draw()  

if __name__ == '__main__' :
    print('fighter object')