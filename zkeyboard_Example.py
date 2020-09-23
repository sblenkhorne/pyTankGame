# A simple keyboard control for a tank including display of available information

import pygame
from pygame import *

def action(my_tank):
    pos = my_tank.my_position()
    lvl = my_tank.my_AI_level()
    heading = my_tank.my_heading()
    tur = my_tank.turret_direction()
    cool = my_tank.weapon_cooldown()
    points = my_tank.checkSensors()
    tanks = my_tank.enemy_tanks()
    hit = my_tank.damaged()
    key = pygame.key.get_pressed()
    if key[K_a]:
        my_tank.turn_left()
    if key[K_d]:
        my_tank.turn_right()
    if key[K_w]:
        my_tank.forward()
    if key[K_q]:
        my_tank.rotate_left()
    if key[K_e]:
        my_tank.rotate_right()
    if key[K_s]:
        my_tank.reverse()
    if key[K_1]:
        my_tank.fire()
    if key[K_0]:
        print("my position",pos)
        print("my AI level",lvl)
        print("my heading",heading)
        print("my turret aim",tur)
        print("shot cooldown",cool)
        print("Damaged?",hit)
        print("tripped sensors:")
        if points['n']: print("North")
        if points['e']: print("East")
        if points['s']: print("South")
        if points['w']: print("West")
        print("point sensors:")
        if points['fl']: print("FL",end = ' ')
        if points['f']: print("F",end = ' ')
        if points['fr']: print("FR",end = ' ')
        if points['r']: print("R",end = ' ')
        if points['br']: print("BR",end = ' ')
        if points['b']: print("B",end = ' ')
        if points['bl']: print("BL",end = ' ')
        if points['l']: print("L",end = ' ')
        print()
        print("Visible enemies:",tanks)
