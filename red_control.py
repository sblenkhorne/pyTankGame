import pygame
from pygame import *

def action(my_tank):
    key = pygame.key.get_pressed()
    if key[K_z]:
        my_tank.turn_left()
    if key[K_c]:
        my_tank.turn_right()
    if key[K_x]:
        my_tank.forward()
    if key[K_v]:
        my_tank.rotate_left()
    if key[K_n]:
        my_tank.rotate_right()
    if key[K_b]:
        my_tank.reverse()
    if key[K_4]:
        my_tank.fire()

