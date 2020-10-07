from math import atan2, degrees
from random import randint

def action(my_tank):
    my_tank.set_Name("Newb")
    prox = my_tank.checkSensors()
    # print(prox)
    try:
        turns
    except:
        turns = []
    if prox['f']:
        if my_tank.my_heading() == 0:
            if prox['l']:
                my_tank.lastTurn = 90
                turns.append([my_tank.my_position(),90])
            elif prox['r']:
                my_tank.lastTurn = 270
            else:
                my_tank.lastTurn = 90 if randint(1,2) == 1 else 270
        elif my_tank.my_heading() == 90:
            if prox['l']:
                my_tank.lastTurn = 180
            elif prox['r']:
                my_tank.lastTurn = 0
            else:
                my_tank.lastTurn = 0 if randint(1,2) == 1 else 180
        elif my_tank.my_heading() == 180:
            if prox['l']:
                my_tank.lastTurn = 270
            elif prox['r']:
                my_tank.lastTurn = 90
            else:
                my_tank.lastTurn = 90 if randint(1,2) == 1 else 270
        elif my_tank.my_heading() == 270:
            if prox['l']:
                my_tank.lastTurn = 0
            elif prox['r']:
                my_tank.lastTurn = 180
            else:
                my_tank.lastTurn = 0 if randint(1,2) == 1 else 180
        my_tank.turn_to(my_tank.lastTurn)
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