import sys
import pygame
import time

from pygame.locals import *


pygame.init()
windowWidth = 720
windowHeight = 480
clock = pygame.time.Clock()

displaySurface = pygame.display.set_mode((windowWidth,windowHeight))

done = False
WHITE = [255, 255, 255]

class tank:
	"""docstring for tank"""
	def __init__(self, name, colour, x, y):
		self.name = name
		if colour == "blue":
			self.colour = [0,0,255]
		elif colour == "green":
			self.colour = [0,255,0]
		elif colour == "red":
			self.colour = [255,0,0]
		self.x = x
		self.y = y
		self.direction = 0
		# self.angle = 0

	def moveRight(self):
		# self.angle = 0
		if self.x < windowWidth - 50:
			self.x += 10
		else:
			self.x = windowWidth-50
		self.direction = 0

	def moveLeft(self):
		# self.angle = 180
		if self.x > 0:
			self.x -= 10
		else:
			self.x = 0
		self.direction = 180

	def moveUp(self):
		# self.angle = 90
		if self.y > 0:
			self.y -= 10
		else:
			self.y = 0
		self.direction = 90

	def moveDown(self):
		# self.angle = 270
		if self.y < windowHeight-50:
			self.y += 10
		else:
			self.y = windowHeight-50
		self.direction = 270

	def draw(self):
		pygame.draw.rect(displaySurface,(self.colour),[self.x, self.y,50,50])

class bullet:
	"""docstring for bullet"""
	def __init__(self, x, y, direction, bulletID):
		self.x = x
		self.y = y
		self.id = bulletID
		self.direction = direction
		if self.direction == 0 or self.direction == 270:
			self.change = 1
		else:
			self.change = -1
		self.flying = True
		if self.direction %180==0:
			self.x += 35*self.change
		else:
			self.y += 35*self.change

	def collisionCheck(self):
		if self.x < 20 or self.x > windowWidth - 20 or self.y < 20 or self.y > windowHeight-20:
			bullets.remove(self.id)

	def draw(self):
		pygame.draw.rect(displaySurface,([0,0,0]),[self.x, self.y, 10,10])
		if self.direction %180==0:
			self.x += 25*self.change
		else:
			self.y += 25*self.change

tanks = []
bullets = []

blueTank = tank("Blue Tank", "blue", 100, 100)
redTank = tank("Red Tank", "red", 500, 350)

tanks.append(blueTank)
tanks.append(redTank)

fired = False

while not done:
	keys=pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	if keys[K_LEFT]:
		blueTank.moveLeft()
	if keys[K_RIGHT]:
		blueTank.moveRight()
	if keys[K_UP]:
		blueTank.moveUp()
	if keys[K_DOWN]:
		blueTank.moveDown()
	if keys[K_SPACE]:
		if not fired:
			bullets.append(bullet(blueTank.x+20, blueTank.y+20, blueTank.direction, len(bullets)))
			fired = True
	else:
		fired = False
	
	displaySurface.fill(WHITE)
	for x in tanks:
		x.draw()
	for x in bullets:
		x.draw()
	
	pygame.display.flip()
	clock.tick(60)