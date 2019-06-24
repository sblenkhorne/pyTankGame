import pygame
from pygame import *

def action(my_tank):
    #Set AI enemy level
    my_tank.set_enemy_lvl(1)
    my_tank.set_Name("YOU MUST DIE")
    my_tank.forward()
    if my_tank.clear_shot():
        while True:
            print("HAHAHA")