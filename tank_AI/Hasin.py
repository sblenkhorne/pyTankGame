

import random
import math
from PIL import Image, ImageDraw, ImageTk 
import tkinter as tk
global gameMap
global lastMove
global aiMode
global target
global root
global lastPos
global loaded
global reloadingTime
global patrolMode

patrolMode = None

reloadingTime = 0
loaded = True
lastPos = [0,0]
lastMove = None


#root = tk.Tk()
aiMode = "mapping"
target = None
def mapGenrator(Val1,val2):
	temp = []
	for y in range(17):
		temp.append([])
		for x in range(22):
			if y == 0 or y == 16 or x == 0 or x == 21:
				temp[y].append(Val1)
			else:
				temp[y].append(val2)
	return temp
#gameMap = mapGenrator(1,0)
gameMap = mapGenrator(1,2)

def mapAnalsis(gameMap):
    temp = gameMap
    for y in range(0,len(gameMap)-1):
        for x in range(0,len(gameMap[y])-1):
            walls = [gameMap[y-1][x],gameMap[y+1][x],gameMap[y][x-1],gameMap[y][x+1]]
            if walls.count(1) >=3:
                temp[y][x] = 1
               # print("aaa")
    #printMap(temp)
    return temp

            

    
# 0 = unkown, 2 = empty, 3 = my postion, 4 = enemy postion, 1 = wall

def mapUpdater(my_tank):
     temp = my_tank.checkSensors()
     try:
         output = gameMap
     except:
         output = gameMap
     if temp["n"]:
         try:
             output[int(math.floor(my_tank.my_position()[1]/60))][int(math.floor(my_tank.my_position()[0]/60)+1)] = 1
         except:
            pass
             #print([int(math.floor(my_tank.my_position()[0]/60)+1),int(math.floor(my_tank.my_position()[1]/60))])
     else:
         try:
             output[int(math.floor(my_tank.my_position()[1]/60))][int(math.floor(my_tank.my_position()[0]/60)+1)] = 2
         except:
            pass
             #print([int(math.floor(my_tank.my_position()[0]/60)+1),int(math.floor(my_tank.my_position()[1]/60))])
     if temp["s"]:
         try:
             output[int(math.floor(my_tank.my_position()[1]/60))+2][int(math.floor(my_tank.my_position()[0]/60)+1)] = 1
         except:
            pass
             #print([int(math.floor(my_tank.my_position()[0]/60)+1),int(math.floor(my_tank.my_position()[1]/60))+2])
     else:
         try:
             output[int(math.floor(my_tank.my_position()[1]/60))+2][int(math.floor(my_tank.my_position()[0]/60)+1)] = 2
         except:
            pass
             #print([int(math.floor(my_tank.my_position()[0]/60)),int(math.floor(my_tank.my_position()[1]/60))+1])
     if temp["w"]:
         try:
             output[int(math.floor(my_tank.my_position()[1]/60)+1)][int(math.floor(my_tank.my_position()[0]/60))] = 1
         except:
            pass
             #print([int(math.floor(my_tank.my_position()[0]/60)+1),int(math.floor(my_tank.my_position()[1]/60))])
     else:
         try:
             output[int(math.floor(my_tank.my_position()[1]/60)+1)][int(math.floor(my_tank.my_position()[0]/60))] = 2
         except:
            pass
             #print([int(math.floor(my_tank.my_position()[0]/60)),int(math.floor(my_tank.my_position()[1]/60))+1])
     if temp["e"]:
         try:
             output[int(math.floor(my_tank.my_position()[1]/60)+1)][int(math.floor(my_tank.my_position()[0]/60))+2] = 1
         except:
            pass
             #print([int(math.floor(my_tank.my_position()[0]/60)+2),int(math.floor(my_tank.my_position()[1]/60))+1+1])
     else:
         try:
             output[int(math.floor(my_tank.my_position()[1]/60)+1)][int(math.floor(my_tank.my_position()[0]/60))+2] = 2
         except:
            pass
             #print([int(math.floor(my_tank.my_position()[0]/60+2)),int(math.floor(my_tank.my_position()[1]/60))+1])
           
     return mapAnalsis(output)
     #return output

def printMap(mapInput):
    print("map")
    for row in mapInput:
        temp = ""
        for item in row:
            if len(str(item)) == 1:
                temp+= "{0}{1} ".format(" ",str(item))
            else:
                temp+= "{0}{1} ".format("",str(item))
        print(temp)


def NoneChecker(pathMap):
	for row in pathMap:
		if None in row:
			return True
	return False
def pathMapFormater(val,x,y, outPut1, outPut2):
    if val == 1 or x == 21 or y == 16 or x == 0 or y == 0:
        return outPut1
    return outPut2
global imagePath
imagePath = None
def pathfinder(gameMap,startPos,endPos):
    global imagePath
    pathfinder_map = [[pathMapFormater(gameMap[y][x],x,y,-1,None) for x in range(len(gameMap[y]))] for y in range(len(gameMap))]

    pathfinder_map[startPos[1]][startPos[0]] = 0
    counter = 1
    supa = []
    while NoneChecker(pathfinder_map):
        for y in range(0,len(pathfinder_map)-1):
            for x in range(0,len(pathfinder_map[y])-1):
    			
                temp = list(set([pathfinder_map[y-1][x],pathfinder_map[y][x+1],pathfinder_map[y+1][x],pathfinder_map[y][x-1]]))
                if None in temp:
                    del temp[temp.index(None)]
                if -1 in temp:
                    del temp[temp.index(-1)]
                if len(temp) != 0 and pathfinder_map[y][x]==None:
                    pathfinder_map[y][x] = min(temp)+1
        counter+=1
    #printMap(pathfinder_map)

    tempPos = endPos
    while True:
        lowestVal = None
        try:
            n = pathfinder_map[tempPos[1]-1][tempPos[0]]
        except:
            n = -1
        try:
            e = pathfinder_map[tempPos[1]][tempPos[0]+1]
        except:
            e = -1
        try:
            s = pathfinder_map[tempPos[1]+1][tempPos[0]]
        except:
            s = -1
        try:
            w = pathfinder_map[tempPos[1]][tempPos[0]-1]
        except:
            w = -1
        try:
            pathfinder_map[tempPos[1]][tempPos[0]] = -2 
        except:
            pass
        if n == 0:
            imagePath = testMap(pathfinder_map,mode="path")
            return "s"
        elif e == 0:
            imagePath = testMap(pathfinder_map,mode="path")
            return "w"
        elif s == 0:
            imagePath = testMap(pathfinder_map,mode="path")
            return "n"
        elif w == 0:
            imagePath = testMap(pathfinder_map,mode="path")
            return "e"
        try:        
            validOption = list(set([n,e,s,w]))
        
            if -1 in validOption:
                del validOption[validOption.index(-1)]
            #-2  = previous pos
            if -2 in validOption:
                del validOption[validOption.index(-2)]

            lowestVal = min(validOption)
        except Exception as error:
            pass
        if lowestVal == n:
            tempPos = [tempPos[0],tempPos[1]-1]
        elif lowestVal == e:
            tempPos = [tempPos[0]+1,tempPos[1]]
        elif lowestVal == s:
            tempPos = [tempPos[0],tempPos[1]+1]
        elif lowestVal == w:
            tempPos = [tempPos[0]-1,tempPos[1]]

def run(gameMap,enemyPos):
    global imagePath
    safeZones = [[pathMapFormater(gameMap[y][x],x,y,-1,None) for x in range(len(gameMap[y]))] for y in range(len(gameMap))]

    safeZones[enemyPos[1]][enemyPos[0]] = 0
    counter = 1
    supa = []
    while NoneChecker(safeZones):
        for y in range(0,len(safeZones)-1):
            for x in range(0,len(safeZones[y])-1):
    			
                temp = list(set([safeZones[y-1][x],safeZones[y][x+1],safeZones[y+1][x],safeZones[y][x-1]]))
                if None in temp:
                    del temp[temp.index(None)]
                if -1 in temp:
                    del temp[temp.index(-1)]
                if len(temp) != 0 and safeZones[y][x]==None:
                    safeZones[y][x] = min(temp)+1
        counter+=1
    tempRow = []
    for y in range(0,len(safeZones)-1):
        tempRow.append(max(safeZones[y]))
    #printMap(safeZones)
    #print(safeZones[tempRow.index(max(tempRow))].index(safeZones[tempRow.index(max(tempRow))][safeZones[tempRow.index(max(tempRow))].index(max(tempRow))]),safeZones.index(safeZones[tempRow.index(max(tempRow))]))
    return [safeZones[tempRow.index(max(tempRow))].index(safeZones[tempRow.index(max(tempRow))][safeZones[tempRow.index(max(tempRow))].index(max(tempRow))]),safeZones.index(safeZones[tempRow.index(max(tempRow))])]
def testMap(mapInput,mode="map"):
    img = Image.new('RGB', (22, 17), color = (225, 0, 0))

    for y in range(len(mapInput)):
        for x in range(len(mapInput[y])):
            if mode == "map":
                if mapInput[y][x] == 1:
                    img.putpixel((x,y),(225,225,225))
                elif mapInput[y][x] == 2:
                    img.putpixel((x,y),(0,0,0))
                elif mapInput[y][x] == 3:
                    img.putpixel((x,y),(0,225,0))
                elif mapInput[y][x] == 4:
                    img.putpixel((x,y),(0,0,225))
            else:
                if mapInput[y][x] == -1:
                    img.putpixel((x,y),(225,225,225))
                elif mapInput[y][x] == -2:
                    img.putpixel((x,y),(0,0,0))
                else:
                    img.putpixel((x,y),(max(round(-1*math.pow(mapInput[y][x]-35,2)+225),0),max(round(-1*math.pow(mapInput[y][x]-17.5,2)+225),0),max(round(-1*math.pow(mapInput[y][x],2)+225),0)))
    
    return img

    
def turnTank(my_tank,heading,ideal):

    angleFromRight = ideal-heading
    angleFromLeft = heading-ideal
    
    if angleFromRight< 0:
        angleFromRight+=360
    if angleFromLeft <0:
        angleFromLeft+=360

    if angleFromRight <= angleFromLeft:
        my_tank.turn_right()
    else:
        my_tank.turn_left()

global label1
global label2
label1= None
label2 = None
def windowUpdate(image1,image2):
    global label1
    global label2
    global root
    img = Image.new('RGB', (22, 17*2+1), color = (225, 225, 225))
    
    for y in range(17):
        for x in range(22):
            pixelColour=image1.getpixel((x,y))
            img.putpixel((x,y),pixelColour)
                
    for y in range(17):
        for x in range(22):
            pixelColour=image2.getpixel((x,y))
            img.putpixel((x,17+1+y),pixelColour)
        
    img = img.resize((22*15,(17*2+1)*15), Image.ANTIALIAS)
    imageTemp = ImageTk.PhotoImage(img)
    if label1 == None:
        label1 = tk.Label(root, image=imageTemp)
    else:
        label1.config(image=imageTemp)
    label1.pack()
    root.update()

def forwardCheck(my_tank):
    heading = my_tank.my_heading()
    sensors = my_tank.checkSensors()
    if heading > 315 or heading <=45:
        return sensors["n"]
    elif 45 < heading and heading >= 135:
        return sensors["e"]
    elif 135 < heading and heading >= 225:
        return sensors["s"]
    else:
        return sensors["w"]
    
def scoutingTarget(gameMap):
    for y in range(0,len(gameMap)-1):
        for x in range(0,len(gameMap[y])-1):
            if gameMap[y][x] == 0:
                return [x,y]
    return False
global c
c = 100

def turretAim(my_tank,target):

    angle = None
    #does targeting based on point
    if type(target) is tuple:
        xChange = abs(my_tank.my_position()[0]-target[0])
        yChange = abs(my_tank.my_position()[1]-target[1])
        try:
            refAngle = math.atan(yChange/xChange)
            #quadrant 1
            if my_tank.my_position()[0] <= target[0] and my_tank.my_position()[1] >= target[1]:
                angle = refAngle
            #quadrant 2
            elif my_tank.my_position()[0] >= target[0] and my_tank.my_position()[1] >= target[1]:
                angle = math.pi - refAngle
            #quadrant 3
            elif my_tank.my_position()[0] >= target[0] and my_tank.my_position()[1] <= target[1]:
                angle = math.pi + refAngle
            #quadrant 4
            else:
                angle = 2*math.pi - refAngle
            
        except Exception as e:
            if my_tank.my_position()[1] < target[1]:
                angle = math.pi/2
            else:
                angle = 3*math.pi/2
            
        #changes the refrence point
        if angle >= math.pi/2:
            angle = math.degrees(math.pi/2 + 2*math.pi - angle)
        else:
            angle = math.degrees(math.pi/2 - angle)
    #does targeting based on required angle
    else:
        angle = target

    angleFromRight = angle-my_tank.turret_direction()
    angleFromLeft = my_tank.turret_direction()-angle
    if angleFromRight< 0:
        angleFromRight+=360
    if angleFromLeft < 0:
        angleFromLeft+=360
    for i in range(3):
        if angleFromRight <= angleFromLeft:
            my_tank.rotate_right()
        else:
            my_tank.rotate_left()
    if abs(angle-my_tank.turret_direction()) <10:
        return True
    return False
global C2
c2 = 0
def patrolChecker(myPos):
    global patrolMode
    global c2
    global lastPos
    patrolNodes = [[1,1],[20,1],[20,15],[1,15]]
        patrolMode = 0
    if myPos == patrolNodes[patrolMode] and lastPos != myPos:
        patrolMode+=1
        try:
            temp = patrolNodes[patrolMode+1]
            
        except Exception as e:
            temp = patrolNodes[0]
            patrolMode = 0
    elif patrolMode == None:
        distances = []
        for point in patrolNodes:
            distances.append(abs(myPos[0]-point[0])+abs(myPos[1]-point[0]))
        patrolMode = patrolNodes.index(patrolNodes[distances.index(min(distances))])
        temp = patrolNodes[distances.index(min(distances))]
    else:
        temp = patrolNodes[patrolMode]
    return temp

def unkownChecker():
    global gameMap
    for row in gameMap:
        if 0 in row:
            return True
    return False
def enemyLastPositionChecker():
    global gameMap
    for row in gameMap:
        if 4 in row:
            return True
    return False
def enemyLastPostion():
    global gameMap
    for y in range(len(gameMap)):
        for x in range(len(gameMap[y])):
            if gameMap[y][x] == 4:
                return [x,y]
        
def aiModeDecider(my_tank):
    global loaded
    if my_tank.clear_shot() and loaded:
        return "hit"
    elif not loaded:
        return "run"
    elif unkownChecker():
        return "scout"
    elif enemyLastPositionChecker() and loaded:
        return "chase"
    else:
        return "patrol"
def action(my_tank):
    global gameMap
    global lastMove
    global root
    
    global imagePath
    global aiMode
    global target
    global lastMove
    global lastPos
    global c
    global c2
    global reloadingTime
    global loaded
    global patrolMode

    my_tank.set_name("The Teriminator")
    
    #Set AI enemy level
    my_tank.set_enemy_lvl(4)

    if my_tank.clear_shot():
        if turretAim(my_tank,my_tank.enemy_position()):
            if loaded:
                my_tank.fire()
                loaded = False
    else:
        turretAim(my_tank,my_tank.my_heading())
    gameMap = mapUpdater(my_tank)
    #printMap(gameMap)
    for y in range(len(gameMap)):
        for x in range(len(gameMap[y])):
            if gameMap[y][x] == 3:
                gameMap[y][x] = 2
            elif gameMap[y][x] == 4 and my_tank.clear_shot():
                gameMap[y][x] = 2
    gameMap[int(math.floor(my_tank.my_position()[1]/60))+1][int(math.floor(my_tank.my_position()[0]/60))+1] = 3
    if not type(my_tank.enemy_position()) is bool:
        gameMap[int(math.floor(my_tank.enemy_position()[1]/60))+1][int(math.floor(my_tank.enemy_position()[0]/60))+1] = 4
        
    aiMode = aiModeDecider(my_tank)
    
    if aiMode == "scout":
        target = scoutingTarget(gameMap)
        patrolMode = None
    elif aiMode == "chase":
        target = enemyLastPostion()#change to last seen enemyPostion
        patrolMode = None
    elif aiMode == "hit":
        target = [math.floor(my_tank.enemy_position()[0]/60)+1,math.floor(my_tank.enemy_position()[1]/60+1)]
        patrolMode = None
    elif aiMode == "run":
        target = run(gameMap,enemyLastPostion())
        patrolMode = None
    elif aiMode == "patrol":
        target = patrolChecker([int(math.floor(my_tank.my_position()[0]/60))+1,int(math.floor(my_tank.my_position()[1]/60))+1])
        
        
    c2+=1

    #printMap(gameMap)
    direction = pathfinder(gameMap,[math.floor(my_tank.my_position()[0]/60+1),math.floor(my_tank.my_position()[1]/60+1)],target)
    #windowUpdate(testMap(gameMap),imagePath)
    #print(c)
   # print(lastPos)
    #print([my_tank.my_position()[0],my_tank.my_position()[1]])
    if (lastMove == "forward" or lastMove == "stuck") and lastPos == [my_tank.my_position()[0],my_tank.my_position()[1]]:
        my_tank.turn_right()
        my_tank.turn_right()
        my_tank.forward()
        lastMove = "stuck"
        if c%5==0:
            c = 0
            if lastPos != [my_tank.my_position()[0],my_tank.my_position()[1]]:
                lastMove = None
    elif direction == "e":
        if my_tank.my_heading() != 90:
            if my_tank.checkSensors()["e"]:
                my_tank.forward()
                lastMove = "forward"
            else:
                if not forwardCheck(my_tank):
                    my_tank.forward()
                temp = 90
                turnTank(my_tank,my_tank.my_heading(),temp)
                turnTank(my_tank,my_tank.my_heading(),temp)
                turnTank(my_tank,my_tank.my_heading(),temp)
                lastMove = "turn"
        else:
            my_tank.forward()
            lastMove = "forward"
    elif direction == "w":
        if my_tank.my_heading() != 270:
            if  my_tank.checkSensors()["w"]:
                my_tank.forward()
                lastMove = "forward"
            else:
                if not forwardCheck(my_tank):
                    my_tank.forward()
                temp = 270
                turnTank(my_tank,my_tank.my_heading(),temp)
                turnTank(my_tank,my_tank.my_heading(),temp)
                turnTank(my_tank,my_tank.my_heading(),temp)
            lastMove = "turn"
        else:
            my_tank.forward()
            lastMove = "forward"
    elif direction == "n":
        if my_tank.my_heading() != 0:
            if  my_tank.checkSensors()["n"]:
                my_tank.forward()
                lastMove = "forward"
            else:
                if not forwardCheck(my_tank):
                    my_tank.forward()
                
                temp = 0
                turnTank(my_tank,my_tank.my_heading(),temp)
                turnTank(my_tank,my_tank.my_heading(),temp)
                turnTank(my_tank,my_tank.my_heading(),temp)
                lastMove = "turn"
        else:
            my_tank.forward()
            lastMove = "forward"
    else:
        if my_tank.my_heading() != 180:
            if  my_tank.checkSensors()["s"]:
                my_tank.forward()
                lastMove = "forward"
            else:
                if not forwardCheck(my_tank):
                    my_tank.forward()
                
                temp = 180
                turnTank(my_tank,my_tank.my_heading(),temp)
                turnTank(my_tank,my_tank.my_heading(),temp)
                turnTank(my_tank,my_tank.my_heading(),temp)
                lastMove = "turn"
        else:
            my_tank.forward()
            lastMove = "forward"
    if c >= 50:
        lastPos = [my_tank.my_position()[0],my_tank.my_position()[1]]
        c = 0
    else:
        c+=1
    if not loaded:
        reloadingTime+=1
    if reloadingTime == 50:
        reloadingTime = 0
        loaded = True
    #print(target)

