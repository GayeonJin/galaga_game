#!/usr/bin/python

import sys
import pygame
import random

from gresource import *

class enemy_object :
    global gctrl

    ENEMY_SPEED = 0.5

    def __init__(self, res_id = 'id_enemy0') :
        self.object = pygame.image.load(get_img_resource(res_id))
        self.width = self.object.get_width()
        self.height = self.object.get_height()

        self.x = random.randrange(0, gctrl.width - self.width)
        self.y = 20
        self.ex = self.x + self.width - 1
        self.ey = self.y + self.height - 1

        self.set_speed(0, enemy_object.ENEMY_SPEED)
       
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
        self.ex = self.x + self.width - 1
        self.ey = self.y + self.height - 1

    def draw(self) :
        if self.object != None :
            gctrl.surface.blit(self.object, (int(self.x), int(self.y)))            

    def is_out_of_range(self) :
        if self.x <= 0 or self.x >= gctrl.width :
            return True
        elif self.y <= 0 or self.y >= gctrl.height :
            return True
        else :
            return False

ENEMY_CREATION_SPEED = 4
ENEMY_MAX = 20

class enemy_group :
    def __init__(self) :
        self.enemies = []
        self.enemies_max = ENEMY_MAX
        self.enemies_count = 0

        self.enemy_tick = 0

        self.delete_indexes = []

        self.booms = []
        self.boom_img = pygame.image.load(get_img_resource('id_boom'))

    def set_max_enemies(self, num) :
        self.enemies_max = num

    def create(self) :
        if self.enemies_count < self.enemies_max :
            self.enemy_tick += 1
            if self.enemy_tick > ENEMY_CREATION_SPEED :
                self.enemy_tick = 0
        
                color = random.randint(0, 1)
                if color == 0 :
                    self.enemies.append(enemy_object())
                else :
                    self.enemies.append(enemy_object('id_enemy1'))

                self.enemies_count += 1
                return True
        
        return False

    def clear_all(self) :
        self.enemies = []
        self.enemies_count = 0
        
        self.enemy_tick = 0
        self.delete_indexes = []
        self.booms = []

    def move(self) :
        crashed = False

        for i, enemy in enumerate(self.enemies) :
            enemy.move()
            if enemy.is_out_of_range() == True :
                self.delete_indexes.append(i)
                crashed = True

        for index in self.delete_indexes :
            del self.enemies[index]

        self.delete_indexes = []        

        return crashed

    def kill(self, object) :
        self.booms.append([10, object.x, object.y])
        self.enemies.remove(object)

    def draw(self) :
        for enemy in self.enemies :
            enemy.draw()

        for index, boom in enumerate(self.booms) :
            gctrl.surface.blit(self.boom_img, (boom[1], boom[2]))

            boom[0] -= 1
            if boom[0] == 0 :
                del self.booms[index]

if __name__ == '__main__' :
    print('enemy object')