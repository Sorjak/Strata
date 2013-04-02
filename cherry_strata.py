import pygame, random, math
from pygame.locals import *
from utils_strata import *
from globals_strata import *
from basic_objects_strata import Static
from plant_strata import Plant

class Cherry(Plant):
    def __init__(self, id, pos, game):
        Plant.__init__(self, id, "cherries.png", pos, game, life=25)
        self.selected = False
        self.grazers = []
        
    def _update(self):
        self.checkGrazers(self.game.oEntities['creeps'])
        for g in self.grazers:
            # g.eating = True
            self.life -= .01
                
    def checkGrazers(self, grazers):
        self.grazers = []
        for g in grazers:
            if self.rect.colliderect(g.rect) and g.nearestFood is self:
                self.grazers.append(g)
    
    def _draw(self, screen): 
        pygame.draw.circle(screen, GREEN, self.rect.center, self.rect.width / 2, 1)
        
    def grow(self, plants):
        Plant.grow(self, Cherry, plants)
    