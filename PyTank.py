#! /usr/bin/env python3

# PyTank - By Andrew Groeneveldt and Scott Blenkhorne
# November 2018


# *********************** IMPORTANT SETUP INFORMATION *************************

# set this to True for tournament play, shoud be False for student copies
tournament = True

# for practice:
# student AI's must be in same folder as this PyTank.py and MUST have "control" in the filename, and be the only such file
# the enemy AI that the students practice against must be in this folder and MUST be named "enemy_AI.py"

# for tournament:
# each contestant should have an AI file ending in .py
# there must be between 2 and 4 of these files in the folder "tank_AI" and NO OTHER FILES
# it does not matter what these files are named as long as they are unique

# ******************************************************************************



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
    while num_players < 2 or num_players > 4:       # in practice mode the student decides how many enemies (all use same AI)
        num_players = int(input("Please enter number of players (2-4):"))
    control_files.append(importlib.import_module([x[:-3] for x in os.listdir() if "control" in x][0]))
    for _ in range(num_players-1): control_files.append(enemy_AI)


# Global sprite groups and other globals
all_sprites = pygame.sprite.LayeredUpdates()
shots = [pygame.sprite.Group(),pygame.sprite.Group(),pygame.sprite.Group(),pygame.sprite.Group()]
enviro_sprites = pygame.sprite.Group()
tanks_sprites = pygame.sprite.Group()
tank_colours = ['blue','green','orange','red']
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
        self.alive = True
        self.respawn_timer = 0
        if tournament: self.lives = 2
        else: self.lives = 1
        self.kills = 0

    def die(self):
        self.alive = False
        self.respawn_timer = 60
        self.lives -= 1

    def respawn(self,spawns):
        if self.lives == 0: return True
        self.respawn_timer -= 1
        if self.respawn_timer: return
        self.alive = True
        Tank(self.number,spawns[:])


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
    def __init__(self,number,spawns):
        pygame.sprite.Sprite.__init__(self)
        self.colour = tank_colours[number]
        self.player_number = number
        image_file = self.colour + 'Tank.png'
        self.tankFireSound = pygame.mixer.Sound("sounds/tankFire.wav")
        self.tankExplosion = pygame.mixer.Sound("sounds/tankExplosion.wav")
        self.base_image = load_image(image_file,75,75)
        self.image = self.base_image
        self.rect = self.image.get_rect(center=spawns.pop(random.randint(0,len(spawns)-1)))
        while pygame.sprite.spritecollideany(self, tanks_sprites, collided = pygame.sprite.collide_rect):
            self.rect = self.image.get_rect(center=spawns.pop(random.randint(0,len(spawns)-1)))
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
                    players[self.player_number].die()
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

        # move turret
        self.turret.rect.center = self.rect.center
        
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
    screen = pygame.display.set_mode((1200, 900))
    pygame.display.set_caption('PyTank')
    background = load_image('sand.png',128,128)
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
        if tournament: countdown(3, screen, background)

        # game loop
        while True:
            start_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

            out_of_play = 0
            for player in players:
                if not player.alive:
                    if player.respawn(spawns): out_of_play += 1
            if out_of_play >= num_players - 1: break

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


if __name__ == '__main__': main()
pygame.quit()


