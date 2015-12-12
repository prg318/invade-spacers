#!/usr/bin/env python2
# invade.py
# fg space invadors
# space invadors clone because I am bored.

from globalvars import * 
import os
import random
import pygame
import sys
import enemy
import world
import powerup
import info
from pygame.locals import *

import herof


def pause():
    """ pause() pauses the entire game; it is a blocker and will not allow anything
    else to run until the game is unpaused """
    
    time = pygame.time.get_ticks()
    
    # loop until the game is unpaused or quit
    while 1:
        event = pygame.event.wait()
        pygame.display.flip()
        
        if event.type == KEYDOWN:
            if event.key == K_PAUSE:
                break
            if event.key == K_ESCAPE:
                sys.exit(1)
        if event.type == QUIT:
            sys.exit(1)
            
    # objects that use time delays must compensate for time the game was paused.
    time_diff = pygame.time.get_ticks() - time
    for x in enemy_grp:
        x.next_shoot += time_diff

    
def reset():
    """ reset the entire game.  this redraws the background, resets the score, and 
    recreates other objects """
    global scr, bg, level, hero, screen, hp
    
    for x in sprite_groups:
        x.empty()
    
    bg = make_bg()
    screen.blit(bg, (0,0))
    
    
    pygame.display.flip()

    scr.set(0)
    scr.show()    
    info_grp.add(scr)
    
    
    hero = herof.Hero((300, 550))
    hero_grp.add(hero)
    
    level = 0
    world.world.wavefunc_list[level](enemy_grp)

    hp = info.HpMeter((0,0))
    info_grp.add(hp)

def make_bg():
    BG_COLOR = (0, 0, 25)
    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.fill(BG_COLOR)
    
    for i in range(1, 100):
        x = random.randint(1, WIDTH)
        y = random.randint(1, HEIGHT)
        pygame.draw.circle(bg, (255, 255, 255), (x, y),1)
    
    return bg

def game_over():
    #font = pygame.font.SysFont("freesansbold", 125)
    #font2 = pygame.font.SysFont("freesansbold", 40)
    font = pygame.font.Font("freesansbold.ttf", 100)
    font2 = pygame.font.Font("freesansbold.ttf", 40)

    image = font.render("GAME OVER", True, (255, 255, 255))
    points = font2.render("Points: " + str(scr.get_score()), True, (255, 255, 255))
    image2 = font2.render("Do you want to play again? [y/n]", True, (255, 255, 255)) 
    screen.blit(image, (150, 100))
    screen.blit(points, (200, 225))
    screen.blit(image2, (20, 550))
    pygame.display.flip()
    while 1:
        event = pygame.event.wait()
        pygame.display.flip()
        
        if event.type == KEYDOWN:
            if event.key == K_y:
                reset()
                return
            if event.key == K_n or event.key == K_ESCAPE:
                break
        if event.type == QUIT:
            break
            
    sys.exit(0)

def you_win():
    font = pygame.font.Font("freesansbold.ttf", 100)
    font2 = pygame.font.Font("freesansbold.ttf", 40)
    image = font.render("YOU WIN", True, (255, 255, 255))
    points = font2.render("Points: " + str(scr.get_score()), True, (255, 255, 255))
    image2 = font2.render("Do you want to play again? [y/n]", True, (255, 255, 255)) 
    screen.blit(image, (150, 100))
    screen.blit(points, (200, 225))
    screen.blit(image2, (20, 550))
    pygame.display.flip()
    while 1:
        event = pygame.event.wait()
        pygame.display.flip()
        
        if event.type == KEYDOWN:
            if event.key == K_y:
                reset()
                return
            if event.key == K_n or event.key == K_ESCAPE:
                break
        if event.type == QUIT:
            break
            
    sys.exit(0)
        
        
    
def play_sound(filename):
    """ play_sound(filename):
            a wrapper around the pygame sound playing functions. """
    if pygame.mixer.get_init():
        snd = pygame.mixer.Sound(filename)
        snd.play() 




# groups
info_grp = pygame.sprite.RenderUpdates()
hero_grp = pygame.sprite.RenderUpdates()
hero_bullet_grp = pygame.sprite.RenderUpdates()
enemy_bullet_grp = pygame.sprite.RenderUpdates()
enemy_grp= pygame.sprite.RenderUpdates()
stuff_grp = pygame.sprite.RenderUpdates()

sprite_groups = [info_grp, hero_grp, hero_bullet_grp, enemy_bullet_grp, enemy_grp, stuff_grp]

if __name__ == "__main__":
    ##
    # Initiation
    ##
    pygame.init()
    try:
        pygame.mixer.init()
    except:
        print "sound couldn't be initialized."
        pass
    icon = pygame.image.load_basic("icon/ex2.bmp")
    icon.set_colorkey((255, 255, 255, 0))
    pygame.display.set_icon(icon)
    
    #screen =  pygame.display.set_mode((WIDTH, HEIGHT))
    screen =  pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN)
    pygame.display.set_caption("Invade Spacers")
    
    bg = 0
    hp = 0
    level = 0
    reset()
    
    while 1:
        pygame.display.flip()
        event = pygame.event.wait()
        if event.type == KEYDOWN:
            break
   
    while 1:
        for x in sprite_groups:
            x.update(pygame.time.get_ticks())
            rectlist = x.draw(screen)
            pygame.display.update(rectlist)
            x.clear(screen, bg)
        
        # take bullets from enemy's queue and add them to the bullet group
        for x in enemy_grp.sprites():
            for y in x.bullets:
               enemy_bullet_grp.add(y)
            # clear the bullet queue
            x.bullets = []
        
        ### Collision detection ###
        dict = pygame.sprite.groupcollide(enemy_grp, hero_bullet_grp, False, True)
        for x in dict:
            
            play_sound("sound/explode3.wav")
            
            if x.on_shot() == 1:
                scr.add(dict.items()[0][0].point_value)
                
                # decide if powerup should be given
                r = random.randint(0, x.powerup.p)
                if r == 0:
                    p = x.powerup((x.rect.left, x.rect.top))
                    stuff_grp.add(p) 
                x.kill()
        
        # if there are no enemies left, advance to the next wave
        if enemy_grp.__len__() == 0:
            play_sound("sound/yay.wav")
            level += 1
            # if there are no waves left...
            if level == world.world.wavefunc_list.__len__():
                you_win()
            world.world.wavefunc_list[level](enemy_grp)
        
        dict = pygame.sprite.groupcollide(hero_grp, enemy_bullet_grp, False, True)
        if dict:
            play_sound("sound/oh_no.wav")
            hero.cur_hp -=1
            hp.set_meter(hero.cur_hp, hero.max_hp)
            if hero.cur_hp == 0:
                game_over()
        
        dict = pygame.sprite.groupcollide(hero_grp, enemy_grp, True, True)
        if dict:
            play_sound("sound/oh_no.wav")
            hero.cur_hp = 0
            hp.set_meter(hero.cur_hp, hero.max_hp)
            if hero.cur_hp == 0:
                game_over()
            
            
        
        dict = pygame.sprite.groupcollide(stuff_grp, hero_grp, False, False)
        for x in dict:
            # TODO: Check to see if its a powerup
            x.activate()
            x.kill()
        
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]: hero.vx = -hero.speed
        if keys[K_RIGHT]: hero.vx = hero.speed
        if keys[K_LEFT] == 0 and keys[K_RIGHT] == 0: hero.vx = 0
        if keys[K_UP]: hero.vy = -hero.speed
        if keys[K_DOWN]: hero.vy = hero.speed
        if keys[K_UP] == 0 and keys[K_DOWN] == 0: hero.vy = 0
        if keys[K_RETURN] or keys[K_SPACE]:
            if pygame.time.get_ticks() > hero.next_shoot:
                b = hero.shoot()
                if b:
                    for x in b:
                        hero_bullet_grp.add(x)
                hero.next_shoot = pygame.time.get_ticks() + hero.shoot_delay

        
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: sys.exit(0)
            if event.key == K_PAUSE: pause()
            if event.key == K_F3:
                if pygame.mixer.get_init():
                    pygame.mixer.quit()
                else:
                    try:
                        pygame.mixer.init()
                    except:
                        print "sound couldn't be initialized."

        if event.type == QUIT:
            sys.exit(0)
