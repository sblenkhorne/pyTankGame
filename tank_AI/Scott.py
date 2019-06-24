import pygame
from pygame import *

def action(my_tank):
    my_tank.set_Name("Scott")
    key = pygame.key.get_pressed()
    if key[K_f]:
        my_tank.turn_left()
    if key[K_h]:
        my_tank.turn_right()
    if key[K_t]:
        my_tank.forward()
    if key[K_r]:
        my_tank.rotate_left()
    if key[K_y]:
        my_tank.rotate_right()
    if key[K_g]:
        my_tank.reverse()
    if key[K_2]:
        my_tank.fire()

