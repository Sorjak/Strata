import pygame, random, math
from pygame.locals import *
from utils_strata import *
from animal_strata import Animal
from hunter_strata import Hunter

class Creep(Animal):
    def __init__(self, id, game, pos, speed, speedmod=None, life=50.0, range=150):
        Animal.__init__(self, id, "creep" + str(random.randint(1, 3)) + ".png", pos, speed, life, range)
        self.nearestEnemy = None
        self.eating = False
        self.range = random.randint(50, 150)
        self.speedmod = speedmod if speedmod else random.uniform(0.8, 1.5)
        self.game = game
        
    def _update(self):
        self.checkDanger(self.game.oEntities['preds'])
        if self.nearestEnemy:
            self.eating = False
            self.searching = False
        else:
            if self.nearestFood:
                if self.eating and self.nearestFood.life > 0:
                    self._feed()
                if self.nearestFood.life <= 0:
                    self._finishedEating()
            else:
                self.eating = False
                self.searching = True


        myTiles = self.game.map.getTilesFromRect(self.rect)
        modifier = max([x.modifier for x in myTiles])
        self.speed = self.speed / modifier
        
        self._nextMove()

    def _draw(self, screen):
        if self.id == 1:
            pygame.draw.rect(screen, BLUE, self.rect)

        pygame.draw.rect(screen, (200, 0, 200), self.rect, 1)
    
    def _search(self):
        food = self.game.oEntities['food']
        self.nearestFood = self._findNearestFood(food)
        
        self.searching = self.nearestFood is not None
        
        if self.searching:
            self._foundFood(self.nearestFood)
        
    def _foundFood(self, nFood):
        if self.rect.colliderect(nFood.rect):
            self.searching = False
            if nFood.life > 0 and len(nFood.grazers) <= 5:
                self.eating = True
        else:
            if not self.nearestEnemy:
                self._goToPoint(nFood.position)

    def _finishedEating(self):
        self.eating = False
        self.searching = True
        self.nearestFood = None
        self.speed = 0

    def _feed(self):
        self.speed = 0
        self.life += self.decay
        self.full += .05

    def checkDanger(self, hunters):
        self.nearestEnemy = self._findNearestEntity(hunters)

    def _grow(self):
        nextid = self.game.getNextId('creeps')
        newchild = Creep(nextid, self.game, self.position, None)
        self.game.addEntity(newchild, 'creeps')
            
    def _nextMove(self):
        if self.speed == 0:
            if self.eating:
                pass
            else:
                self.speed = self.speedmod
                self._setRandomDirection()
        if self.nearestEnemy:
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