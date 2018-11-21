#! /usr/bin/env python3

# PyTank - By Andrew Groeneveldt and Scott Blenkhorne
# November 2018


import pygame, os, random, green_control, orange_control
from pygame.locals import *


all_sprites = pygame.sprite.LayeredUpdates()
green_shots = pygame.sprite.Group()
green_tanks = pygame.sprite.Group()
orange_shots = pygame.sprite.Group()
orange_tanks = pygame.sprite.Group()


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



class Shot(pygame.sprite.Sprite):
    """Class to represent and control projectiles"""
    
    def __init__(self, position, heading):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = load_image('bullet.png',15,15)
        self.image = self.base_image
        self.area = pygame.display.get_surface().get_rect()
        self.rect = self.image.get_rect(center=position)
        self.heading = heading
        self.image = rotate_ip(self, self.heading.angle_to(pygame.math.Vector2(0, -5)))
        self.velocity = heading*2.5
        self.rect.move_ip(self.velocity)
    
    def update(self):
        """ update shot position """
        self.rect.move_ip(self.velocity)
        if not self.area.contains(self.rect):
            self.kill()


class Turret(pygame.sprite.Sprite):
    """Class to represent gun turrets"""

    def __init__(self,tank,colour):
        pygame.sprite.Sprite.__init__(self)
        all_sprites.add(self, layer = 1)
        if colour == 'green': green_tanks.add(self)
        else: orange_tanks.add(self)
        image_file = colour + 'Turret.png'
        self.base_image = load_image(image_file,50,50)
        self.image = self.base_image
        self.rect = self.image.get_rect(center=tank.rect.center)
        self.heading = pygame.math.Vector2(0, -5)


class Tank(pygame.sprite.Sprite):
    """Class to represent and control tanks"""
    
    def __init__(self,colour = 'green',position = (600,400)):
        pygame.sprite.Sprite.__init__(self)
        if colour != 'green' and colour != 'orange': colour = 'green'
        all_sprites.add(self, layer = 0)
        if colour == 'green':
            green_tanks.add(self)
            self.control = green_control
            self.shot_group = green_shots
        else:
            orange_tanks.add(self)
            self.control = orange_control
            self.shot_group = orange_shots
        image_file = colour + 'Tank.png'
        self.base_image = load_image(image_file,75,75)
        self.image = self.base_image
        self.area = pygame.display.get_surface().get_rect()
        self.rect = self.image.get_rect(center=position)
        self.radius = 35
        self.velocity = pygame.math.Vector2()
        self.heading = pygame.math.Vector2(0, -5)
        self.turret = Turret(self,colour)
        self.cooldown = 0
        self.moved = False
        self.turned = False
        self.rotated = False
        self.fired = False
    
    def kill(self):
        self.turret.kill()
        pygame.sprite.Sprite.kill(self)
    
    def forward(self):
        if self.moved: return
        self.moved = True
        self.rect.move_ip(self.heading)
        if pygame.sprite.groupcollide(green_tanks, orange_tanks, False, False, collided = pygame.sprite.collide_circle):
            self.rect.move_ip(self.heading*-2.5)
    
    def turn_left(self):
        if self.turned: return
        self.turned = True
        self.heading.rotate_ip(-5)
        self.image = rotate_ip(self, self.heading.angle_to(pygame.math.Vector2(0, -5)))
    
    def turn_right(self):
        if self.turned: return
        self.turned = True
        self.heading.rotate_ip(5)
        self.image = rotate_ip(self, self.heading.angle_to(pygame.math.Vector2(0, -5)))
    
    def rotate_left(self):
        if self.rotated: return
        self.rotated = True
        self.turret.heading.rotate_ip(-5)
        self.turret.image = rotate_ip(self.turret, self.turret.heading.angle_to(pygame.math.Vector2(0, -5)))
        
    def rotate_right(self):
        if self.rotated: return
        self.rotated = True
        self.turret.heading.rotate_ip(5)
        self.turret.image = rotate_ip(self.turret, self.turret.heading.angle_to(pygame.math.Vector2(0, -5)))

    def fire(self):
        if self.fired: return
        self.fired = True
        shot = Shot(self.rect.center, self.turret.heading)
        self.shot_group.add(shot)
        all_sprites.add(shot)
        self.cooldown = 5
    
    def update(self):
        """ update tank heading, speed, and position """
        
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



def main():
    """run the game"""
    # initialization and setup
    pygame.init()
    random.seed()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption('PyTank')
    
    background = load_image('arena.png')
    screen.blit(background, (0, 0))
    
    Tank('green',(100,100))
    Tank('orange',(1100,700))
    
    # game loop
    while True:
        start_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        all_sprites.update()
        pygame.sprite.groupcollide(green_shots, orange_tanks, True, True, collided = pygame.sprite.collide_circle)
        pygame.sprite.groupcollide(orange_shots, green_tanks, True, True, collided = pygame.sprite.collide_circle)

        
        all_sprites.clear(screen, background)
        all_sprites.draw(screen)
        pygame.display.flip()
        frame_time = pygame.time.get_ticks() - start_time
        if frame_time < 15:
            pygame.time.delay(15-frame_time)


if __name__ == '__main__': main()
pygame.quit()


