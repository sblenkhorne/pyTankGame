import math, random  # ignore the next line...
Hacks = ((0,-10),(0,-9),(1,-9),(2,-9),(3,-9),(4,-9),(4,-8),(5,-8),(6,-7),(7,-7),(7,-6),(8,-5),(8,-5),(9,-4),(9,-3),(9,-2),(9,-1),(9,0),(10,0),(9,0),(9,1),(9,2),(9,3),(9,4),(8,4),(8,5),(7,6),(7,7),(6,7),(5,8),(5,8),(4,9),(3,9),(1,9),(0,9),(0,10),(0,9),(-1,9),(-2,9),(-3,9),(-4,9),(-4,8),(-5,8),(-6,7),(-7,7),(-7,6),(-8,5),(-8,5),(-9,4),(-9,3),(-9,2),(-9,1),(-9,0),(-10,0),(-9,0),(-9,-1),(-9,-2),(-9,-3),(-9,-4),(-8,-4),(-8,-5),(-7,-6),(-7,-7),(-6,-7),(-5,-8),(-5,-8),(-4,-9),(-3,-9),(-2,-9),(-1,-9),(0,-9))
def pathing_direction(my_tank,wanted_angle):  #choses direction to go in order to get to targetede location, only goes straight up left right or down
    global enemy_last_pos, target
    if my_tank.enemy_tanks():
        enemy_pos = my_tank.enemy_tanks()[0]
    else:
        enemy_pos = target
    if abs(my_tank.my_position()[0] - enemy_pos[0]) > abs(my_tank.my_position()[1] - enemy_pos[1]):
        if len(my_tank.enemy_tanks())>0 and my_tank.enemy_tanks()[0][0] - enemy_pos[0] > 0:
            if my_tank.checkSensors()['e'] == False and not wanted_angle == 270:
                return 90
            if my_tank.enemy_tanks()[0][1] - enemy_pos[1] > 0:
                if my_tank.checkSensors()['s'] == False and not wanted_angle == 0:
                    return 180
                if my_tank.checkSensors()['n'] == False and not wanted_angle == 180:
                    return 0
                if my_tank.checkSensors()['w'] == False and not wanted_angle == 90:
                    return 270
                wanted_angle += 180
                if wanted_angle > 359:
                    wanted_angle -= 360
                return wanted_angle
            if my_tank.checkSensors()['n'] == False and not wanted_angle == 180:
                return 0
            if my_tank.checkSensors()['s'] == False and not wanted_angle == 0:
                return 180
            if my_tank.checkSensors()['w'] == False and not wanted_angle == 90:
                return 270
            wanted_angle += 180
            if wanted_angle > 359:
                wanted_angle -=360
            return wanted_angle
        if my_tank.checkSensors()['w'] == False and not wanted_angle == 90:
            return 270
        if my_tank.enemy_tanks() and my_tank.enemy_tanks()[0][1] - enemy_pos[1] > 0:
            if my_tank.checkSensors()['s'] == False and not wanted_angle == 0:
                return 180
            if my_tank.checkSensors()['n'] == False and not wanted_angle == 180:
                return 0
            if my_tank.checkSensors()['e'] == False and not wanted_angle == 270:
                return 90
            wanted_angle += 180
            if wanted_angle > 359:
                wanted_angle -= 360
            return wanted_angle
        if my_tank.checkSensors()['n'] == False and not wanted_angle == 180:
            return 0
        if my_tank.checkSensors()['s'] == False and not wanted_angle == 0:
            return 180
        if my_tank.checkSensors()['e'] == False and not wanted_angle == 270:
            return 90
        wanted_angle += 180
        if wanted_angle > 359:
            wanted_angle -=360
        return wanted_angle
    if my_tank.enemy_tanks():
        if my_tank.enemy_tanks()[0][1] - enemy_pos[1] > 0:
            if my_tank.checkSensors()['s'] == False and not wanted_angle == 0:
                return 180
            if my_tank.enemy_tanks()[0][0] - enemy_pos[0] > 0:
                if my_tank.checkSensors()['e'] == False and not wanted_angle == 270:
                    return 90
                if my_tank.checkSensors()['w'] == False and not wanted_angle == 90:
                    return 270
                if my_tank.checkSensors()['n'] == False and not wanted_angle == 180:
                    return 0
                wanted_angle += 180
                if wanted_angle > 359:
                    wanted_angle -= 360
                return wanted_angle
            if my_tank.checkSensors()['w'] == False and not wanted_angle == 90:
                return 270
            if my_tank.checkSensors()['e'] == False and not wanted_angle == 270:
                return 90
            if my_tank.checkSensors()['n'] == False and not wanted_angle == 180:
                return 0
            wanted_angle += 180
            if wanted_angle > 359:
                wanted_angle -=360
            return wanted_angle
    if my_tank.checkSensors()['n'] == False and not wanted_angle == 180:
        return 0
    if my_tank.enemy_tanks() and my_tank.enemy_tanks()[0][0] - enemy_pos[0] > 0:
        if my_tank.checkSensors()['e'] == False and not wanted_angle == 270:
            return 90
        if my_tank.checkSensors()['w'] == False and not wanted_angle == 90:
            return 270
        if my_tank.checkSensors()['s'] == False and not wanted_angle == 0:
            return 180
        wanted_angle += 180
        if wanted_angle > 359:
            wanted_angle -= 360
        return wanted_angle
    if my_tank.checkSensors()['w'] == False and not wanted_angle == 90:
        return 270
    if my_tank.checkSensors()['e'] == False and not wanted_angle == 270:
        return 90
    if my_tank.checkSensors()['s'] == False and not wanted_angle == 0:
        return 180
    wanted_angle += 180
    if wanted_angle > 359:
        wanted_angle -=360
    return wanted_angle
def Target(my_tank, pos):  # calculates where the tank will be when the buller hits if it continues in the same direction
    global target
    if pos == []:
        return target
    if pos[-1] == my_tank.enemy_tanks() or len(pos) > 3:
        return pos[-1]
    if my_tank.enemy_tanks():
        extrapolated_pos = my_tank.enemy_tanks()[0]
        change = ((extrapolated_pos[0]-pos[2][0],extrapolated_pos[1]-pos[2][1]),(pos[3][0]-pos[2][0],pos[3][1]-pos[2][1]),(pos[2][0]-pos[1][0],pos[2][1]-pos[1][1]),(pos[1][0]-pos[0][-0],pos[1][1]-pos[0][1]))
        Frames = 0
        Repeat = False
        for repeat in ((8,-5),(5,8),(-8,5),(-5,-8)):
            if change[0] == repeat:
                Repeat = True
        if change[0] == change[1] and (not Repeat or change[1] == change[2]):
            while True:
                distnce = math.sqrt(pow(extrapolated_pos[0]-my_tank.my_position()[0])+pow(extrapolated_pos[1]-my_tank.my_position()[1]))
                bullet_frames = 0
                while distnce > 20:
                    distnce -= 20
                    bullet_frames += 1
                if bullet_frames <= Frames:
                    return extrapolated_pos
                else:
                    extrapolated_pos[0] += change[0][0]
                    extrapolated_pos[1] += change[0][1]
                    Frames += 1
        enemy_angle = [find_angle(change[0]),find_angle(change[1]),find_angle(change[2]),find_angle(change[3])]
        turn = "left"
        if enemy_angle[0] == "":
            if enemy_angle[1] == "":
                if change[0] == (8,-5):
                    if enemy_angle[2] == 10:
                        turn == "right"
                        enemy_angle[0] = 12
                    else:
                        enemy_angle[0] = 11
                elif change[0] == (8,5):
                    if enemy_angle[2] == 28:
                        turn == "right"
                        enemy_angle[0] = 30
                    else:
                        enemy_angle[0] = 29
                elif change[0] == (-8,5):
                    if enemy_angle[2] == 46:
                        turn == "right"
                        enemy_angle[0] = 48
                    else:
                        enemy_angle[0] = 47
                elif change[0] == (-5,-8):
                    if enemy_angle[2] == 64:
                        turn == "right"
                        enemy_angle[0] = 66
                    else:
                        enemy_angle[0] = 65
            elif change[0] == (8,-5):
                if enemy_angle[1] == 10:
                    turn == "right"
                    enemy_angle[0] = 11
                else:
                    enemy_angle[0] = 12
            elif change[0] == (8,5):
                if enemy_angle[1] == 28:
                    turn == "right"
                    enemy_angle[0] = 29
                else:
                    enemy_angle[0] = 30
            elif change[0] == (-8,5):
                if enemy_angle[1] == 46:
                    turn == "right"
                    enemy_angle[0] = 47
                else:
                    enemy_angle[0] = 48
            elif change[0] == (-5,-8):
                if enemy_angle[1] == 64:
                    turn == "right"
                    enemy_angle[0] = 65
                else:
                    enemy_angle[0] = 66
            else:
                if change[0] == (0,-9):
                    if enemy_angle[1] == 70:
                        turn == "right"
                        enemy_angle[0] = 71
                    elif  enemy_angle[3] == 70:
                        turn = "right"
                        enemy_angle[0] = 1
                    elif enemy_angle[1] == 2:
                        enemy_angle[0] = 1
                    else:
                        enemy_angle[0] = 71
                elif change[0] == (9,0):
                    if enemy_angle[1] == 16:
                        turn == "right"
                        enemy_angle[0] = 17
                    elif  enemy_angle[3] == 16:
                        turn = "right"
                        enemy_angle[0] = 19
                    elif enemy_angle[1] == 20:
                        enemy_angle[0] = 19
                    else:
                        enemy_angle[0] = 17
                elif change[0] == (0,9):
                    if enemy_angle[1] == 34:
                        turn == "right"
                        enemy_angle[0] = 35
                    elif  enemy_angle[3] == 34:
                        turn = "right"
                        enemy_angle[0] = 37
                    elif enemy_angle[1] == 38:
                        enemy_angle[0] = 37
                    else:
                        enemy_angle[0] = 35
                elif change[0] == (-9,0):
                    if enemy_angle[1] == 52:
                        turn == "right"
                        enemy_angle[0] = 53
                    elif  enemy_angle[3] == 52:
                        turn = "right"
                        enemy_angle[0] = 55
                    elif enemy_angle[1] == 56:
                        enemy_angle[0] = 55
                    else:
                        enemy_angle[0] = 53
        else:
            if enemy_angle[1] == "":
                if enemy_angle[2] == "":
                    if enemy_angle[0] == enemy_angle[3]+3:
                        turn = "right"
                else:
                    if enemy_angle[0] == enemy_angle[2]+2:
                        turn = "right"
            else:
                if enemy_angle[0] == enemy_angle[1]+1:
                    turn = "right"
        while True:
            distnce = math.sqrt(pow(extrapolated_pos[0]-my_tank.my_position()[0])+pow(extrapolated_pos[1]-my_tank.my_position()[1]))
            bullet_frames = 0
            while distnce > 20:
                distnce -= 20
                bullet_frames += 1
            if bullet_frames <= Frames:
                return extrapolated_pos
            else:
                if turn == "right":
                    if enemy_angle[0]+Frames > 71:
                        Change = Hacks[enemy_angle[0]+Frames-71]
                    else:
                        Change = Hacks[enemy_angle[0]+Frames]
                else:
                    Change = Hacks[enemy_angle[0]-Frames]
                extrapolated_pos[0] += Change[0]
                extrapolated_pos[1] += Change[1]
                Frames += 1
def find_angle(change):  # returns any angles that only occur once in hacks with their index in the list
    for repeat in ((8,-5),(5,8),(-8,5),(-5,-8),(0,-9),(9,0),(0,9),(-9,0)):
        if change == repeat:
            return ""
    return Hacks.index(change)
def Aim(my_tank,enemy_pos):  # calculates the angle of the barel neaded to hit the targeted posistion
    if enemy_pos:
        my_tank.my_position()
        x_distance = enemy_pos[0] - my_tank.my_position()[0]
        y_distance = enemy_pos[1] - my_tank.my_position()[1]
        if x_distance == 0:
            if y_distance >= 0:
                return 180
            return 0
        if y_distance == 0:
            if x_distance >= 0:
                return 90
            return 270
        if x_distance > 0:
            if y_distance > 0:
                Angle = round(math.atan(y_distance/float(x_distance))*180/math.pi) + 90
            else:
                Angle = round(math.atan(x_distance/float(-y_distance))*180/math.pi)
        else:
            if y_distance > 0:
                Angle = round(math.atan(-x_distance/float(y_distance))*180/math.pi) + 180
            else:
                Angle = round(math.atan(-y_distance/float(-x_distance))*180/math.pi) + 270
        if Angle % 5 > 2:
            while not Angle % 5 == 0:
                Angle += 1
        while not Angle % 5 == 0:
                Angle -= 1
        return Angle
    else:
        return 0
wanted_angle = 0
next_turn = 0
last_pos = ((0,0),0)
count = 0
movment_LRFS = [0,0,0,0]
enemy_last_pos = []
random.seed()
target = (random.randint(0,1200),random.randint(0,900))
def action(my_tank):  # main loop cauled within every frame of the game
    global wanted_angle, next_turn, last_pos, count, movment_LRFS, enemy_last_pos,target
    my_tank.set_Name("H.O.U.N.D.")
    if my_tank.my_position()[0] <= target[0] + 100 and my_tank.my_position()[0] >= target[0] - 100 and my_tank.my_position()[1] <= target[1] + 100 and my_tank.my_position()[1] >= target[1] - 100:
        target = (random.randint(0,1200),random.randint(0,900))
    if len(my_tank.enemy_tanks()) > 0:
        if len(enemy_last_pos)>0:
            target = enemy_last_pos[-1]
            enemy_last_pos = []
        next_turn = 0
        random.seed()
        last_pos = (my_tank.my_position(),my_tank.my_heading())
        if movment_LRFS[0] == 0 and movment_LRFS[1] == 0 and movment_LRFS[2] == 0:
            if random.randint(1,5) <= 2:
                movment_LRFS[0] = random.randint(5,18)
            elif random.randint(1,3) <= 2:
                movment_LRFS[1] = random.randint(5,18)
            else:
                movment_LRFS[2] = random.randint(5,18)
        if movment_LRFS[0] > 0:
            my_tank.turn_left()
            movment_LRFS[0] -= 1
        elif movment_LRFS[1] > 0:
            my_tank.turn_right()
            movment_LRFS[1] -= 1
        else:
            movment_LRFS[2] -= 0
        if random.randint(1,50) == 1:
            movment_LRFS[3] = 5
        if movment_LRFS[3] == 0:
            my_tank.forward()
        else:
            movment_LRFS[3] -= 1
        if last_pos == (my_tank.my_position(),my_tank.my_heading()):
            movment_LRFS[0],movment_LRFS[1],movment_LRFS[2] = 0,0,0
    else:
        if last_pos == (my_tank.my_position(),my_tank.my_heading()):
            count += 1
            if count > 5:
                wanted_angle += 180
                if wanted_angle > 359:
                    wanted_angle -=360
        else:
            count = 0
            last_pos = (my_tank.my_position(),my_tank.my_heading())
        if my_tank.my_heading() == wanted_angle:
            if next_turn <= 0 and not wanted_angle == pathing_direction(my_tank,wanted_angle):
                wanted_angle = pathing_direction(my_tank,wanted_angle)
                random.seed()
                if random.randint(1,5) == 1:
                    next_turn = random.randint(10,100)
                else:
                    next_turn = random.randint(10,50)
                if wanted_angle == 270:
                    if my_tank.my_heading() == 0:
                        my_tank.turn_left()
                    else:
                        my_tank.turn_right()
                else:
                    if my_tank.my_heading() == wanted_angle + 90:
                        my_tank.turn_left()
                    else:
                        my_tank.turn_right()
            else:
                my_tank.forward()
                next_turn -= 1
                if (my_tank.checkSensors()['n'] == True and wanted_angle == 0)or(my_tank.checkSensors()['e'] == True and wanted_angle == 90)or(my_tank.checkSensors()['s'] == True and wanted_angle == 180)or(my_tank.checkSensors()['w'] == True and wanted_angle == 270):
                    next_turn = 0
        else:
            if wanted_angle == 270:
                if my_tank.my_heading() == 0 or my_tank.my_heading() > 270:
                    my_tank.turn_left()
                else:
                    my_tank.turn_right()
            else:
                if my_tank.my_heading() > wanted_angle and my_tank.my_heading() <= wanted_angle + 90:
                    my_tank.turn_left()
                else:
                    my_tank.turn_right()
    aim = Aim(my_tank,Target(my_tank, enemy_last_pos))
    if  not my_tank.turret_direction() == aim:
        if aim >= 180:
            if my_tank.turret_direction() <= aim - 180 or my_tank.turret_direction() > aim:
                my_tank.rotate_left()
            else:
                my_tank.rotate_right()
        else:
            if my_tank.turret_direction() > aim and my_tank.turret_direction() <= aim + 180:
                my_tank.rotate_left()
            else:
                my_tank.rotate_right()
    if  my_tank.enemy_tanks() and my_tank.turret_direction() == aim and my_tank.enemy_tanks()[0]:
        my_tank.fire()
    if len(enemy_last_pos) > 3:
        enemy_last_pos.pop()
    if len(my_tank.enemy_tanks())>0:
        enemy_last_pos.append(my_tank.enemy_tanks()[0])