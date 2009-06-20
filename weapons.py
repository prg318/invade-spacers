# bullets.py
import os
import pygame
import invade
import globalvars
from pygame.locals import *

class Bullet(pygame.sprite.Sprite):
    """ A bullet object that flies from a enemy or player. """
    def __init__(self, pos, down=True):
        """ pos = initial position of the bullet (probably the cords of the
                  object shooting it)
            down = if down is true, bullet will fly down.  if false, it will 
                   fly up. """
        pygame.sprite.Sprite.__init__(self)

        self.using_image = False
        # check to see if there is a laser.bmp file.  If so load it, to allow modding.
        if os.access("img/laser.bmp", os.F_OK):
            self.image = pygame.image.load_basic("img/laser.bmp")
            self.image.set_colorkey((255, 255, 255))
            self.using_image = True
        else:
            self.image = pygame.Surface((3, 32))
            self.image.fill((255, 0, 0))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        if down:
            self._dir = 1
        else:
            self.rect.top -= self.image.get_height()
            self._dir = -1
        self._next_update = 0
        self._speed = 5
        
    def update(self, t):
        if t > self._next_update:
            # Move the bullet
            self.rect.top += self._speed * self._dir
            # If we've reached an edge of the screen, suicide. 
            if self.rect.top < 0 or self.rect.bottom > globalvars.HEIGHT or self.rect.left < 0 or self.rect.right >globalvars.WIDTH:
                self.kill()
                del self
                return
            
            self._next_update = t + 15 


def double_gun(rect):
    bullet = Bullet((rect.topleft), down=False)
    #bullet.image = pygame.image.load_basic("img/laser2.bmp") 
    #bullet.image.set_colorkey((255, 255, 255))
        
    bullet2 = Bullet((rect.topright), down=False)
    #bullet2.image = pygame.image.load_basic("img/laser2.bmp")
    #bullet2.image.set_colorkey((255, 255, 255))
    
    return (bullet, bullet2)

def single_gun(rect):
    bullet = Bullet((rect.midtop), down=False)
    if bullet.using_image == False:
        bullet.image.fill((0, 0, 255))
    #bullet.image = pygame.image.load_basic("img/laser2.bmp")
    #bullet.image = pygame.image.load_basic("img/super.bmp")
    #3bullet.image.set_colorkey((255, 255, 255))
    
    return [bullet]
