#!/usr/bin/env python
# world.py
#
# this is a template for a world
#
# Ideas:
# a world is a python script.
# it is an array of functions
# each function is a wave
# all functions will be passed the "bads" group to define bad guys

# each world file can define it's own enemies or import enemies from a enemy module

import enemy

def basic_one(bads):
    for y in [100]:
        for x in [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]:
            bads.add(enemy.BadAssMuthaFucka((x, y)))

def basic_two(bads):
    for y in [0, 100]:
        for x in [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]:
            bads.add(enemy.BadAssMuthaFucka((x, y)))

def basic_three(bads):
    for y in [0, 100, 200]:
        for x in [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]:
            bads.add(enemy.BadAssMuthaFucka((x, y)))
    
    

def windows(bads):
    for x in [200, 300, 400, 500, 600]:
        bads.add(enemy.Bad2((x, 50)))

def three(bads):
    for y in [0, 100]:
        for x in [200, 300, 400, 500, 600]:
            bads.add(enemy.SuperGuy((x, y)))

def new_movers(bads):
    for y in [0, 100, 200, 300]:
        for x in [100, 300, 600]:
            bads.add(enemy.NewMover((x, y)))

def kamak(bads):
    for y in [100, 200, 300, 400]:
        for x in [100, 200, 300, 400, 500]:
            bads.add(enemy.Kamakazee((x, y)))

def boss(bads):
    bads.add(enemy.Boss((300, 100)))

class World:
    pass

world = World()
world.name = "Template world"
world.wavefunc_list = [basic_one, basic_two, windows, basic_three, three, windows, three, new_movers, kamak, new_movers, kamak, boss]



