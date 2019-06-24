import pygame, random
from math import *
from pygame import *

def distanceBetween(x1, y1, x2, y2):
		return sqrt(y2 - y1)**2 + (x2 - x1)**2

def angleBetween(x, y1, x2, y2):

	if x2 == False or y2 == False:
		return 180

	x1 = x
	
	if x2 == x1:
		print("subratced")
		x1 += 2
	
	try:
		angle = atan(((y1 - y2) / (x2 - x1))) * (180 / pi)
	except:
		angle = atan(((y1 - y2) / 1)) * (180 / pi)


	angle = standardAngle(angle)
	
	if x2 - x1 <= 0 and y1 - y2 <= 0 and angle >= 0 and angle <= 90 or x2 - x1 < 0 and y1 - y2 > 0 and angle > 270 and angle < 360 : 
		angle += 180
	
	return standardAngle((angle))

def standardAngle(angle):
	while angle < 0: 
		angle += 360

	while angle >= 360: 
		angle -= 360
	return angle

def setTurretHeading(angle, my_tank):
	#while True:

	# print("Dumb GAme")


	if my_tank.my_heading() - angle < -2 or my_tank.my_heading() - angle > 2:
		if my_tank.turret_direction() > angle:
			my_tank.rotate_left()
		elif my_tank.turret_direction() < angle:
			my_tank.rotate_right()








def setHeading(angle, my_tank):

	if my_tank.my_heading() != angle:
		if my_tank.my_heading() > angle:
			my_tank.turn_left()
		elif my_tank.my_heading() < angle:
			my_tank.turn_right()
	elif my_tank.my_heading() == angle:
		#print("asdjogfndjosgnodfgnodfg")
		isTurning[0] = False
		isTurning[1] = 0



isTurning = [False, 0]
directions = {"n": 0, "e": 90, "s": 180, "w": 270}
directionsLetters = ["n", "e", "s", "w"]

def action(my_tank):

	#Set AI enemy level
	my_tank.set_enemy_lvl(4)
	my_tank.set_Name("Headache")

	if len(my_tank.enemy_tanks())>0:
		enemyHeading = standardAngle((angleBetween(my_tank.my_position()[0], my_tank.my_position()[1], my_tank.enemy_tanks()[0][0], my_tank.enemy_tanks()[0][1]) + 270) / (-1))
	else:
		enemyHeading = 0
	setTurretHeading(enemyHeading, my_tank)

	if my_tank.enemy_tanks():
		#if enemyHeading - my_tank.my_heading() > -10 and enemyHeading - my_tank.my_heading() < 10:
		my_tank.fire()
		#print("kachow")


	
	surroundings = my_tank.checkSensors()

	print(surroundings)
	oldCoords = my_tank.my_position()


	preferredDirection = 0

	if enemyHeading > 45 and enemyHeading < 135:
		preferredDirection = 90
	elif enemyHeading > 135 and enemyHeading < 225:
		preferredDirection = 180
	elif enemyHeading > 225 and enemyHeading < 315:
		preferredDirection = 270
	elif (enemyHeading > 315 and enemyHeading < 360) or (enemyHeading > 0 and enemyHeading < 45):
		preferredDirection = 0
	
	if not isTurning[0]:
		#print("helo")
		randomSeed = random.randint(0, 1)

		#move in perfered direction if no obsticals
		'''
		if not surroundings["n"] and not surroundings["e"] and not surroundings["s"] and not surroundings["w"]:
			if my_tank.my_heading() != preferredDirection:
				isTurning[0] = True
				isTurning[1] = preferredDirection
			else:
				my_tank.forward()
		elif surroundings["n"] and my_tank.my_heading() == 0: #object in front
				isTurning[0] = True
				isTurning[1] = 90
		elif surroundings["e"] and my_tank.my_heading() == 90:
				isTurning[0] = True
				isTurning[1] = 180
		elif surroundings["s"] and my_tank.my_heading() == 180:
				isTurning[0] = True
				isTurning[1] = 270
		elif surroundings["w"] and my_tank.my_heading() == 270:
				isTurning[0] = True
				isTurning[1] = 0
		elif surroundings["n"] and my_tank.my_heading() != 0: #object in front
				my_tank.forward()
		elif surroundings["e"] and my_tank.my_heading() != 90: #object in front
				my_tank.forward()
		elif surroundings["s"] and my_tank.my_heading() != 180: #object in front
				my_tank.forward()
		elif surroundings["w"] and my_tank.my_heading() != 270: #object in front
				my_tank.forward()
		else:
			my_tank.forward()


		if oldCoords == my_tank.my_position():
			isTurning[0] = True

			if randomSeed == 0:
				isTurning[1] = standardAngle(my_tank.my_heading() + 90)
			elif randomSeed == 1:
				isTurning[1] = standardAngle(my_tank.my_heading() - 90)
			elif randomSeed == 2:
				isTurning[1] = standardAngle(my_tank.my_heading() + 180)
			else:
				my_tank.forward()
			'''
		
		#if my_tank.clear_shot():
		#	if my_tank.my_heading() - enemyHeading > -5 and my_tank.my_heading() - enemyHeading < 5:
		#		my_tank.forward()
		#	else:
		#		isTurning[0] = True 
		#		isTurning[1] = enemyHeading

		if surroundings["n"] and my_tank.my_heading() == 0:
			#print("gello")

			isTurning[0] = True 

			if randomSeed == 0:
				isTurning[1] = 270
			else:
				isTurning[1] = 90
			
		
		elif surroundings["s"] and my_tank.my_heading() == 180:
			isTurning[0] = True 

			if randomSeed == 0:
				isTurning[1] = 90
			else:
				isTurning[1] = 270

		elif surroundings["e"] and my_tank.my_heading() == 90:
			isTurning[0] = True 

			if randomSeed == 0:
				isTurning[1] = 0
			else:
				isTurning[1] = 180

		elif surroundings["w"] and my_tank.my_heading() == 270:
			isTurning[0] = True 

			if randomSeed == 0:
				isTurning[1] = 180
			else:
				isTurning[1] = 0
		
		else: 
			#print("hello")
			#if not my_tank.clear_shot():

			
			#for i in directionsLetters:
			#	if not surroundings[i] and directions[i] == preferredDirection:
			#		print("yippie")
			#		if my_tank.my_heading() != preferredDirection:
			#			isTurning[0] = True 
			#			isTurning[1] = preferredDirection
			#		else:
			#			my_tank.forward()
			


			my_tank.forward()
		
	elif isTurning[0]:
		#print("gewy")
		setHeading(isTurning[1], my_tank)



	
	'''
	if surroundings["n"]:
		setHeading(270, my_tank)
	
	elif surroundings["s"]:
		setHeading(90, my_tank)

	elif surroundings["e"]:
		setHeading(0, my_tank)

	elif surroundings["w"]:
		setHeading(180, my_tank)
	
	else:
		setHeading(enemyHeading, my_tank)
		
	if not my_tank.clear_shot():
		my_tank.forward()

	oldCoords = my_tank.my_position()
	'''
	
	#if oldCoords == my_tank.my_position():
		#setHeading(standardAngle(my_tank.my_heading() + 180), my_tank)
	
	
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
