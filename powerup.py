# powerup.py
# this function defines classes for powerups
import pygame
import globalvars
import info



from pygame.locals import *

class PowerUp(pygame.sprite.Sprite):
    """ PowerUp:
        this class is the generic class for PowerUps.  It will not be used directly, but other classes will
        inherit PowerUp's memebers. """
    p = 1 # the probability of appearing.  for example:  this class has a 1/p probability of appearing
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self._next_update = 0
        
        
        # members you should edit in descendants
        self._speed = 1
        self.activate = self.do_nothing
            
    def do_nothing(self):
        pass
    
    def update(self, t):
        if t > self._next_update:
            self.move()
            self._next_update = t + 15
            # If we've reached a border, kill it.
            if self.rect.top > globalvars.HEIGHT:
                self.kill()
            
    def set_image(self, filename):
        self.image = pygame.image.load_basic(filename)
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        
    def move(self):
        self.rect.top += self._speed
        
# TODO: FIX ME
class Health(PowerUp):
    p = 1
    def __init__(self, pos):
        self.set_image("img/health.bmp")
        PowerUp.__init__(self, pos)
        self.activate = self.give_health
        
    def give_health(self):
        print 'yay2'
        globalvars.hero.give_hp(1)

class Money(PowerUp):
    p = 10 # probability of appearing
    def __init__(self, pos):
        self.set_image("img/money.bmp")
        PowerUp.__init__(self, pos)
        self.activate = self.give_money
        
    def give_money(self):
        globalvars.scr.add(1000)