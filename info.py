# info.py
import pygame
import globalvars

class Score(pygame.sprite.Sprite):
    def __init__(self, pos):
        self._score = 0
        self.image = pygame.Surface((32, 32))
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self._show = False
    
    def show(self):
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.image = self.font.render(str(self._score), True, (255, 255, 255, 255))
        self._show = True
    
    def get_score(self):
        return self._score
        

    def add(self, val):
        self._score += val
        if self._show:
            self.image = self.font.render(str(self._score), True, (255, 255, 255, 255))

    
    def set(self, val):
        self._score = val

        
    def remove(self, val):
        pass
        
    
    def update(self, t):
        pass
        

class HpMeter(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.color = (0, 255 ,0)
        self.height = globalvars.HEIGHT
        self.width = 15
        self.image = pygame.Surface((self.width, self.height)) #= pygame.Rect([0, 0, 40, 40])
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255, 255, 255))
        self.image.fill(self.color)
        self.rect.topleft = pos
        
    def update(self, t):
        pass
        
    def set_meter(self, current, max):
        self.image.fill((255,255,255))
        
        ratio = float(current)/float(max)
        
        if ratio >= 0:
            self.color = (255, 0, 0)
        if ratio >= float(1)/float(2):
            self.color = (255, 255, 0)
        if ratio == 1:
            self.color = (0, 255, 0)
        
        if(current > 0):
            height = self.height * current/max
            pygame.draw.rect(self.image, self.color, [0, globalvars.HEIGHT - height, self.width, height])
            
        
