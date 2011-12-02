import pygame, random, math
from pygame.locals import *
from utils_strata import *
from animal_strata import Animal
# from creep_strata import Creep


# food_types = [Creep]



class Hunter(Animal):
    def __init__(self, id, map, pos, speedmod, image="playericon.png", life=25.0, range=200):
        Animal.__init__(self, id, image, pos, None, life, range)
        self.size = (15, 15)
        self.image_raw, self.rect = load_image(image, -1)
        self.image = pygame.transform.scale(self.image_raw, self.size)
        self.rect.size = self.size
        self.rect.center = (self.position.x, self.position.y)
        self.nearestFood = None
        self.nearestEnemy = None
        self.map = map
        self.speedmod = speedmod if speedmod else random.uniform(2.3, 2.7)
        
    def _update(self):
        if not self.nearestEnemy:
            if not self.nearestFood or self.nearestFood.life <= 0:
                self.eating = False
            if self.eating and self.nearestFood.life > 0:
                self.speed = self.nearestFood.speed
                self.nearestFood.life = self.nearestFood.life - .05
                self.life += ANIMAL_DECAY
                self.full += .07
            else:
                if self.speed == 0:
                    self.eating = False
                if self.searching:
                    self.speed += .08
        else:
            self.eating = False
            self.searching = False

        myTiles = self.map.getTilesFromRect(self.rect)
        modifier = max([x.modifier for x in myTiles])
        if modifier == 4:
            self.speed /= 5.0
        elif modifier == 2:
            self.speed /= 1.5
        
        self._nextMove()

    def _draw(self, screen):
        pass
    
    def _search(self, food):
        pass
        
    def _foundFood(self, nFood):
        if self.rect.colliderect(nFood.rect):
            self.searching = False
            if nFood.life > 0:
                self.eating = True
        else:
            if not self.nearestEnemy:
                self._goToPoint(nFood.position)
        
    def _grow(self):
        friends = self.groups()
        newchild = Hunter(len(friends[0]) + 1,self.map, self.position, None)
        self.children.append(newchild)
        for f in friends:
            f.add(newchild)
            
    def _nextMove(self):
        if not self.nearestEnemy:
            if not self.eating and self.speed == 0:
                self._setRandomDirection()
        else:
            self._goAwayPoint(self.nearestEnemy.rect.center)