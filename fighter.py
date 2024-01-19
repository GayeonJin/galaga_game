#!/usr/bin/python

import sys
import pygame
import random

from gobject import *
from gresource import *
   
class fighter_object(game_object) :
    def __init__(self, x, y, resource_id) :
        super().__init__(x, y, resource_id)

        self.init_position()
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

if __name__ == '__main__' :
    print('fighter object')