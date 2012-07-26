import pygame, random, math
from pygame.locals import *
from utils_strata import *
from globals_strata import *
from cherry_strata import Cherry
from hunter_strata import Hunter
from creep_strata import Creep


class BaseManager(object):
    def __init__(self, game, seednum):
        self.game = game
        self.map = game.map
        self.seednum = seednum
        self.members = []
        
    def seed(self):
        pass
    
    def update(self):
        for m in self.members:
            m.update()
            
    def __len__(self):
        return len(self.members)
            
    def draw(self, screen):
        for m in self.members:
            m.draw(screen)
            
    def collidesWith(self, point):
        for m in self.members:
            if (m.rect.collidepoint(point)):
                return m
        return None
        
    
class PlantManager(BaseManager):
    def __init__(self, game, seednum):
        BaseManager.__init__(self, game, seednum)
        
    def seed(self):
        for i in range(0, random.randint(self.seednum /2 , self.seednum) - 1):
            c = Cherry(i, None, self.game)
            self.members.append(c)
            
class CreepManager(BaseManager):
    def __init__(self, game, seednum):
        BaseManager.__init__(self, game, seednum)
        
    def seed(self):
        for i in range(0, random.randint(self.seednum / 2 , self.seednum)-1):
            self.members.append(Creep(i, self.game, None, None))
            
class HunterManager(BaseManager):
    def __init__(self, game, seednum):
        BaseManager.__init__(self, game, seednum)
        
    def seed(self):
        for i in range(0, random.randint(self.seednum/2, self.seednum)):
            self.members.append(Hunter(i, self.game, None, None, life=25.0))  