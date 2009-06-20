import globalvars
import pygame
import invade
import weapons
from pygame.locals import *


god = False
#god = True

class Hero(pygame.sprite.Sprite):
    """ Hero() - The hero class is the player's object.  """
    def __init__(self, pos):
        #self.color = (255, 150, 0)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.image = pygame.image.load_basic("img/ship.bmp")
        self.image.set_colorkey((255,255,255), RLEACCEL)
       
        self.max_hp = 3
        self.cur_hp = self.max_hp
        
        self.gun = weapons.single_gun
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.speed = 3
        self.vx = 0
        self.vy = 0
        self.next_shoot = 0
        self.shoot_delay = 300
        if god:
            self.shoot_delay = 0
        
        
        self.alive = True
    
        self.next_update = 0
    def update(self, t):
        if t > self.next_update:
            self.rect.top += self.vy
            self.rect.left += self.vx
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > globalvars.WIDTH:
                self.rect.right = globalvars.WIDTH
            if self.rect.bottom > globalvars.HEIGHT:
                self.rect.bottom = globalvars.HEIGHT
            
            self.next_update = t + 15
            
    def shoot(self):
        """ Hero.shoot():
        this function returns two bullets, which will be added to the hero_bullet_grp in the main loop """
        if self.alive == False:
            return
        invade.play_sound("sound/laser.wav")
        
        
        
        return (self.gun(self.rect))
    
    def give_hp(self, val):
        print "before", self.cur_hp
        if self.cur_hp < self.max_hp:
            self.cur_hp += val
            globalvars.hp.set_meter(self.cur_hp, self.max_hp)
        print "after", self.cur_hp