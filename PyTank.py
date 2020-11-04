#Copyright (c) 2019 Andrew Groeneveldt and Scott Blenkhorne
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


# *********************** IMPORTANT SETUP INFORMATION *************************

# set this to True for tournament play, shoud be False for student copies
tournament = False
training = True

# for practice:
# student AI's must be in same folder as this PyTank.py and MUST have "control" in the filename, and be the only such file
# the enemy AI that the students practice against must be in this folder and MUST be named "enemy_AI.py"

# for tournament:
# each contestant should have an AI file ending in .py
# place these files in the folder "tank_AI" and NO OTHER FILES
# it does not matter what these files are named as long as they are unique

# the sub-folders titled "assets", "mapsRaw", and "sounds" must be included in this folder
# as well as the script titled "mapGen.py"

# ******************************************************************************


from math import atan2, degrees, pi
import pygame, os, random, mapGen, importlib, enemy_AI, threading
from pygame.locals import *

# these must be above dynamic loading code
random.seed()
num_players = 0     # do NOT change this initial value - EVER!!!!
control_files = []

def printOptions(options):
    for x in range(len(options)):
        print("{}) {}".format(x+1, options[x]))

# this code dynamically loads the control files
if tournament:
    controllers = [x[:-3] for x in os.listdir("tank_AI") if x.endswith("py")]
    while num_players < 2 or num_players > 4:       # in practice mode the student decides how many enemies (all use same AI)
        num_players = int(input("Please enter number of players (2-4):"))
    players = []
    while len(players) < num_players:
        printOptions(controllers)
        try:
            choice = int(input("Pick your next competitor: "))
            players.append(controllers.pop(choice-1))
        except:
            print("That's not a valid choice.")
    
    random.shuffle(players)
    for controller in players: control_files.append(importlib.import_module("tank_AI."+controller))
else:
    if training:
        valid=False
        while not valid:
            try:
                challenge = int(input("Which challenge do you want to face? (1-5): "))
                if challenge >5 or challenge<1:
                    raise Exception("Please enter a number between 1 and 5")
                valid = True
            except:
                valid = False
        num_players = 1
        control_files.append(importlib.import_module([x[:-3] for x in os.listdir() if "control" in x][0]))
        if challenge >2:
            control_files.append(importlib.import_module('enemy_AI'))
    else:
        while num_players < 2 or num_players > 4:       # in practice mode the student decides how many enemies (all use same AI)
            num_players = int(input("Please enter number of players (2-4):"))
        control_files.append(importlib.import_module([x[:-3] for x in os.listdir() if "control" in x][0]))
        for _ in range(num_players-1): control_files.append(enemy_AI)

# Global sprite groups and other globals
all_sprites = pygame.sprite.LayeredUpdates()
shots = [pygame.sprite.Group(),pygame.sprite.Group(),pygame.sprite.Group(),pygame.sprite.Group()]
enviro_sprites = pygame.sprite.Group()
objectives = pygame.sprite.Group()
tanks_sprites = pygame.sprite.Group()
tank_colours = ['blue','green','orange','red']
players = []

def intersect(p1,p2,p3,p4):
    """tests for intersection of two line segments, caution does not work well with parallel line
        takes: the endpoints of the line segments to test at pairs (x,y)
                segment 1 defined by p1 and p2, segment 2 by p3 and p4
        returns: a boolean value of if the lines intersect at any point
        notes: behaviour for parallel lines is incorrect but this does not impact this program
                as is explained in the notes accompanying the method calling this code"""
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

class Objective(pygame.sprite.Sprite):
    """Class to represent map objectives """
    def __init__(self, position):
        """Objective class constructor
            takes: the position of the objective (as a pair)
        """
        pygame.sprite.Sprite.__init__(self)
        all_sprites.add(self, layer = 0)
        objectives.add(self)
        image_file = 'objective.png'
        self.base_image = load_image(image_file,60,60)
        self.image = self.base_image
        self.rect = self.image.get_rect(topleft = (position[0], position[1]))

class Wall(pygame.sprite.Sprite):
    """Class to represent obstacles"""
    def __init__(self,position,perm = True):
        """ Wall class constructor
            takes: the position of the wall block (as a pair) and a boolean decribing if the wall can be destroyed in play
            assumes: stoneWall.png is in assets subfolder"""
        pygame.sprite.Sprite.__init__(self)
        all_sprites.add(self, layer = 0)
        enviro_sprites.add(self)
        self.image = load_image('stoneWall.png',60,60)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft = (position[0],position[1]))
        self.permanent = perm


class Player():
    """Class to represent a player in the game"""
    def __init__(self,number):
        """Player class constructor
            takes: a unique identifier for this player as an integer"""
        self.number = number
        self.alive = True
        self.respawn_timer = 0
        if tournament: self.lives = 2
        else: self.lives = 1
        self.kills = 0

    def die(self):
        """method called to record the death of a tank belonging to this player"""
        self.alive = False
        self.respawn_timer = 60
        self.lives -= 1

    def respawn(self,spawns):
        """method to instantiate a new tank for this player"""
        if self.lives == 0: return True
        self.respawn_timer -= 1
        if self.respawn_timer: return
        self.alive = True
        Tank(self.number,spawns[:])


class Shot(pygame.sprite.Sprite):
    """Class to represent and control projectiles"""
    def __init__(self, position, heading):
        """Shot class constructor
            takes: the starting position of the shot (as a pair) and a heading (as a vector) the shot will travel along
            assumes: bullet.png is in assets subfolder"""
        pygame.sprite.Sprite.__init__(self)
        self.base_image = load_image('bullet.png',15,15)
        self.image = self.base_image
        self.rect = self.image.get_rect(center=position)
        self.radius = 6
        self.heading = heading * 1
        self.image = rotate_ip(self, self.heading.angle_to(pygame.math.Vector2(0, -1)))
        self.rect.move_ip(self.heading)
    
    def update(self):
        """ update shot position and process collision with walls"""
        self.rect.move_ip(self.heading)
        wall_hit = pygame.sprite.spritecollideany(self, enviro_sprites)
        if wall_hit:
            if not wall_hit.permanent: wall_hit.kill()
            self.kill()

class Turret(pygame.sprite.Sprite):
    """Class to represent gun turrets associated with a tank"""
    def __init__(self,tank,colour,heading):
        """Turret class contructor
            takes: a tank object the turret belongs to, a colour (as a string) and an intial aim heading (as a vector)
            assumes: the appropriately named image file is in the assets subfolder"""
        pygame.sprite.Sprite.__init__(self)
        all_sprites.add(self, layer = 1)
        image_file = colour + 'Turret.png'
        self.base_image = load_image(image_file,40,40)
        self.image = self.base_image
        self.rect = self.image.get_rect(center=tank.rect.center)
        self.heading = heading * 2

class Tank(pygame.sprite.Sprite):
    """Class to represent and control tanks, this is a large and complex class"""
    def __init__(self,number,spawns):
        """Tank class constructor
            takes: an integer ID of the player owning this tank and a list of pairs representing possible spawn points
            assumes: the precense of support files in subdirectories"""
        pygame.sprite.Sprite.__init__(self)
        self.colour = tank_colours[number]
        self.player_number = number
        self.exit = False
        image_file = self.colour + 'Tank.png'
        self.tankFireSound = pygame.mixer.Sound("sounds/tankFire.wav")
        self.tankExplosion = pygame.mixer.Sound("sounds/tankExplosion.wav")
        self.base_image = load_image(image_file,50,50)
        self.image = self.base_image
        self.rect = self.image.get_rect(topleft=spawns.pop(random.randint(0,len(spawns)-1)))
        while pygame.sprite.spritecollideany(self, tanks_sprites, collided = pygame.sprite.collide_rect):
            self.rect = self.image.get_rect(topleft=spawns.pop(random.randint(0,len(spawns)-1)))
        tanks_sprites.add(self)
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
        self.nSensor = pygame.math.Vector2(0,-60)
        self.sSensor = pygame.math.Vector2(0,60)
        self.wSensor = pygame.math.Vector2(-60,0)
        self.eSensor = pygame.math.Vector2(60,0)
        self.flSensor = pygame.math.Vector2(-45,-45)
        self.frSensor = pygame.math.Vector2(45,-45)
        self.blSensor = pygame.math.Vector2(-45,45)
        self.brSensor = pygame.math.Vector2(45,45)
        self.fSensor = pygame.math.Vector2(0,-43)
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
    
    # ********** methods intended to be called by player AI's ***********
    
    def turn_right_for(self,degs):
        """continue to turn right at current rate of turn until specified degrees are reached"""
        if self.turn_target == 0: self.turn_target = degs
    
    def turn_left_for(self,degs):
        """continue to turn left at current rate of turn until specified degrees are reached"""
        if self.turn_target == 0: self.turn_target = -degs
    
    def turn_to(self,bearing):
        """continue to turn at present rate of turn until heading is specified bearing"""
        if self.turn_target != 0: return
        self.turn_target = ((180 + bearing - self.my_heading()) % 360) - 180
    
    def turret_right_for(self,degs):
        """continue to turn turret right at current rate of turn until specified degrees are reached"""
        if self.turret_aim_target == 0: self.turret_aim_target = degs
    
    def turret_left_for(self,degs):
        """continue to turn turret left at current rate of turn until specified degrees are reached"""
        if self.turret_aim_target == 0: self.turret_aim_target = -degs
    
    def turret_to(self,aim):
        """continue to turn turret at present rate of turn until heading is specified aim"""
        if self.turret_aim_target != 0: return
        self.turret_aim_target = ((180 + aim - self.turret_direction()) % 360) - 180
    
    def set_enemy_lvl(self,lvl):
        """set value for practice AI difficulty (as integer
            assumes: enemy AI has implemented variable difficulty"""
        for tank in tanks_sprites.sprites():
            if self.player_number == tank.player_number: continue
            tank.AIlevel = lvl

    def set_Name(self, newName):
        """sets the displayed name on the tank sprite in game"""
        self.name = newName
    
    def damaged(self):
        """returns a boolean indicating if the tank has taken damage"""
        return self.__health != 2

    def my_position(self):
        """returnd a pair decribing the location of the calling tank"""
        return self.rect.center

    def my_AI_level(self):
        """returns the cuurent specified AI difficulty level as an integer"""
        return self.AIlevel

    def my_heading(self):
        """returns the cuurent heading of the tank as an integer number of degrees"""
        return (360-((round(int(self.heading.angle_to(pygame.math.Vector2(0,-1)))<<1,-1))>>1))%360
    
    def turret_direction(self):
        """returns the cuurent aim of the turret as an integer number of degrees"""
        return (360-((round(int(self.turret.heading.angle_to(pygame.math.Vector2(0,-1)))<<1,-1))>>1))%360

    def weapon_cooldown(self):
        """returns an integer indicating the remaining frames before the tank can fire again"""
        return self.__cooldown

    def checkSensors(self):
        """returns a dictionary with directional keys and boolean values of if the tank senses a wall or other object
            dictionary has 12 keys, 8 directions relative to tank heading and 4 fixed on grid directions"""
        sensors = {'n':False,'s':False,'w':False,'e':False,'fl':False,'f':False,'fr':False,'r':False,'br':False,'b':False,'bl':False,'l':False}
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
            if object.rect.collidepoint(self.nSensor + self.rect.center): sensors['n'] = True
            if object.rect.collidepoint(self.sSensor + self.rect.center): sensors['s'] = True
            if object.rect.collidepoint(self.wSensor + self.rect.center): sensors['w'] = True
            if object.rect.collidepoint(self.eSensor + self.rect.center): sensors['e'] = True
        return sensors

    def enemy_tanks(self):
        """returns a list of positions of visible enemy tanks (as pairs), closest in index 0 (rest NOT in order!!)"""
        visible = []
        closest = 2250000
        for tank in tanks_sprites.sprites():
            if self.player_number == tank.player_number: continue
            vis = True
            minx = min(self.rect.topleft[0],tank.rect.topleft[0])
            miny = min(self.rect.topleft[1],tank.rect.topleft[1])
            maxx = max(self.rect.bottomright[0],tank.rect.bottomright[0])
            maxy = max(self.rect.bottomright[1],tank.rect.bottomright[1])
            # calls intersection code to see if line from tank to tank crosses segments making an X in wall blocks
            # thus even if one segment is parallel the other won't be
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
        """attempts to move tank forward at current speed along current heading
            returns True if movement completed and False if not"""
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
        """attempts to move tank backwards at current speed along current heading
            returns True if movement completed and False if not"""
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
        """turn tank left at current rate of turn"""
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
        """turn tank right at current rate of turn"""
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
        """turn turret left at current rate of turn"""
        if self.rotated: return
        self.rotated = True
        self.turret.heading.rotate_ip(-self.rotate_rate)
        self.turret.image = rotate_ip(self.turret, self.turret.heading.angle_to(pygame.math.Vector2(0, -1)))
    
    def rotate_right(self):
        """turn turret right at current rate of turn"""
        if self.rotated: return
        self.rotated = True
        self.turret.heading.rotate_ip(self.rotate_rate)
        self.turret.image = rotate_ip(self.turret, self.turret.heading.angle_to(pygame.math.Vector2(0, -1)))

    def fire(self):
        """attempts to fire the weapon if cooldown completed"""
        if self.fired: return
        if self.__cooldown != 0: return
        self.fired = True
        shot = Shot(self.rect.center, self.turret.heading)
        self.shot_group.add(shot)
        all_sprites.add(shot)
        self.__cooldown = 50
        pygame.mixer.Sound.play(self.tankFireSound)
    
    # *********** end of player callable methods *****************************
    
    def take_damage(self):
        """called if collision detected between tank and enemy shot
            returns True if this is a killing shot and False if it is not"""
        self.__health -= 1
        pygame.mixer.Sound.play(self.tankExplosion)
        if self.__health == 0: return True
        self.heading = self.heading * 0.7
        self.rotate_rate = 2
        self.turn_rate = 3
        return False
    
    def kill(self):
        """wrapper method to kill both the tank and its turret"""
        self.turret.kill()
        pygame.sprite.Sprite.kill(self)
    
    def drawHealthBar(self):
        """display a graphical representation of the damage level of the tank in game"""
        healthRect = pygame.Rect(self.rect.center[0]-40,self.rect.center[1]-50,80*self.__health/2,10)
        healthOutline = pygame.Rect(self.rect.center[0]-40,self.rect.center[1]-50,80,10)
        if self.__health == 2:
            rectCol = (0,255,0)
        else:
            rectCol = (255, 160, 0)
        pygame.draw.rect(pygame.display.get_surface(),rectCol,healthRect,0)
        pygame.draw.rect(pygame.display.get_surface(),(0,0,0),healthOutline,1)
            
    def drawTankName(self):
        """display a name label on the tank in game, name is set by player AI"""
        nameTxt = pygame.font.Font('freesansbold.ttf',15)
        text = str(players[self.player_number].lives)+' '+self.name+' '+str(players[self.player_number].kills)
        textSurf, textRect = text_objects(text, nameTxt, (0,0,0))
        textRect.center = (self.rect.center[0], self.rect.center[1]-60)
        pygame.display.get_surface().blit(textSurf, textRect)

    def update(self):
        """per frame update of tank state"""
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
                    players[self.player_number].die()
                    players[shots.index(shot_group)].kills += 1
                    self.kill()
                    break
        if pygame.sprite.spritecollideany(self, objectives):
            self.exit = True

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

        # move turret
        self.turret.rect.center = self.rect.center
        
        # clear action flags
        self.moved = False
        self.turned = False
        self.rotated = False
        self.fired = False


def text_objects(text, font, txtColour):
    """helper function to display text in game"""
    textSurface = font.render(text, True, txtColour)
    return textSurface, textSurface.get_rect()

def message_display(text, txtColour, fntSize):
    """function to display text in game"""
    largeText = pygame.font.Font('freesansbold.ttf',fntSize)
    TextSurf, TextRect = text_objects(str(text), largeText, txtColour)
    TextRect.center = (600,450)
    pygame.display.get_surface().blit(TextSurf, TextRect)
    pygame.display.update()

def set_up_level(maze_maps):
    """function to set up game arena
        takes: a list of lists, element one is a list of wall locations, element two a list of tank spawn locations
        returns: the list of spawn locations for use in creating tanks"""
    if len(maze_maps)>1:
        maze_map = maze_maps[random.randint(0,len(maze_maps)-1)]
    else:
        maze_map = maze_maps[0]
    for y in range(len(maze_map[0])):
        for x in range(len(maze_map[0][y])):
            if maze_map[0][y][x]=="1":
                Wall((x*60,y*60),False)
            elif maze_map[0][y][x]=="2":
                Objective((x*60, y*60))
            elif maze_map[0][y][x] == "3":
                players.append(Player(1))
                print(maze_map[0][y][x])
                Tank(1,[(x*60, y*60)])
    for t in range(20):
        Wall((t*60,-60))
        Wall((t*60,900))
    for w in range(15):
        Wall((-60,w*60))
        Wall((1200,w*60))
    return maze_map[1]

def drawBackground(screen,background):
    """draw the background tile onto the screen"""
    for b in range(1200//128):
        for c in range(900//128 + 3):
            screen.blit(background,(c*128,b*128))

def countdown(count, screen, background):
    """display a countdown on screen before game begins"""
    while count+1:
        start_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        drawBackground(screen,background)
        tanks_sprites.draw(screen)
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
    screen = pygame.display.set_mode((1200, 900), pygame.SCALED)
    pygame.display.set_caption('PyTank')
    background = load_image('sand.png',128,128)
    if training:
        maze_maps = mapGen.getMap(challenge)
    else:
        maze_maps = mapGen.getMaps()
    
    while True:
        # initial tank set-up
        players.clear()
        all_sprites.empty()
        enviro_sprites.empty()
        tanks_sprites.empty()

        spawns = set_up_level(maze_maps)
        for i in range(num_players):
            players.append(Player(i))
            Tank(i,spawns[:])

        # onscreen countdown to game start
        if tournament: countdown(0, screen, background)
        # game loop
        while True:
            start_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

            if num_players > 1:
                out_of_play = 0
                for player in players:
                    if not player.alive:
                        if player.respawn(spawns): out_of_play += 1
                if out_of_play >= num_players - 1: break
            else:
                if tanks_sprites.sprites()[0].exit:
                    exitWin = True
                    break

            drawBackground(screen,background)
            ts = []
            for tank in tanks_sprites.sprites():
                t = threading.Thread(target = tank.update)
                ts.append(t)
                t.start()
            for t in ts: t.join()
            all_sprites.update()
            tanks_sprites.draw(screen)
            all_sprites.draw(screen)
            pygame.display.flip()
            
            frame_time = pygame.time.get_ticks() - start_time
            if frame_time < 25:
                pygame.time.delay(25-frame_time)

        if tournament:
            win_string = tanks_sprites.sprites()[0].name + " is the winner!!"
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        return
                drawBackground(screen,background)
                # all_sprites.draw(screen)
                message_display(win_string,(0,0,0),75)
        else:
            win_string = "You beat the Challenge!"
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        return
                drawBackground(screen,background)
                # all_sprites.draw(screen)
                message_display(win_string,(0,0,0),75)


if __name__ == '__main__': main()
pygame.quit()


