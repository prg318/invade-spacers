# enemy.py
import pygame
from pygame.locals import *
import weapons
#import invade 
import globalvars
import powerup
import random

### Movements ###
""" Below are a list of movement classes. Every enemy needs to use a movement 
class.  The movement class needs to provide a move function for the enemy
objects to call. """

class LineMovement:
    """ LineMovement - a movement for use by enemy classes.  This movement
    moves left to right a certain amount of pixels. """
    def __init__(self, (x, y)):
        self._dir = 1
        self._speed = 1
        self._initial_x = x
        self._initial_y = y 
        self.set_width(50)
        
    def set_speed(self, s):
        """ sets how many pixels the object will move per update """
        self._speed =  s
    
    def set_width(self, w):
        """ sets how many pixels the the object will move """
        self._bound_right = self._initial_x + w/2
        self._bound_left = self._initial_x - w/2
        
    def move(self, rect):
        """ LineMovement.move(self, rect):
            operates on an enemy's rect object.  This will move the
            enemy _speed pixels on every update """
        if rect.left < self._bound_left or rect.left > self._bound_right:
            self._dir = self._dir * -1
        rect.left += self._speed * self._dir
        
class EnterTopMovement:
    """ This movement moves an object into a level.  It will start the object
    50 pixels above the level, and will continue to move down.  The object can then
    choose to use another movement when the desired destination is reached. """
    def __init__(self, (x, y)):
        self._first = True
        self._speed = 1
    
    def set_speed(self, s):
        self._speed = s
        
    def move(self, rect):
        if self._first:
            rect.top = -50
            self._first = False
        rect.top += self._speed

class BounceMovement:
    """ A movmement that operates on a rect, and makes them bounce
    around the screen. """
    def __init__(self, (x, y)):
        self.set_speed(1)

    def set_speed(self, s):
        """ set how many pixels to move each update """
        self._vx = s
        self._vy = s
    
    def set_vy(self, vy):
        self._vy = vy
    
    def set_vx(self, vx):
        self._vx = vx
    
    def move(self, rect):
        # When we have reached an edge, turn around
        if rect.left < 0 or rect.right > globalvars.WIDTH:
            self._vx = self._vx * -1
        if rect.top < 0 or rect.bottom > globalvars.HEIGHT:
            self._vy = self._vy * -1
        
        rect.left += self._vx
        rect.top += self._vy

        

class SquareMovement:
    """ TODO: Clean and comment """
    def __init__(self, (x, y)):
        # self.pos can be either [t]op [l]eft [b]ottom or [r]ight.  this is used for the square_movement.
        self.pos = 't'
        self.bound = 50
        self.bound_left = x 
        self.bound_right = x + self.bound
        self.bound_up = y
        self.bound_down = y + self.bound
        self.square_has_run = 1
        self.speed = 1
    
    def set_speed(self, s):
        self.speed = s
        
    def move(self, rect):
        if self.pos == "t":
            rect.left -= self.speed
        if rect.left < self.bound_left:
            self.pos = "l"
        if self.pos == "l":
            rect.top += self.speed
            if rect.top > self.bound_down:
                self.pos = "b"
        if self.pos == "b":
            rect.left += self.speed
            if rect.left > self.bound_right:
                self.pos = "r"
        if self.pos == "r":
            rect.top -= self.speed
            if rect.top < self.bound_up:
                self.pos = "t"


class EnemyClass(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.initial_pos = pos
        
        self.bullets = []
        
        self.movement = LineMovement(pos)
        self.shoot = self.basic_front
        self.enter_level = EnterTopMovement(pos)
        
        self.next_update = 0
        self.next_shoot = 0
        
        self.point_value = 100
        
        self.hp = 1
        
        self.powerup = powerup.Money
        
        self.gun_delay = 3000
#        self.gun_delay = 100
        
        # clean me later
        self.first = True
        
    
    def on_shot(self):
        self.hp -= 1
        if self.hp == 0:
            return 1
        return 0
    
    def basic_front(self):
        my_bullet = weapons.Bullet(self.rect.midbottom, down=True)
        self.bullets.append(my_bullet)
              
    
    def set_image(self, filename):
        self.image = pygame.image.load_basic(filename)
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        
    
    
    def update(self, t):
        if t > self.next_update:
            self.move.move(self.rect)
            if self.rect.top > self.initial_pos[1]:
                self.move = self.movement
            if t > self.next_shoot:
                self.shoot()
                self.next_shoot = t + self.gun_delay
    
            self.next_update = t + 15
    
        
        
    
    def post_init(self):
        self.move = self.enter_level
        #self.gun_delay += random.randint(-self.gun_delay/6, self.gun_delay/6)
        self.gun_delay += random.randint(-500, 500)

class BadAssMuthaFucka(EnemyClass):
    def __init__(self, pos):
        EnemyClass.__init__(self, pos)
        self.set_image("img/enemy1.bmp")
        self.post_init()
        
class Bad2(EnemyClass):
    def __init__(self, pos):
        EnemyClass.__init__(self, pos)
        self.gun_delay = 800
        self.movement = SquareMovement(pos)
        self.movement.set_speed(2)
        self.set_image("img/enemy2.bmp")
        self.point_value = 150
        self.post_init()
        
class SuperGuy(EnemyClass):
    def __init__(self, pos):
        EnemyClass.__init__(self, pos)
        self.gun_delay = 1200
        self.movement = SquareMovement(pos)
        self.movement.set_speed(2)
        self.set_image("img/enemy3.bmp")
        self.point_value = 300
        #self.powerup = powerup.Health
        self.post_init()

class NewMover(EnemyClass):
    def __init__(self, pos):
        EnemyClass.__init__(self, pos)
        self.movement = BounceMovement(pos)
        self.movement.set_speed(2)
        
        self.set_image("img/enemy4.bmp")
        self.shoot = self.front_back_shoot
        self.post_init()
    
    def front_back_shoot(self):
        bullet1 = weapons.Bullet(self.rect.topleft, down=True)
        bullet2 = weapons.Bullet(self.rect.topleft, down=False)
        
        self.bullets.append(bullet1)
        self.bullets.append(bullet2)
        
class Kamakazee(EnemyClass):
    def __init__(self,pos):
        EnemyClass.__init__(self, pos)
        self.movement = BounceMovement(pos)
        self.movement.set_speed(4)
        
        self.shoot = self.no_shoot
        self.set_image("img/enemy5.bmp")
        self.post_init()
    def no_shoot(self):
        pass

class Boss(EnemyClass):
    def __init__(self, pos):
        EnemyClass.__init__(self, pos)
        self.set_image("img/boss1.bmp")
        self.movement = LineMovement(pos)
        self.movement.set_speed(5)
        self.movement.set_width(400)
        self.point_value = 1500
        self.gun_delay = 100
        
        self.hp = 10
        self.post_init()

