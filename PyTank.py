#! /usr/bin/env python3

# PyTank - By Andrew Groeneveldt and Scott Blenkhorne
# November 2018


import pygame, os, random, blue_control, green_control, orange_control, red_control, mapGen
from pygame.locals import *

# Global sprite groups and other globals
all_sprites = pygame.sprite.LayeredUpdates()
shots = [pygame.sprite.Group(),pygame.sprite.Group(),pygame.sprite.Group(),pygame.sprite.Group()]
enviro_sprites = pygame.sprite.Group()
tanks_sprites = pygame.sprite.Group()
tank_colours = ['blue','green','orange','red']
control_files = [blue_control,green_control,orange_control,red_control]
players = []

# helper function for visibility sensor
def intersect(p1,p2,p3,p4):
    x1,y1 = p1
    x2,y2 = p2
    x3,y3 = p3
    x4,y4 = p4
    a1 = (y1 - y2)
    b1 = (x2 - x1)
    c1 = -(x1 * y2 - x2 * y1)
    a2 = (y3 - y4)
    b2 = (x4 - x3)
    c2 = -(x3 * y4 - x4 * y3)
    d = a1 * b2 - b1 * a2
    dx = c1 * b2 - b1 * c2
    dy = a1 * c2 - c1 * a2
    if d == 0: return False
    if not (min(x3,x4) <= dx/d <= max(x3,x4)) or not (min(y3,y4) <= dy/d <= max(y3,y4)): return False
    return True

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


class Wall(pygame.sprite.Sprite):
    """Class to represent obstacles"""
    def __init__(self,position,perm = True):
        pygame.sprite.Sprite.__init__(self)
        all_sprites.add(self, layer = 0)
        enviro_sprites.add(self)
        self.image = load_image('stoneWall.png',60,60)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft = (position[0],position[1]))
        self.permanent = perm

class Player():
    def __init__(self,number):
        self.number = number
        self.colour = tank_colours[number]
        self.alive = True
        self.respawn_timer = 0
        self.lives = 3
        self.kills = 0

    def die(self,position):
        self.dead_at = position
        self.alive = False
        self.respawn_timer = 60
        self.lives -= 1

    def respawn(self):
        if self.lives == 0: return True
        self.respawn_timer -= 1
        if self.respawn_timer: return
        self.alive = True
        Tank(self.number,self.dead_at)

class wallSensor(pygame.sprite.Sprite):     # was this meant to subclass Sprite? 'cause it didn't
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

class Shot(pygame.sprite.Sprite):
    """Class to represent and control projectiles"""
    def __init__(self, position, heading):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = load_image('bullet.png',15,15)
        self.image = self.base_image
        self.rect = self.image.get_rect(center=position)
        self.radius = 6
        self.heading = heading * 1
        self.image = rotate_ip(self, self.heading.angle_to(pygame.math.Vector2(0, -1)))
        self.rect.move_ip(self.heading)
    
    def update(self):
        """ update shot position """
        self.rect.move_ip(self.heading)
        wall_hit = pygame.sprite.spritecollideany(self, enviro_sprites)
        if wall_hit:
            if not wall_hit.permanent: wall_hit.kill()
            self.kill()

class Turret(pygame.sprite.Sprite):
    """Class to represent gun turrets"""
    def __init__(self,tank,colour,heading):
        pygame.sprite.Sprite.__init__(self)
        all_sprites.add(self, layer = 1)
        image_file = colour + 'Turret.png'
        self.base_image = load_image(image_file,50,50)
        self.image = self.base_image
        self.rect = self.image.get_rect(center=tank.rect.center)
        self.heading = heading * 2

class Tank(pygame.sprite.Sprite):
    """Class to represent and control tanks"""
    def __init__(self,number,position):
        pygame.sprite.Sprite.__init__(self)
        self.colour = tank_colours[number]
        self.player_number = number
        all_sprites.add(self, layer = 0)
        tanks_sprites.add(self)
        image_file = self.colour + 'Tank.png'
        self.tankFireSound = pygame.mixer.Sound("sounds/tankFire.wav")
        self.tankExplosion = pygame.mixer.Sound("sounds/tankExplosion.wav")
        self.base_image = load_image(image_file,75,75)
        self.image = self.base_image
        self.rect = self.image.get_rect(center=position)
        self.speed = 10
        self.turn_rate = 5
        self.rotate_rate = 3
        self.control = control_files[number]
        self.shot_group = shots[number]
        self.name = self.colour + " tank"
        self.heading = pygame.math.Vector2(0, -self.speed)
        self.mask = pygame.mask.from_surface(self.image)
        self.radius = 35
        self.__health = 2
        self.turret = Turret(self,self.colour,self.heading)
        self.nSensor = wallSensor(self,'n')
        self.sSensor = wallSensor(self,'s')
        self.wSensor = wallSensor(self,'w')
        self.eSensor = wallSensor(self,'e')
        self.flSensor = pygame.math.Vector2(-45,-45)
        self.frSensor = pygame.math.Vector2(45,-45)
        self.blSensor = pygame.math.Vector2(-45,45)
        self.brSensor = pygame.math.Vector2(45,45)
        self.fSensor = pygame.math.Vector2(0,-50)
        self.rSensor = pygame.math.Vector2(50,0)
        self.bSensor = pygame.math.Vector2(0,50)
        self.lSensor = pygame.math.Vector2(-50,0)
        self.__cooldown = 0
        self.moved = False
        self.turned = False
        self.rotated = False
        self.fired = False
        self.AIlevel = 0
        self.turn_target = 0
        self.turret_aim_target = 0
    
    def turn_right_for(self,degs):
        if self.turn_target == 0: self.turn_target = degs
    
    def turn_left_for(self,degs):
        if self.turn_target == 0: self.turn_target = -degs
    
    def turn_to(self,bearing):
        if self.turn_target != 0: return
        self.turn_target = ((180 + bearing - self.my_heading()) % 360) - 180
    
    def turret_right_for(self,degs):
        if self.turret_aim_target == 0: self.turret_aim_target = degs
    
    def turret_left_for(self,degs):
        if self.turret_aim_target == 0: self.turret_aim_target = -degs
    
    def turret_to(self,aim):
        if self.turret_aim_target != 0: return
        self.turret_aim_target = ((180 + aim - self.turret_direction()) % 360) - 180
    
    def set_enemy_lvl(self,lvl):
        for tank in tanks_sprites.sprites():
            if self.player_number == tank.player_number: continue
            tank.AIlevel = lvl

    def set_Name(self, newName):
        self.name = newName
    
    def damaged(self):
        return self.__health != 2

    def my_position(self):
        return self.rect.center

    def my_AI_level(self):
        return self.AIlevel

    def my_heading(self):
        return (360-((round(int(self.heading.angle_to(pygame.math.Vector2(0,-1)))<<1,-1))>>1))%360
    
    def turret_direction(self):
        return (360-((round(int(self.turret.heading.angle_to(pygame.math.Vector2(0,-1)))<<1,-1))>>1))%360

    def weapon_cooldown(self):
        return self.__cooldown
    
    def checkSensors(self):
        sensors = {'n':False,'s':False,'w':False,'e':False}
        if pygame.sprite.spritecollideany(self.nSensor,enviro_sprites,collided=pygame.sprite.collide_circle): sensors['n']=True
        if pygame.sprite.spritecollideany(self.sSensor,enviro_sprites,collided=pygame.sprite.collide_circle): sensors['s']=True
        if pygame.sprite.spritecollideany(self.wSensor,enviro_sprites,collided=pygame.sprite.collide_circle): sensors['w']=True
        if pygame.sprite.spritecollideany(self.eSensor,enviro_sprites,collided=pygame.sprite.collide_circle): sensors['e']=True
        return sensors
    
    def pointSensors(self):
        sensors = {'fl':False,'f':False,'fr':False,'r':False,'br':False,'b':False,'bl':False,'l':False}
        for object in enviro_sprites.sprites() + tanks_sprites.sprites():
            if object == self: continue
            if object.rect.collidepoint(self.flSensor + self.rect.center): sensors['fl'] = True
            if object.rect.collidepoint(self.frSensor + self.rect.center): sensors['fr'] = True
            if object.rect.collidepoint(self.blSensor + self.rect.center): sensors['bl'] = True
            if object.rect.collidepoint(self.brSensor + self.rect.center): sensors['br'] = True
            if object.rect.collidepoint(self.fSensor + self.rect.center): sensors['f'] = True
            if object.rect.collidepoint(self.rSensor + self.rect.center): sensors['r'] = True
            if object.rect.collidepoint(self.bSensor + self.rect.center): sensors['b'] = True
            if object.rect.collidepoint(self.lSensor + self.rect.center): sensors['l'] = True
        return sensors

    def enemy_tanks(self):
        # returns a list of positions of visible enemy tanks, closest in index 0 (rest NOT in order!!)
        visible = []
        closest = 2250000
        for tank in tanks_sprites.sprites():
            if self.player_number == tank.player_number: continue
            vis = True
            minx = min(self.rect.topleft[0],tank.rect.topleft[0])
            miny = min(self.rect.topleft[1],tank.rect.topleft[1])
            maxx = max(self.rect.bottomright[0],tank.rect.bottomright[0])
            maxy = max(self.rect.bottomright[1],tank.rect.bottomright[1])
            for wall in enviro_sprites.sprites():
                if minx < wall.rect.center[0] < maxx and miny < wall.rect.center[1] < maxy:
                    if intersect(self.rect.center,tank.rect.center,wall.rect.topleft,wall.rect.bottomright):
                        vis = False
                        break
                    if intersect(self.rect.center,tank.rect.center,wall.rect.topright,wall.rect.bottomleft):
                        vis = False
                        break
            if vis:
                distance = (self.rect.center[0] - tank.rect.center[0])**2 + (self.rect.center[1] - tank.rect.center[1])**2
                if distance < closest:
                    closest = distance
                    visible.insert(0,tank.rect.center)
                else:
                    visible.append(tank.rect.center)
        return visible

    def forward(self):
        if self.moved: return False
        self.moved = True
        self.rect.move_ip(self.heading)
        for tank in tanks_sprites.sprites():
            if self.player_number == tank.player_number: continue
            if pygame.sprite.collide_mask(self, tank):
                self.rect.move_ip(-self.heading)
                return False
        if pygame.sprite.spritecollideany(self, enviro_sprites, collided = pygame.sprite.collide_mask):
            self.rect.move_ip(-self.heading)
            return False
        return True

    def reverse(self):
        if self.moved: return False
        self.moved = True
        self.rect.move_ip(-self.heading)
        for tank in tanks_sprites.sprites():
            if self.player_number == tank.player_number: continue
            if pygame.sprite.collide_mask(self, tank):
                self.rect.move_ip(self.heading)
                return False
        if pygame.sprite.spritecollideany(self, enviro_sprites, collided = pygame.sprite.collide_mask):
            self.rect.move_ip(self.heading)
            return False
        return True

    def turn_left(self):
        if self.turned: return
        self.turned = True
        self.heading.rotate_ip(-self.turn_rate)
        self.flSensor.rotate_ip(-self.turn_rate)
        self.fSensor.rotate_ip(-self.turn_rate)
        self.frSensor.rotate_ip(-self.turn_rate)
        self.rSensor.rotate_ip(-self.turn_rate)
        self.brSensor.rotate_ip(-self.turn_rate)
        self.bSensor.rotate_ip(-self.turn_rate)
        self.blSensor.rotate_ip(-self.turn_rate)
        self.lSensor.rotate_ip(-self.turn_rate)
        self.image = rotate_ip(self, self.heading.angle_to(pygame.math.Vector2(0, -1)))
        self.mask = pygame.mask.from_surface(self.image)
    
    def turn_right(self):
        if self.turned: return
        self.turned = True
        self.heading.rotate_ip(self.turn_rate)
        self.flSensor.rotate_ip(self.turn_rate)
        self.fSensor.rotate_ip(self.turn_rate)
        self.frSensor.rotate_ip(self.turn_rate)
        self.rSensor.rotate_ip(self.turn_rate)
        self.brSensor.rotate_ip(self.turn_rate)
        self.bSensor.rotate_ip(self.turn_rate)
        self.blSensor.rotate_ip(self.turn_rate)
        self.lSensor.rotate_ip(self.turn_rate)
        self.image = rotate_ip(self, self.heading.angle_to(pygame.math.Vector2(0, -1)))
        self.mask = pygame.mask.from_surface(self.image)
    
    def rotate_left(self):
        if self.rotated: return
        self.rotated = True
        self.turret.heading.rotate_ip(-self.rotate_rate)
        self.turret.image = rotate_ip(self.turret, self.turret.heading.angle_to(pygame.math.Vector2(0, -1)))
    
    def rotate_right(self):
        if self.rotated: return
        self.rotated = True
        self.turret.heading.rotate_ip(self.rotate_rate)
        self.turret.image = rotate_ip(self.turret, self.turret.heading.angle_to(pygame.math.Vector2(0, -1)))

    def fire(self):
        if self.fired: return
        if self.__cooldown != 0: return
        self.fired = True
        shot = Shot(self.rect.center, self.turret.heading)
        self.shot_group.add(shot)
        all_sprites.add(shot)
        self.__cooldown = 50
        pygame.mixer.Sound.play(self.tankFireSound)
    
    def take_damage(self):
        self.__health -= 1
        pygame.mixer.Sound.play(self.tankExplosion)
        if self.__health == 0: return True
        self.heading = self.heading * 0.7
        self.rotate_rate = 2
        self.turn_rate = 3
        return False
    
    def kill(self):
        self.turret.kill()
        pygame.sprite.Sprite.kill(self)
    
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
        text = str(players[self.player_number].lives)+' '+self.name+' '+str(players[self.player_number].kills)
        textSurf, textRect = text_objects(text, nameTxt, (0,0,0))
        textRect.center = (self.rect.center[0], self.rect.center[1]-60)
        pygame.display.get_surface().blit(textSurf, textRect)

    def update(self):
        """ tank update """
        self.drawTankName()
        
        # shot cooldown
        if self.__cooldown > 0: self.__cooldown -= 1
        
        # check if shot
        shot = None
        for shot_group in shots:
            if shot_group == self.shot_group: continue
            shot = pygame.sprite.spritecollideany(self, shot_group, collided = pygame.sprite.collide_circle)
            if shot:
                shot.kill()
                if self.take_damage():
                    players[self.player_number].die(self.rect.center)
                    players[shots.index(shot_group)].kills += 1
                    self.kill()
                    break
        self.drawHealthBar()
        
        # execute turn and turret aim to target bearing
        if self.turn_target < 0:
            self.turn_left()
            self.turn_target += self.turn_rate
            if -self.turn_target < self.turn_rate: self.turn_target = 0
        if self.turn_target > 0:
            self.turn_right()
            self.turn_target -= self.turn_rate
            if self.turn_target < self.turn_rate: self.turn_target = 0
        if self.turret_aim_target < 0:
            self.rotate_left()
            self.turret_aim_target += self.rotate_rate
            if -self.turret_aim_target < self.rotate_rate: self.turret_aim_target = 0
        if self.turret_aim_target > 0:
            self.rotate_right()
            self.turret_aim_target -= self.rotate_rate
            if self.turret_aim_target < self.rotate_rate: self.turret_aim_target = 0

        # control input
        self.control.action(self)

        # move turret & sensors
        self.turret.rect.center = self.rect.center
        self.nSensor.rect.center = (self.rect.center[0], self.rect.center[1] - 25)
        self.sSensor.rect.center = (self.rect.center[0], self.rect.center[1] + 25)
        self.wSensor.rect.center = (self.rect.center[0]-25, self.rect.center[1])
        self.eSensor.rect.center = (self.rect.center[0]+25, self.rect.center[1])
        
        # clear action flags
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

def set_up_level(maze_maps):
    maze_map = maze_maps[random.randint(0,len(maze_maps)-1)]
    for y in range(len(maze_map[0])):
        for x in range(len(maze_map[0][y])):
            if maze_map[0][y][x]=="1":
                Wall((x*60,y*60),False)
    for t in range(20):
        Wall((t*60,-60))
        Wall((t*60,900))
    for w in range(15):
        Wall((-60,w*60))
        Wall((1200,w*60))
    return maze_map[1]

def drawBackground(screen,background):
    for b in range(1200//128):
        for c in range(900//128 + 3):
            screen.blit(background,(c*128,b*128))

def countdown(count, screen, background):
    while count+1:
        start_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        drawBackground(screen,background)
        all_sprites.draw(screen)
        message_display(count,(0,0,0),200)
        count -= 1
        pygame.display.flip()
        timer = 20000000
        while timer: timer -= 1


def main():
    # initialization and setup
    pygame.init()
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    random.seed()
    screen = pygame.display.set_mode((1200, 900))
    pygame.display.set_caption('PyTank')
    background = load_image('sand.png',128,128)
    maze_maps = mapGen.getMaps()
    num_players = 4     # set to 2-4 or to 0 for user input
    while num_players < 2 or num_players > 4:
        num_players = int(input("Please enter number of players (2-4):"))
    
    # initial tank set-up
    spawns = set_up_level(maze_maps)
    for i in range(num_players):
        players.append(Player(i))
        spawn = spawns.pop(random.randint(0,len(spawns)-1))
        Tank(i,spawn)

    # onscreen countdown to game start
    countdown(3, screen, background)

    # game loop
    while True:
        start_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        out_of_play = 0
        for player in players:
            if not player.alive:
                if player.respawn(): out_of_play += 1
        if out_of_play >= num_players - 1: break

        drawBackground(screen,background)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        
        frame_time = pygame.time.get_ticks() - start_time
        if frame_time < 25:
            pygame.time.delay(25-frame_time)


if __name__ == '__main__': main()
pygame.quit()


