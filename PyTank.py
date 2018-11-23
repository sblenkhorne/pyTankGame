#! /usr/bin/env python3

# PyTank - By Andrew Groeneveldt and Scott Blenkhorne
# November 2018


import pygame, os, random, green_control, orange_control
from pygame.locals import *


all_sprites = pygame.sprite.LayeredUpdates()
green_shots = pygame.sprite.Group()
orange_shots = pygame.sprite.Group()
enviro_sprites = pygame.sprite.Group()
maze_map = []


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

    def __init__(self,position,orientation):
        pygame.sprite.Sprite.__init__(self)
        all_sprites.add(self, layer = 0)
        enviro_sprites.add(self)
        self.image = load_image('wall.png',200,20)
        self.image = pygame.transform.rotate(self.image,orientation)
        self.mask = pygame.mask.from_surface(self.image)
        if orientation == 0: self.rect = self.image.get_rect(topleft = (position[0],position[1]-10))
        if orientation == 90: self.rect = self.image.get_rect(topleft = (position[0]-10,position[1]))
        if orientation == 180: self.rect = self.image.get_rect(bottomright = (position[0],position[1]+10))
        if orientation == 270: self.rect = self.image.get_rect(bottomright = (position[0]+10,position[1]))



class Shot(pygame.sprite.Sprite):
    """Class to represent and control projectiles"""
    
    def __init__(self, position, heading):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = load_image('bullet.png',15,15)
        self.image = self.base_image
        self.area = pygame.display.get_surface().get_rect()
        self.rect = self.image.get_rect(center=position)
        self.radius = 6
        self.heading = heading
        self.image = rotate_ip(self, self.heading.angle_to(pygame.math.Vector2(0, -1)))
        self.rect.move_ip(self.heading)
    
    def update(self):
        """ update shot position """
        self.rect.move_ip(self.heading)
        if pygame.sprite.spritecollideany(self, enviro_sprites) or not self.area.contains(self.rect): self.kill()


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
        if colour == 'green': self.image = rotate_ip(self, self.heading.angle_to(pygame.math.Vector2(0, -1)))


class Tank(pygame.sprite.Sprite):
    """Class to represent and control tanks"""
    
    def __init__(self,colour = 'green',position = (600,400)):
        pygame.sprite.Sprite.__init__(self)
        if colour != 'green' and colour != 'orange': colour = 'green'
        all_sprites.add(self, layer = 0)
        image_file = colour + 'Tank.png'
        self.base_image = load_image(image_file,75,75)
        self.image = self.base_image
        self.rect = self.image.get_rect(center=position)
        if colour == 'green':
            self.control = green_control
            self.shot_group = green_shots
            self.heading = pygame.math.Vector2(0, 10)
            self.image = rotate_ip(self, self.heading.angle_to(pygame.math.Vector2(0, -1)))
        else:
            self.control = orange_control
            self.shot_group = orange_shots
            self.heading = pygame.math.Vector2(0, -10)
        self.mask = pygame.mask.from_surface(self.image)
        self.radius = 35
        self.turret = Turret(self,colour,self.heading)
        self.cooldown = 0
        self.moved = False
        self.turned = False
        self.rotated = False
        self.fired = False
        
    def set_enemy(self, tank):
        self.enemy = tank
    
    def kill(self):
        self.turret.kill()
        pygame.sprite.Sprite.kill(self)

    def get_walls(self):
        if self.rect.center[0] < 0 or self.rect.center[0] >= 1200:
            return maze_map[24]
        if self.rect.center[1] < 0 or self.rect.center[1] >= 800:
            return maze_map[25]
        return maze_map[6 * (self.rect.center[1]//200) + self.rect.center[0]//200]

    def my_position(self):
        return self.rect.center
    
    def enemy_position(self):
        return self.enemy.rect.center
    
    def my_heading(self):
        return (360-((round(int(self.heading.angle_to(pygame.math.Vector2(0,-1)))<<1,-1))>>1))%360
    
    def turret_direction(self):
        return (360-((round(int(self.turret.heading.angle_to(pygame.math.Vector2(0,-1)))<<1,-1))>>1))%360

    def clear_shot(self):
        return False
    
    def forward(self):
        if self.moved: return False
        self.moved = True
        self.rect.move_ip(self.heading * 0.8)
        if pygame.sprite.collide_mask(self, self.enemy):
            self.rect.move_ip(-self.heading * 0.8)
            return False
        if pygame.sprite.spritecollideany(self, enviro_sprites, collided = pygame.sprite.collide_mask):
            self.rect.move_ip(-self.heading * 0.8)
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
        self.turret.heading.rotate_ip(-5)
        self.turret.image = rotate_ip(self.turret, self.turret.heading.angle_to(pygame.math.Vector2(0, -1)))
        
    def rotate_right(self):
        if self.rotated: return
        self.rotated = True
        self.turret.heading.rotate_ip(5)
        self.turret.image = rotate_ip(self.turret, self.turret.heading.angle_to(pygame.math.Vector2(0, -1)))

    def fire(self):
        if self.fired: return
        self.fired = True
        shot = Shot(self.rect.center, self.turret.heading)
        self.shot_group.add(shot)
        all_sprites.add(shot)
        self.cooldown = 15
    
    def update(self):
        """ update tank heading and position """
        
        if self.cooldown > 0:
            self.cooldown -= 1

        # get control input
        self.control.action(self)

        # wrap screen
        if self.rect.x + self.rect.width < 0:
            self.rect.x = 1200
        if self.rect.y + self.rect.height < 0:
            self.rect.y = 800
        if self.rect.x > 1200:
            self.rect.x = -self.rect.width
        if self.rect.y > 800:
            self.rect.y = -self.rect.height

        # move turret with tank
        self.turret.rect.center = self.rect.center

        # clear action flags
        self.moved = False
        self.turned = False
        self.rotated = False
        self.fired = False



def set_up_walls():
    for _ in range(24): maze_map.append({'n':0,'s':0,'e':0,'w':0})
    maze_map.append({'n':1,'s':1,'e':0,'w':0})
    maze_map.append({'n':0,'s':0,'e':1,'w':1})
    Wall((0,10),0)
    maze_map[0]['n'] = 1
    Wall((200,10),0)
    maze_map[1]['n'] = 1
    Wall((400,10),0)
    maze_map[2]['n'] = 1
    Wall((800,10),0)
    maze_map[4]['n'] = 1
    Wall((1000,10),0)
    maze_map[5]['n'] = 1
    Wall((0,790),0)
    maze_map[18]['s'] = 1
    Wall((200,790),0)
    maze_map[19]['s'] = 1
    Wall((400,790),0)
    maze_map[20]['s'] = 1
    Wall((800,790),0)
    maze_map[22]['s'] = 1
    Wall((1000,790),0)
    maze_map[23]['s'] = 1
    Wall((10,0),90)
    maze_map[0]['w'] = 1
    Wall((10,400),90)
    maze_map[12]['w'] = 1
    Wall((10,600),90)
    maze_map[18]['w'] = 1
    Wall((1190,0),90)
    maze_map[5]['e'] = 1
    Wall((1190,400),90)
    maze_map[17]['e'] = 1
    Wall((1190,600),90)
    maze_map[23]['e'] = 1
    point = [0,1,2,3,4,6,7,8,9,10,12,13,14,15,16]
    index = 0
    for y in range(200,700,200):
        for x in range(200,1100,200):
            r = random.choice([0,90,180,270])
            if r == 0:
                maze_map[point[index]+1]['s'] = 1
                maze_map[point[index]+7]['n'] = 1
            elif r == 90:
                maze_map[point[index]+6]['e'] = 1
                maze_map[point[index]+7]['w'] = 1
            elif r == 180:
                maze_map[point[index]]['s'] = 1
                maze_map[point[index]+6]['n'] = 1
            elif r == 270:
                maze_map[point[index]]['e'] = 1
                maze_map[point[index]+1]['w'] = 1
            Wall((x,y),r)
            index += 1

def main():
    """run the game"""
    # initialization and setup
    pygame.init()
    random.seed()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption('PyTank')
    
    background = load_image('arena.png')
    screen.blit(background, (0, 0))

    set_up_walls()
    greenT = Tank('green',(100,100))
    orangeT = Tank('orange',(1100,700))
    greenT.set_enemy(orangeT)
    orangeT.set_enemy(greenT)
    
    # game loop
    while True:
        start_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        all_sprites.update()
        if pygame.sprite.spritecollideany(greenT, orange_shots, collided = pygame.sprite.collide_circle): greenT.kill()
        if pygame.sprite.spritecollideany(orangeT, green_shots, collided = pygame.sprite.collide_circle): orangeT.kill()

        
        all_sprites.clear(screen, background)
        all_sprites.draw(screen)
        pygame.display.flip()
        frame_time = pygame.time.get_ticks() - start_time
        if frame_time < 25:
            pygame.time.delay(25-frame_time)


if __name__ == '__main__': main()
pygame.quit()


