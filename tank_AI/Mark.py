#import pygame
#from pygame import *
from random import *
from math import *

"""
def targAndFire():
    posme = my_tank.my_position()
    posenemy = my_tank.enemy_position()
    xme = posme[0]
    yme = posme[1]
    xen = posenemy[0]
    yen = posenemy[1]
    print(xme + " " + yme)
    print(xen + " " + yen)
    
    posme = str(my_tank.my_position())
    cords = posme.split(", ")
    xi1 = cords(0)
    x1 = xi1.remove(0)
    yi1 = cords(1)
    y1 = yi1.remove(-1)
    print(y1)
    print(x1)

    posenemy = str(my_tank.my_position())
    cords2 = posenemy.split(", ")
    xi2 = cords2(0)
    x2 = xi2.remove(0)
    yi2 = cords2(1)
    y2 = yi2.remove(-1)
    print(y2)
    print(x2)

    degreefire = atan(y2 - y1 / x2 - x1)

    if my_tank.turret_direction() >= degreefire - 5 and my_tank.turret_direction() <= degreefire + 5:
        my_tank.fire()
    elif my_tank.turret_direction() >= degreefire + 5:
        my_tank.rotate_left()
    elif my_tank.turret_direction() <= degreefire - 5:
        my_tank.rotate_left()
    else:
        my_tank.fire()
"""

def action(my_tank):
    #Set AI enemy level
    my_tank.set_enemy_lvl(3)
    my_tank.set_Name("GWAKAMMOLE")
    north = my_tank.checkSensors()['n']
    east = my_tank.checkSensors()['e']
    south = my_tank.checkSensors()['s']
    west = my_tank.checkSensors()['w']
    tankDegree = my_tank.my_heading()
    
    #if tankDegree <= 45 and tankDegree >= 315:
    #    tankDegree = "north"
    #elif False:
        # define NESW

    if my_tank.enemy_tanks():
        posme = my_tank.my_position()
        posenemy = my_tank.enemy_tanks()[0]
        xme = posme[0]
        yme = posme[1]
        xen = posenemy[0]
        yen = posenemy[1]
        quadrant = 0
        #determine the quadrant
        if xme > xen and yme > yen:
            quadrant = 3
        elif xme < xen and yme > yen:
            quadrant = 4
        elif xme < xen and yme < yen:
            quadrant = 1
        elif xme > xen and yme < yen:
            quadrant = 2
        
        print(str(xme) + " " + str(yme))
        print(str(xen) + " " + str(yen))
        degreefire = degrees(atan(yme - yen / xme - xen))
        print(degreefire)

        if quadrant == 1:
            degreefire = abs(degreefire) + 180
        elif quadrant == 2:
            degreefire = abs(degreefire) + 90
        elif quadrant == 3:
            degreefire = abs(degreefire)
        elif quadrant == 4:
            degreefire = abs(degreefire) + 180
        else:
            degreefire = degreefire


        if my_tank.turret_direction() <= degreefire - 3 and my_tank.turret_direction() >= degreefire + 3:
            print("firing")
            my_tank.fire()
        elif my_tank.turret_direction() > degreefire + 3:
            my_tank.rotate_left()
        elif my_tank.turret_direction() < degreefire - 3:
            my_tank.rotate_right()
        elif my_tank.turret_direction() == degreefire:
            my_tank.fire()
        else:
            print("else")
            #my_tank.fire()
            r = randint(0, 1)
            if r == 1:
                my_tank.rotate_left()
            """
            r = randint(0, 2)
            if r == 1:
                r = randint(0, 2)
                if r == 2:
                    my_tank.rotate_right()
                elif r == 1:
                    my_tank.rotate_left()
                else:
                    my_tank.turn_right()
                    my_tank.forward()
                    degreefire = degreefire + 180
                    """
    else:
        if north and tankDegree <= 45 and tankDegree >= 315:
            my_tank.turn_left()
        elif east and tankDegree >= 45 and tankDegree <= 135:
            my_tank.turn_left()
        elif south and tankDegree <= 225 and tankDegree >= 135:
            my_tank.turn_left()
        elif west and tankDegree >= 225 and tankDegree <= 315:
            my_tank.turn_left()
        elif north and south and (tankDegree == 90 or tankDegree == 180):
            my_tank.forward()
        elif not north and not south and not east and not west:
            my_tank.forward()
        else:
            r = randint(0,1)
            if r == 0:
                my_tank.turn_left()
            else:
                my_tank.forward()
            
    #my_tank.forward()

"""

def action(my_tank):
    if not north and (tankDegree < 44 and tankDegree > 315):
        my_tank.forward()
        #my_tank.turn_right()
        my_tank.rotate_left()
        my_tank.fire()
    elif not east and (tankDegree < 134 and tankDegree > 46):
        my_tank.forward()
        #my_tank.turn_right()
        my_tank.rotate_left()
        my_tank.fire()
    elif not south and (tankDegree < 224 and tankDegree > 136):
        my_tank.forward()
        #my_tank.turn_right()
        my_tank.rotate_left()
        my_tank.fire()
    elif False:#not west and (tankDegree < 358 and tankDegree > 226):
        my_tank.forward()
        #my_tank.turn_right()
        my_tank.rotate_left()
        my_tank.fire()
    elif not (north or east or south or west):
        my_tank.turn_right()
        my_tank.rotate_left()
        my_tank.fire()
    elif False:# get the current position and compare it with an ld position, if its the same, turn and move:
        pass
    else:
        if my_tank.clear_shot():
            my_tank.rotate_left()
            my_tank.fire()
    
        else:
            a = randint(0, 5)
            if a == 0 or a == 3 or a == 4:
                my_tank.forward()
            elif a == 1:
                my_tank.turn_right()
            elif a == 2:
                my_tank.turn_left()
            else:
                my_tank.fire()
                """