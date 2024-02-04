#!/usr/bin/python

import sys
import pygame
import random

from gobject import *
from gresource import *

SOUND_MUTE = True

class bulles_group :
    BULLET_SPEED = -1
    SHOT_ENEMY = 1

    def __init__(self, dx = 0, dy = BULLET_SPEED) :
        self.bullets = []
        self.snd_shot = pygame.mixer.Sound(get_snd_resource('snd_shot'))
        self.dx = dx
        self.dy = dy

    def add(self, x, y) :
        self.bullets.append(game_object(x, y, 'id_bullet'))

    def clear_all(self) :
        self.bullets = []

    def move(self, enemy) :
        is_shot = 0

        for i, bullet in enumerate(self.bullets) :
            bullet.move(self.dx, self.dy)

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
    print('bullet object')