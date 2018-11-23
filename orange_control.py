import pygame
from pygame import *

def action(my_tank):
    key = pygame.key.get_pressed()
    if key[K_j]:
        my_tank.turn_left()
    if key[K_l]:
        my_tank.turn_right()
    if key[K_i]:
        my_tank.forward()
    if key[K_u]:
        my_tank.rotate_left()
    if key[K_o]:
        my_tank.rotate_right()
    if key[K_k] and my_tank.cooldown == 0:
        my_tank.fire()

    if key[K_RETURN]:
        walls = my_tank.get_walls()
        if walls['n']: print('wall to north ',end='')
        if walls['s']: print('wall to south ',end='')
        if walls['e']: print('wall to east ',end='')
        if walls['w']: print('wall to west ',end='')
        print()
    if key[K_RSHIFT]:
        print(my_tank.clear_shot())
