#!/usr/bin/python

import sys
import pygame
import random

from gresource import *

class enemy_object :
    global gctrl

    ENEMY_SPEED = 0.5

    def __init__(self, res_id = 'id_enemy0', x = -1, y = -1) :
        self.object = pygame.image.load(get_img_resource(res_id))
        self.width = self.object.get_width()
        self.height = self.object.get_height()

        if x == -1 and y == -1 :
            self.x = random.randrange(0, gctrl.width - self.width)
            self.y = 20
        else :
            self.x = x
            self.y = y

        self.ex = self.x + self.width - 1
        self.ey = self.y + self.height - 1

        self.set_speed(0, enemy_object.ENEMY_SPEED)
       
    def set_speed(self, del_x, del_y) :
        self.dx = del_x
        self.dy = del_y

    def move(self, del_x = 0, del_y = 0) :
        if del_x == 0 and del_y == 0 :
            self.x += self.dx
            self.y += self.dy
        else :
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

class enemy_group :
    ENEMY_CREATION_SPEED = 10
    ENEMY_MAX = 20

    def __init__(self) :
        self.enemies = []
        self.enemies_max = enemy_group.ENEMY_MAX
        self.enemies_count = 0

        self.enemy_tick = 0

        self.delete_indexes = []

        self.booms = []
        self.boom_img = pygame.image.load(get_img_resource('id_boom'))

    def set_max_enemies(self, num) :
        self.enemies_max = num

    def create_one(self) :
        if self.enemies_count < self.enemies_max :
            self.enemy_tick += 1
            if self.enemy_tick > enemy_group.ENEMY_CREATION_SPEED :
                self.enemy_tick = 0
        
                enemy_id = 'id_enemy%d'%(random.randint(0, 1))   
                self.enemies.append(enemy_object(enemy_id))
                self.enemies_count += 1
                return True
        
        return False

    def create(self, enemies_num, sx, sy) :
        if self.enemies_count + enemies_num >= self.enemies_max :
            enemies_num = self.enemies_max - self.enemies_count

        for i in range(enemies_num) :       
            enemy_id = 'id_enemy%d'%(random.randint(0, 1))   
            self.enemies.append(enemy_object(enemy_id), sx, sy)
            self.enemies_count += 1

        print('enemy_count : %d, enemy_max : %d'%(self.enemies_count, self.enemies_max))

    def clear_all(self) :
        self.enemies = []
        self.enemies_count = 0

        self.enemy_tick = 0
        self.delete_indexes = []
        self.booms = []

    def move(self) :
        missed_count = 0

        for i, enemy in enumerate(self.enemies) :
            enemy.move()
            if enemy.is_out_of_range() == True :
                self.delete_indexes.append(i)
                missed_count += 1

        for index in self.delete_indexes :
            del self.enemies[index]

        self.delete_indexes = []        

        return missed_count

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