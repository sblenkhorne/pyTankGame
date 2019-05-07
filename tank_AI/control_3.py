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
    if key[K_k]:
        my_tank.reverse()
    if key[K_3]:
        my_tank.fire()

