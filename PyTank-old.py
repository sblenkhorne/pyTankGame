#! /usr/bin/env python3

# PyTank - By Andrew Groeneveldt and Scott Blenkhorne
# November 2018


import pygame, os, random, green_control, blue_control, mapGen
from pygame.locals import *

# import maps

all_sprites = pygame.sprite.LayeredUpdates()
green_shots = pygame.sprite.Group()
blue_shots = pygame.sprite.Group()
enviro_sprites = pygame.sprite.Group()
tanks_sprites = pygame.sprite.Group()
"""
Load map from map.py
0 - Empty map. Good for creating an AI without any obstacles
1 - Basic rectangle in the middle of the map
2 - Maze map
"""
maze_maps = mapGen.getMaps()
maze_map = maze_maps[random.randint(0,len(maze_maps)-1)]


def load_image(filename,x=None,y=None):
    """Load an image from file
        takes: an image filename and desired dimensions
        returns: a converted image object
        assumes: file is in local subdirectory assets/
        image has transparency
        """
    image = pygame.image.load(os.path.join("assets", filename)).convert_alpha()
    if x and y: image = pygame.transform.smoothscale(image,(x,y))
    return image


def rotate_ip(self, angle):
    """ Rotate an image about its center
        takes: self, angle
        returns: new image
        assumes: aspect ratio of 1:1
        """
    location = self.rect.center
    new_image = pygame.transform.rotate(self.base_image, angle)
    self.rect = new_image.get_rect(center=location)
    return new_image


# helper function for clear shot sensor
def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C
    
def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return int(x),int(y)
    else:
        return False

class Wall(pygame.sprite.Sprite):
    """Class to represent obstacles"""

    def __init__(self,position,orientation): # don't need orientation anymore
        pygame.sprite.Sprite.__init__(self)
        all_sprites.add(self, layer = 0)
        enviro_sprites.add(self)
        self.image = load_image('stoneWall.png',60,60)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft = (position[0],position[1]))

class Shot(pygame.sprite.Sprite):
    """Class to represent and control projectiles"""
    
    def __init__(self, position, heading):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = load_image('bullet.png',15,15)
        self.image = self.base_image
        self.area = pygame.display.get_surface().get_rect()
        self.rect = self.image.get_rect(center=position)
        self.radius = 6
        self.heading = heading * 1
        self.image = rotate_ip(self, self.heading.angle_to(pygame.math.Vector2(0, -1)))
        self.rect.move_ip(self.heading)
    
    def update(self):
        """ update shot position """
        self.rect.move_ip(self.heading)
        if pygame.sprite.spritecollideany(self, enviro_sprites) or not self.area.contains(self.rect): self.kill()

class wallSensor():
    """docstring for ClassName"""
    def __init__(self, tank, side):
        pygame.sprite.Sprite.__init__(self)
        if side=='w':
            self.rect = Rect(tank.rect.topleft,(20,30))
            self.color = (100,100,0)
        elif side == 'e':
            self.rect = Rect(tank.rect.topright,(20,30))
            self.color = (255,0,0)
        elif side == 'n':
            self.rect = Rect(tank.rect.topleft,(30,20))
            self.color = (0,255,0)
        elif side == 's':
            self.rect = Rect(tank.rect.bottomleft,(30,20))
            self.color = (0,0,255)
        

class Turret(pygame.sprite.Sprite):
    """Class to represent gun turrets"""

    def __init__(self,tank,colour,heading):
        pygame.sprite.Sprite.__init__(self)
        all_sprites.add(self, layer = 1)
        image_file = colour + 'Barrel.png'
        self.base_image = load_image(image_file,24,96)
        self.image = self.base_image
        self.rect = self.image.get_rect(center=tank.rect.center)
        self.heading = heading * 2
        if colour == 'green': self.image = rotate_ip(self, self.heading.angle_to(pygame.math.Vector2(0, -1)))


class Tank(pygame.sprite.Sprite):
    """Class to represent and control tanks"""
    
    def __init__(self,colour = 'blue',position = (600,400)):
        pygame.sprite.Sprite.__init__(self)
        if colour != 'green' and colour != 'blue': colour = 'green'
        all_sprites.add(self, layer = 0)
        tanks_sprites.add(self)
        image_file = colour + 'Tank.png'

        # Load sound effects
        self.tankFireSound = pygame.mixer.Sound("sounds/tankFire.wav")
        self.tankExplosion = pygame.mixer.Sound("sounds/tankExplosion.wav")
        self.base_image = load_image(image_file,75,75)
        self.image = self.base_image
        self.rect = self.image.get_rect(center=position)
        self.speed = 10
        self.colour = colour
        self.AIlevel = 1
        if self.colour == 'green':
            self.control = green_control
            self.shot_group = green_shots
            self.name = "Green Tank"
            self.heading = pygame.math.Vector2(0, self.speed)
            self.image = rotate_ip(self, self.heading.angle_to(pygame.math.Vector2(0, -1)))
        else:
            self.control = blue_control
            self.shot_group = blue_shots
            self.name = "Blue Tank"
            self.heading = pygame.math.Vector2(0, -self.speed)
        self.mask = pygame.mask.from_surface(self.image)
        self.radius = 35
        self.__health = 2
        self.turret = Turret(self,colour,self.heading)
        self.nSensor = wallSensor(self,'n')
        self.sSensor = wallSensor(self,'s')
        self.wSensor = wallSensor(self,'w')
        self.eSensor = wallSensor(self,'e')
        self.cooldown = 0
        self.moved = False
        self.turned = False
        self.rotated = False
        self.fired = False
        
    def set_enemy(self, tank):
        self.enemy = tank
    
    def set_Name(self, newName):
        self.name = newName
    
    def takeDamage(self):
        self.__health -= 1
        self.speed -= 3             # self.speed is not used anywhere after init?
        pygame.mixer.Sound.play(self.tankExplosion)
        if self.__health > 0:
            return False
            self.heading = self.heading.scale_to_length(0.5) # this never executes
        else:
            self.kill()
            return True

    def status(self):
    	if self.__health < 2:
    		return True
    	else:
    		return False

    def kill(self):
        self.turret.kill()
        pygame.sprite.Sprite.kill(self)

    def respawn(self):          # need a new way to do this that doesn't leave an invisible corpse!
        self.__health = 2
        self.speed = 10
        if self.colour == 'green':
            self.heading = pygame.math.Vector2(0, self.speed)
        else:
            self.heading = pygame.math.Vector2(0, -self.speed)
        all_sprites.add(self, layer = 0)
        tanks_sprites.add(self)
        all_sprites.add(self.turret, layer = 1)

    def checkSensors(self):
        sensors = {'n':False,'s':False,'w':False,'e':False}
        if pygame.sprite.spritecollideany(self.nSensor,enviro_sprites,collided=pygame.sprite.collide_circle): sensors['n']=True
        if pygame.sprite.spritecollideany(self.sSensor,enviro_sprites,collided=pygame.sprite.collide_circle): sensors['s']=True
        if pygame.sprite.spritecollideany(self.wSensor,enviro_sprites,collided=pygame.sprite.collide_circle): sensors['w']=True
        if pygame.sprite.spritecollideany(self.eSensor,enviro_sprites,collided=pygame.sprite.collide_circle): sensors['e']=True
        return sensors        

    # def get_walls(self):
    #     if self.rect.center[0] < 0 or self.rect.center[0] >= 1200:
    #         return maze_map[24]
    #     if self.rect.center[1] < 0 or self.rect.center[1] >= 800:
    #         return maze_map[25]
    #     return maze_map[6 * (self.rect.center[1]//200) + self.rect.center[0]//200]

    def my_position(self):
        return self.rect.center
    
    def enemy_position(self):
        return self.enemy.rect.center
    
    def set_enemy_lvl(self,lvl):
        self.enemy.AIlevel = lvl

    def my_heading(self):
        return (360-((round(int(self.heading.angle_to(pygame.math.Vector2(0,-1)))<<1,-1))>>1))%360
    
    def turret_direction(self):
        return (360-((round(int(self.turret.heading.angle_to(pygame.math.Vector2(0,-1)))<<1,-1))>>1))%360

    def clear_shot(self):          # need to examine this closer, may not work as intended with new walls
        maxx = self.rect.center[0] if self.rect.center[0] >= self.enemy.rect.center[0] else self.enemy.rect.center[0]
        maxy = self.rect.center[1] if self.rect.center[1] >= self.enemy.rect.center[1] else self.enemy.rect.center[1]
        minx = self.rect.center[0] if self.rect.center[0] <= self.enemy.rect.center[0] else self.enemy.rect.center[0]
        miny = self.rect.center[1] if self.rect.center[1] <= self.enemy.rect.center[1] else self.enemy.rect.center[1]
        L = line(self.rect.center,self.enemy.rect.center)
        area = pygame.display.get_surface()     # not used
        for x in range(0,1201,60):
            i = intersection(L,line((x,0),(x,900)))
            if i and minx <= x <= maxx:
                for wall in enviro_sprites.sprites():
                    if wall.rect.collidepoint(i): 
                        # pygame.draw.line(area,(255,255,255),self.rect.center,self.enemy.rect.center,1)
                        return False
        for y in range(0,901,60):
            i = intersection(L,line((0,y),(1200,y)))
            if i and miny <= y <= maxy:
                for wall in enviro_sprites.sprites():
                    if wall.rect.collidepoint(i): 
                        # pygame.draw.line(area,(255,255,255),self.rect.center,self.enemy.rect.center,1)
                        return False
        
        return True
    
    def forward(self):
        if self.moved: return False
        self.moved = True
        self.rect.move_ip(self.heading)
        if pygame.sprite.collide_mask(self, self.enemy):
            self.rect.move_ip(-self.heading)
            return False
        if pygame.sprite.spritecollideany(self, enviro_sprites, collided = pygame.sprite.collide_mask):
            self.rect.move_ip(-self.heading)
            return False
        if self.rect.x + self.rect.width < 60 or self.rect.x>1180: # adjust so no catching on edge?
            self.rect.move_ip(-self.heading)
            return False
        if self.rect.y + self.rect.height < 60 or self.rect.y>900:
            self.rect.move_ip(-self.heading)
            return False
        return True
    
    def turn_left(self):
        if self.turned: return
        self.turned = True
        self.heading.rotate_ip(-5)
        self.image = rotate_ip(self, self.heading.angle_to(pygame.math.Vector2(0, -1)))
        self.mask = pygame.mask.from_surface(self.image)
    
    def turn_right(self):
        if self.turned: return
        self.turned = True
        self.heading.rotate_ip(5)
        self.image = rotate_ip(self, self.heading.angle_to(pygame.math.Vector2(0, -1)))
        self.mask = pygame.mask.from_surface(self.image)
    
    def rotate_left(self):
        if self.rotated: return
        self.rotated = True
        self.turret.heading.rotate_ip(-3)
        self.turret.image = rotate_ip(self.turret, self.turret.heading.angle_to(pygame.math.Vector2(0, -1)))
        
    def rotate_right(self):
        if self.rotated: return
        self.rotated = True
        self.turret.heading.rotate_ip(3)
        self.turret.image = rotate_ip(self.turret, self.turret.heading.angle_to(pygame.math.Vector2(0, -1)))

    def fire(self):
        if self.fired: return
        if self.cooldown != 0: return
        self.fired = True
        shot = Shot(self.rect.center, self.turret.heading)
        self.shot_group.add(shot)
        all_sprites.add(shot)
        self.cooldown = 50
        pygame.mixer.Sound.play(self.tankFireSound)
    
    def drawHealthBar(self):
        healthRect = pygame.Rect(self.rect.center[0]-40,self.rect.center[1]-50,80*self.__health/2,10)
        healthOutline = pygame.Rect(self.rect.center[0]-40,self.rect.center[1]-50,80,10)
        if self.__health == 2:
            rectCol = (0,255,0)
        else:
            rectCol = (255, 160, 0)
        pygame.draw.rect(pygame.display.get_surface(),rectCol,healthRect,0)    	
        pygame.draw.rect(pygame.display.get_surface(),(0,0,0),healthOutline,1)


    def drawTankName(self):
        nameTxt = pygame.font.Font('freesansbold.ttf',15)
        textSurf, textRect = text_objects(str(self.name), nameTxt, (0,0,0))
        textRect.center = (self.rect.center[0], self.rect.center[1]-60)
        pygame.display.get_surface().blit(textSurf, textRect)

    def update(self):
        """ update tank heading and position """
        
        if self.cooldown > 0:
            self.cooldown -= 1

        # get control input
        self.control.action(self)

        # wrap screen
        # if self.rect.x + self.rect.width < 0:
        #     self.rect.x = 1200
        # if self.rect.y + self.rect.height < 0:
        #     self.rect.y = 800
        # if self.rect.x > 1200:
        #     self.rect.x = -self.rect.width
        # if self.rect.y > 800:
        #     self.rect.y = -self.rect.height

        # move turret with tank
        self.turret.rect.center = self.rect.center
        self.nSensor.rect.center = (self.rect.center[0], self.rect.center[1] - 25)
        self.sSensor.rect.center = (self.rect.center[0], self.rect.center[1] + 25)
        self.wSensor.rect.center = (self.rect.center[0]-25, self.rect.center[1])
        self.eSensor.rect.center = (self.rect.center[0]+25, self.rect.center[1])
        # pygame.draw.rect(pygame.display.get_surface(),self.nSensor.color,self.nSensor.rect,0)
        # pygame.draw.rect(pygame.display.get_surface(),self.sSensor.color,self.sSensor.rect,0)
        # pygame.draw.rect(pygame.display.get_surface(),self.wSensor.color,self.wSensor.rect,0)
        # pygame.draw.rect(pygame.display.get_surface(),self.eSensor.color,self.eSensor.rect,0)

        if self.__health > 0:
        	self.drawHealthBar()
        # clear action flags
        self.drawTankName()
        self.moved = False
        self.turned = False
        self.rotated = False
        self.fired = False

def text_objects(text, font, txtColour):
    textSurface = font.render(text, True, txtColour)
    return textSurface, textSurface.get_rect()

def message_display(text, txtColour, fntSize):
    largeText = pygame.font.Font('freesansbold.ttf',fntSize)
    TextSurf, TextRect = text_objects(str(text), largeText, txtColour)
    TextRect.center = (600,450)
    pygame.display.get_surface().blit(TextSurf, TextRect)
    pygame.display.update()

def countdown(cntDown):
    if cntDown >0:
        message_display(cntDown, (0,0,0), 200)
    return cntDown - 1

def set_up_walls():
    for y in range(len(maze_map[0])):
        for x in range(len(maze_map[0][y])):
            if maze_map[0][y][x]=="1":
                Wall((x*60,y*60),0)
    for t in range(20):
        Wall((t*60,-60),0)
        Wall((t*60,900),0)
    for w in range(15):
        Wall((-60,w*60),0)
        Wall((1200,w*60),0)

def drawBackground(screen,background):
    for b in range(1200//128):
        for c in range(900//128 + 3):
            screen.blit(background,(c*128,b*128))

def main():
    """run the game"""
    # initialization and setup
    
    pygame.init()
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    random.seed()
    screen = pygame.display.set_mode((1200, 900))
    pygame.display.set_caption('PyTank')

    background = load_image('sand.png',128,128)

    set_up_walls()
    
    spawns = maze_map[1]
    print(spawns)
    bluePos = random.randint(0,len(spawns)-1)
    greenPos = random.randint(0,len(spawns)-1)
    while greenPos == bluePos:
        greenPos = random.randint(0,len(spawns)-1)
    blueSpawn = spawns[bluePos]
    greenSpawn = spawns[greenPos]

    greenT = Tank('green',greenSpawn)
    blueT = Tank('blue',blueSpawn)
    greenT.set_enemy(blueT)
    blueT.set_enemy(greenT)
    
    blueDeathTimer = 60
    greenDeathTimer = 60

    blueKilled = False
    greenKilled = False

    cntDown = 0
    cntDownTimer = 60
    drawBackground(screen, background)

    all_sprites.draw(screen)
    cntDown = countdown(cntDown)

    # game loop
    while True:
        start_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        
        if cntDown >= 0:        # this should really be outside the game loop
            if cntDownTimer>0:
                cntDownTimer -= 1
            else:
                cntDownTimer = 60
                drawBackground(screen,background)
                all_sprites.draw(screen)
                cntDown = countdown(cntDown)
        else:                   # so this if else isn't always being eval'd
            if blueKilled:
                blueDeathTimer -= 1
            if greenKilled:
                greenDeathTimer -= 1

            #If death timers countdowns reach 0, respawn appropriate tank
            if blueDeathTimer<1:        # this is messy, need better corpse free way
                blueT.respawn()
                blueDeathTimer = 60
                blueKilled = False
            if greenDeathTimer < 1:
                greenT.respawn()
                greenDeathTimer = 60
                greenKilled = False
            gShot = pygame.sprite.spritecollideany(blueT, green_shots, collided = pygame.sprite.collide_circle)
            oShot = pygame.sprite.spritecollideany(greenT, blue_shots, collided = pygame.sprite.collide_circle)
            if gShot: 
                gShot.kill()
                if blueT.takeDamage():
                    blueKilled = True
            if oShot:
                oShot.kill()
                if greenT.takeDamage():
                    greenKilled = True
                
            # all_sprites.clear(screen, background)

            # Draw background
            drawBackground(screen, background)

            all_sprites.draw(screen)
            all_sprites.update()
        pygame.display.flip()
        frame_time = pygame.time.get_ticks() - start_time
        if frame_time < 25:
            pygame.time.delay(25-frame_time)


if __name__ == '__main__': main()
pygame.quit()


