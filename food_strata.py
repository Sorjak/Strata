import pygame, random, math
from pygame.locals import *
from utils_strata import *
from globals_strata import *
from basic_objects_strata import Static
from plant_strata import Plant

class Cherry(Plant):
    def __init__(self, id, pos, map):
        Plant.__init__(self, id, "cherries.png", self.spawn(pos), map, life=25)
        self.selected = False
        self.map = map
        self.grazers = []
        
    def _update(self):
        for g in self.grazers:
            # g.eating = True
            self.life -= .01
                
    def checkGrazers(self, grazers):
        self.grazers = []
        for g in grazers:
            if self.rect.colliderect(g.rect) and g.nearestFood is self:
                self.grazers.append(g)
    
    def _draw(self, screen): 
        pass
        
    def _grow(self):
        pass
        
    def spawn(self, pos):
        if not pos:
            pass
    