from random import *
from math import *

def action(my_tank):
    # Set AI enemy level
    my_tank.set_enemy_lvl(1)
    my_tank.set_Name("OOOOOOOOOOOOOO KILL 'EM")
    direction = my_tank.my_heading()
    turretDirection = my_tank.turret_direction()
    enemyCoordinates = my_tank.enemy_position()
    enemyX = int(enemyCoordinates[0])
    enemyY = int(enemyCoordinates[1])
    playerCoordinates = my_tank.my_position()
    playerX = int(playerCoordinates[0])
    playerY = int(playerCoordinates[1])
    quadrant = 0
    if playerX > enemyX and playerY < enemyY:
        quadrant = 2
    elif playerX < enemyX and playerY < enemyY:
        quadrant = 1
    elif playerX > enemyX and playerY > enemyY:
        quadrant = 3
    elif playerX < enemyX and playerY > enemyY:
        quadrant = 4
    slope = degrees(atan((enemyY - playerY) / (enemyX - playerX)))
    aimTurret = 0
    if quadrant == 1:
        aimTurret = 180 - slope
    elif quadrant == 2:
        aimTurret = 270 + slope
    elif quadrant == 3:
        aimTurret = 180 + slope
    elif quadrant == 4:
        aimTurret = 360 - slope
    
    if turretDirection < aimTurret + 5 and turretDirection > aimTurret - 5:
        my_tank.fire()
    elif turretDirection >= aimTurret + 5:
        my_tank.rotate_left()
    elif turretDirection <= aimTurret - 5:
        my_tank.rotate_right()
    
    if my_tank.checkSensors()['n']:
        if direction != 90:
            my_tank.turn_right()
        unstuck(my_tank)
    elif my_tank.checkSensors()['e']:
        if direction != 180:
            my_tank.turn_right()
        unstuck(my_tank)
    elif my_tank.checkSensors()['s']:
        if direction != 270:
            my_tank.turn_left()
        unstuck(my_tank)
    elif my_tank.checkSensors()['w']:
        if direction != 0:
            my_tank.turn_left()
        unstuck(my_tank)
    else:
        unstuck(my_tank)

def unstuck(my_tank):
    direction = my_tank.my_heading()
    randomDirection = randint(0, 7)
    if randomDirection == 0:
        if direction != 90:
            my_tank.turn_left()
        my_tank.forward()
    elif randomDirection == 1:
        if direction != 180:
            my_tank.turn_left()
        my_tank.forward()
    elif randomDirection == 2:
        if direction != 270:
            my_tank.turn_left()
        my_tank.forward()
    elif randomDirection == 3:
        if direction != 0:
            my_tank.turn_left()
        my_tank.forward()
    elif randomDirection == 4:
        if direction != 90:
            my_tank.turn_right()
        my_tank.forward()
    elif randomDirection == 5:
        if direction != 180:
            my_tank.turn_right()
        my_tank.forward()
    elif randomDirection == 6:
        if direction != 270:
            my_tank.turn_right()
        my_tank.forward()
    elif randomDirection == 7:
        if direction != 0:
            my_tank.turn_right()
        my_tank.forward()