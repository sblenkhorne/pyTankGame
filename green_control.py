import pygame
from pygame import *

def action(my_tank):
    key = pygame.key.get_pressed()
    if key[K_f]:
        my_tank.turn_left_for(45)
    if key[K_h]:
        my_tank.turn_right_for(90)
    if key[K_t]:
        my_tank.turn_to(290)
    if key[K_r]:
        my_tank.turret_left_for(135)
    if key[K_y]:
        my_tank.turret_right_for(315)
    if key[K_g]:
        my_tank.turret_to(20)
    if key[K_2]:
        my_tank.fire()

