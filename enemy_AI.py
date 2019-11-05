from math import atan2, degrees
import random

lastTurn = 0
def action(my_tank):
    my_tank.set_Name("Killer")
    enemyTanks = my_tank.enemy_tanks()
    print(my_tank.AIlevel)
    if my_tank.my_AI_level() == 2:
        my_tank.turn_left()
        my_tank.forward()
    elif my_tank.AIlevel >= 3:
        if len(enemyTanks) > 0:
            enemyDirection = getDirectionEnemy(my_tank.my_position(), enemyTanks[0])
            print("Enemy: " + str(enemyDirection) + " | My: " + str(my_tank.turret_direction()))
            dirDiff = abs(enemyDirection - my_tank.turret_direction())
            if enemyDirection < my_tank.turret_direction() - 8:
                my_tank.rotate_left()
            elif enemyDirection > my_tank.turret_direction() + 8:
                my_tank.rotate_right()
            else:
                if my_tank.AIlevel == 4:
                    my_tank.fire()
        prox = my_tank.checkSensors()
        if prox['f'] or prox['fl'] or prox['fr']:
            if my_tank.my_heading() == 0:
                if random.randint(1,2) ==1:
                    my_tank.turn_to(90)
                    lastTurn = 90
                else:
                    my_tank.turn_to(270)
                    lastTurn = 270
            elif my_tank.my_heading() == 90:
                if random.randint(1,2) ==1:
                    my_tank.turn_to(0)
                    lastTurn = 0
                else:
                    my_tank.turn_to(180)
                    lastTurn = 180
            elif my_tank.my_heading() == 180:
                if random.randint(1,2) ==1:
                    my_tank.turn_to(90)
                    lastTurn = 90
                else:
                    my_tank.turn_to(270)
                    lastTurn = 270
            elif my_tank.my_heading() == 270:
                if random.randint(1,2) ==1:
                    my_tank.turn_to(180)
                    lastTurn = 180
                else:
                    my_tank.turn_to(0)
                    lastTurn = 0
        else:
            my_tank.forward()
    

        

def getDirectionEnemy(myPosition, enemy):
    dx = enemy[0] - myPosition[0]
    dy = enemy[1] - myPosition[1]
    rads = atan2(-dy,dx)
    degs = degrees(rads)
    if degs <= 90:
        degs = 90 - degs
    elif degs > 90 and degs <= 180:
        degs = 360 - (degs-90)
    return degs