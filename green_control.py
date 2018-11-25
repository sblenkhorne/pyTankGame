import pygame
from pygame import *

def action(my_tank):
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
        my_tank.fire()

