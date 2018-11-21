#! /usr/bin/env python3

# PyTank - By Andrew Groeneveldt and Scott Blenkhorne
# November 2018


import pygame, os, random, green_control, orange_control
from pygame.locals import *


all_sprites = pygame.sprite.LayeredUpdates()
green_shots = pygame.sprite.Group()
orange_shots = pygame.sprite.Group()
enviro_sprites = pygame.sprite.Group()


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
        self.rect = self.image.get_rect(topleft=position)


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
        self.velocity = heading
        self.rect.move_ip(self.velocity)
    
    def update(self):
        """ update shot position """
        self.rect.move_ip(self.velocity)
        if pygame.sprite.spritecollideany(self, enviro_sprites) or not self.area.contains(self.rect): self.kill()


class Turret(pygame.sprite.Sprite):
    """Class to represent gun turrets"""

    def __init__(self,tank,colour):
        pygame.sprite.Sprite.__init__(self)
        all_sprites.add(self, layer = 1)
        image_file = colour + 'Turret.png'
        self.base_image = load_image(image_file,50,50)
        self.image = self.base_image
        self.rect = self.image.get_rect(center=tank.rect.center)
        self.heading = pygame.math.Vector2(0, -20)


class Tank(pygame.sprite.Sprite):
    """Class to represent and control tanks"""
    
    def __init__(self,colour = 'green',position = (600,400)):
        pygame.sprite.Sprite.__init__(self)
        if colour != 'green' and colour != 'orange': colour = 'green'
        all_sprites.add(self, layer = 0)
        if colour == 'green':
            self.control = green_control
            self.shot_group = green_shots
        else:
            self.control = orange_control
            self.shot_group = orange_shots
        image_file = colour + 'Tank.png'
        self.base_image = load_image(image_file,75,75)
        self.image = self.base_image
        self.mask = pygame.mask.from_surface(self.image)
        self.area = pygame.display.get_surface().get_rect()
        self.rect = self.image.get_rect(center=position)
        self.radius = 35
        self.velocity = pygame.math.Vector2()
        self.heading = pygame.math.Vector2(0, -10)
        self.turret = Turret(self,colour)
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
    
    def forward(self):
        if self.moved: return False
        self.moved = True
        self.rect.move_ip(self.heading * 0.75)
        if pygame.sprite.collide_mask(self, self.enemy):
            self.rect.move_ip(-self.heading * 0.75)
            return False
        if pygame.sprite.spritecollideany(self, enviro_sprites, collided = pygame.sprite.collide_mask):
            self.rect.move_ip(-self.heading * 0.75)
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
            self.rect.x = self.area.width
        if self.rect.y + self.rect.height < 0:
            self.rect.y = self.area.height
        if self.rect.x > self.area.width:
            self.rect.x = -self.rect.width
        if self.rect.y > self.area.height:
            self.rect.y = -self.rect.height

        # move turret with tank
        self.turret.rect.center = self.rect.center

        # clear action flags
        self.moved = False
        self.turned = False
        self.rotated = False
        self.fired = False



def set_up_walls():
    Wall((0,0),0)
    Wall((200,0),0)
    Wall((400,0),0)
    Wall((800,0),0)
    Wall((1000,0),0)
    Wall((0,780),0)
    Wall((200,780),0)
    Wall((400,780),0)
    Wall((800,780),0)
    Wall((1000,780),0)
    Wall((0,0),90)
    Wall((0,400),90)
    Wall((0,600),90)
    Wall((1180,0),90)
    Wall((1180,400),90)
    Wall((1180,600),90)
    for y in range(190,700,200):
        for x in range(190,1100,200):
            r = random.choice([0,90,180,270])
            Wall((x,y),r)

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


