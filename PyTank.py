#! /usr/bin/env python3

# PyTank - By Andrew Groeneveldt and Scott Blenkhorne
# November 2018


import pygame, os, random
from pygame.locals import *


all_sprites = pygame.sprite.Group()
shots = pygame.sprite.Group()
tanks = pygame.sprite.Group()


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
        self.image = rotate_ip(self, self.heading.angle_to(pygame.math.Vector2(0, -10)))
        self.velocity = heading * 2
        self.rect.move_ip(self.velocity)
    
    def update(self):
        """ update shot position """
        self.rect.move_ip(self.velocity)
        if not self.area.contains(self.rect):
            self.kill()


class Tank(pygame.sprite.Sprite):
    """Class to represent and control tanks"""
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = load_image('greenTank.png',75,75)
        self.image = self.base_image
        self.area = pygame.display.get_surface().get_rect()
        start_x = self.area.width/2
        start_y = self.area.height/2
        self.rect = self.image.get_rect(center=(start_x, start_y))
        self.velocity = pygame.math.Vector2()
        self.heading = pygame.math.Vector2(0, -10)
        self.cooldown = 0
    
    def update(self):
        """ update ship heading, speed, and position """
        key = pygame.key.get_pressed()
        
        if self.cooldown > 0:
            self.cooldown -= 1
        
        # read keyoard input
        if key[K_LEFT]:
            self.heading.rotate_ip(-5)
            self.image = rotate_ip(self, self.heading.angle_to(pygame.math.Vector2(0, -10)))
        if key[K_RIGHT]:
            self.heading.rotate_ip(5)
            self.image = rotate_ip(self, self.heading.angle_to(pygame.math.Vector2(0, -10)))
        if key[K_UP]:
            self.rect.move_ip(self.heading)
        if key[K_SPACE] and self.cooldown == 0:
            shot = Shot(self.rect.center, self.heading)
            shots.add(shot)
            all_sprites.add(shot)
            self.cooldown = 5
        
        # wrap screen
        if self.rect.x + self.rect.width < 0:
            self.rect.x = self.area.width
        if self.rect.y + self.rect.height < 0:
            self.rect.y = self.area.height
        if self.rect.x > self.area.width:
            self.rect.x = -self.rect.width
        if self.rect.y > self.area.height:
            self.rect.y = -self.rect.height


def main():
    """run the game"""
    # initialization and setup
    pygame.init()
    random.seed()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption('PyTank')
    
    background = load_image('arena.png')
    screen.blit(background, (0, 0))
    
    tank = Tank()
    tank.add(all_sprites)
    tank.add(tanks)
    
    # game loop
    while True:
        start_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        all_sprites.update()

        
        all_sprites.clear(screen, background)
        all_sprites.draw(screen)
        pygame.display.flip()
        frame_time = pygame.time.get_ticks() - start_time
        if frame_time < 25:
            pygame.time.delay(25-frame_time)


if __name__ == '__main__': main()
pygame.quit()


