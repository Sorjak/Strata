import pygame, random, math
from pygame.locals import *
from utils_strata import *
from animal_strata import Animal

class Hunter(Animal):
    def __init__(self, id, game, pos, speedmod, image="playericon.png",  life=25.0, range=200):
        Animal.__init__(self, id, image, pos, None, life, range)
        self.size = (10, 10)
        self.image_raw, self.rect = load_image(image, -1)
        self.image = pygame.transform.scale(self.image_raw, self.size)
        self.rect.size = self.size
        self.rect.center = (self.position.x, self.position.y)
        self.nearestFood = None
        self.nearestEnemy = None
        self.game = game
        self.speedmod = speedmod if speedmod else random.uniform(2.3, 2.7)
        
    def _update(self):
        if not self.nearestEnemy:
            if not self.nearestFood or self.nearestFood.life <= 0:
                self.eating = False
            if self.eating and self.nearestFood.life > 0 and self.rect.colliderect(self.nearestFood) :
                self._feed()
            else:
                if self.speed == 0:
                    self.eating = False
                if self.searching:
                    self.speed += .08
        else:
            self.eating = False
            self.searching = False

        myTiles = self.game.map.getTilesFromRect(self.rect)
        modifier = max([x.modifier for x in myTiles])
        if modifier == 4:
            self.speed /= 5.0
        elif modifier == 2:
            self.speed /= 1.5
        
        self._nextMove()

    def _draw(self, screen):
        if self.id == 1:
            pygame.draw.rect(screen, BLUE, self.rect)

        pygame.draw.polygon(screen, RED, \
            [[self.rect.centerx, self.rect.top], \
            [self.rect.left, self.rect.bottom], \
            [self.rect.right, self.rect.bottom]], 1)
    
    def _search(self):
        food = self.game.oEntities['creeps']
        self.nearestFood = self._findNearestFood(food)
        
        self.searching = self.nearestFood is not None
        
        if self.searching:
            self._foundFood(self.nearestFood)
        
    def _foundFood(self, nFood):
        if self.rect.colliderect(nFood.rect):
            self.searching = False
            if nFood.life > 0:
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
        self.speed = self.nearestFood.speed
        self.nearestFood.life = self.nearestFood.life - .07
        self.life += self.decay
        self.full += .07

    def checkDanger(self, hunters):
        self.nearestEnemy  = self._findNearestEntity(hunters)

    def _grow(self):
        nextid = self.game.getNextId('preds')
        newchild = Hunter(nextid, self.game, self.position, None)
        self.game.addEntity(newchild, 'preds')
            
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
            distance = math.sqrt(((self.position.x - f.position.x) ** 2) + ((self.position.y - f.position.y) ** 2))
            
            if distance < mini[1]:
                mini = (f, distance)  
        if mini[1] < 200:
            return mini[0]
        else:
            return None