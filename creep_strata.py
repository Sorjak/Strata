import pygame, random, math
from pygame.locals import *
from utils_strata import *
# from globals_strata import *
from animal_strata import Animal
from hunter_strata import Hunter

class Creep(Animal):
    def __init__(self, id, map, pos, speed, speedmod=None, life=50.0, range=150):
        Animal.__init__(self, id, "creep" + str(random.randint(1, 3)) + ".png", pos, speed, life, range)
        self.map = map
        self.nearestEnemy = None
        self.eating = False
        self.range = random.randint(50, 150)
        self.speedmod = speedmod if speedmod else random.uniform(0.8, 1.5)
        
    def _update(self):
        if not self.nearestEnemy:
            if not self.nearestFood:
                self.eating = False
            if self.eating and self.nearestFood.life > 0:
                self.speed = 0
                self.life += ANIMAL_DECAY
                self.full += .05
            else:
                if self.speed == 0:
                    self.eating = False
        else:
            self.eating = False
            self.searching = False

        myTiles = self.map.getTilesFromRect(self.rect)
        modifier = max([x.modifier for x in myTiles])
        self.speed = self.speed / modifier
        
        self._nextMove()


    def _draw(self, screen):
        if self.id == 1:
            pygame.draw.rect(screen, BLUE, self.rect)
    
    def _search(self, food):
        pass
        
    def _foundFood(self, nFood):
        if self.rect.colliderect(nFood.rect):
            self.searching = False
            if nFood.life > 0 and len(nFood.grazers) <= 5:
                self.eating = True
        else:
            if not self.nearestEnemy:
                self._goToPoint(nFood.position)

    def checkDanger(self, hunters):
        self.nearestEnemy  = self._findNearestEntity(hunters)

    def _grow(self):
        friends = self.groups()
        newchild = Creep(len(friends[0]) + 1, self.map, self.position, None)
        self.children.append(newchild)
        for f in friends:
            f.add(newchild)
            
    def _nextMove(self):
        if not self.nearestEnemy:
            if not self.eating and self.speed == 0:
                self._setRandomDirection()
        else:
            self._goAwayPoint(self.nearestEnemy.rect.center)

        
    def _findNearestFood(self, food):
        mini = (None, 99999)
        for f in food:
            if self in f.grazers:
                mini = (f, 0)
                break
            if len(f.grazers) <= 5:
                distance = math.sqrt(((self.position.x - f.position.x) ** 2) + ((self.position.y - f.position.y) ** 2))
                
                if distance < mini[1]:
                    mini = (f, distance)  
        if mini[1] < 200:
            return mini[0]
        else:
            return None