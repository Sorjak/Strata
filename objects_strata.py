import pygame, random, os, sys, re, math
from time import time
from pygame.locals import *
from utils_strata import *
from maps_strata import *
from basic_objects_strata import *

from math import sin, cos

class Animal(Particle, pygame.sprite.DirtySprite):
    def __init__(self, id, image, pos, speed, life):
        Particle.__init__(self, pos, speed)
        pygame.sprite.DirtySprite.__init__(self)
        self.size = (15, 15)
        self.image_raw, self.rect = load_image(image, -1)
        self.image = pygame.transform.scale(self.image_raw, self.size)
        self.rect.size = self.size
        self.rect.center = (self.position.x, self.position.y)
        self.id = id
        self.life = life
        self.full = 0
        self.children = []
        self.selected = False
        self.searching = False
        self.nearestFood = None
        
    def update(self, food):
        self._update()
        
        self.search(food)
        
        self.move()
        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y
        

        if self.life <= 0:
            self.kill()

        
    def draw(self, screen):
        self._draw(screen)
    
        if self.selected:
            pygame.draw.rect(screen, RED, self.rect, 2)
        displacement = Vector2(self.direction.x * (self.speed * 30), self.direction.y * (self.speed * 30))
        
        if self.searching:
            pygame.draw.line(screen, WHITE, self.rect.center, self.nearestFood.position)
        else:
            pygame.draw.line(screen, WHITE, self.rect.center, self.position + displacement)
        screen.blit(self.image, self.rect)
        
    def search(self, food):
        self.nearestFood = self._findNearestFood(food)
        
        self.searching = self.nearestFood is not None
        
        if self.searching:
            if self.rect.colliderect(self.nearestFood.rect):
                self._foundFood(self.nearestFood)
                self.searching = False
            else:
                self._goToPoint(self.nearestFood.position)
        
        self._search(food)
                
    def _update(self):
        pass
    
    def _draw(self):
        pass
    
    def _foundFood(self, nFood):
        pass
    
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
        

class Creep(Animal):
    def __init__(self, id, pos, speed, life=50.0):
        Animal.__init__(self, id, "creep" + str(random.randint(1, 3)) + ".png", pos, speed, life)
        
        self.fleeing = False
        self.eating = False
        
    def _update(self):
        if not self.nearestFood:
            self.eating = False
        if self.eating and self.nearestFood.life > 0:
            self.speed = 0
            self.full += .05
        else:
            if self.speed == 0:
                self.eating = False
                self._setRandomDirection()
            self.life -= .002
            self.speed = (self.life * 1.5) * .01
        
        if self.full >= 100:
            self._grow()
            self.full = 0

    def _draw(self, screen):
        pass
    
    def _search(self, food):
        pass
        
    def _foundFood(self, nFood):
        if nFood.life > 0 and len(nFood.grazers) <= 5:
            self.eating = True

    def checkDanger(self, mp):
        if mp:
            distance = math.sqrt(((self.position.x - mp[0]) ** 2) + ((self.position.y - mp[1]) ** 2))
            if distance < 100:
                self._goAwayPoint(mp)
        
    def _grow(self):
        friends = self.groups()
        print "#####################################################"
        print friends
        print dir(friends[0])
        print dir(friends[1])
        print "#####################################################"
        newchild = Hunter(len(friends[0]) + 1, self.position, None)
        self.children.append(newchild)
        for f in friends:
            f.add(newchild)

        
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
            

class Hunter(Animal):
    def __init__(self, id, pos, speed, life=50.0):
        Animal.__init__(self, id, "playericon.png", pos, speed, life)
        self.size = (15, 15)
        self.image_raw, self.rect = load_image("playericon.png", -1)
        self.image = pygame.transform.scale(self.image_raw, self.size)
        self.rect.size = self.size
        self.rect.center = (self.position.x, self.position.y)
        self.nearestFood = None
        
    def _update(self):
        if not self.nearestFood or self.nearestFood.life <= 0:
            self.eating = False
     
        if self.eating and self.nearestFood.life > 0:
            self.speed = self.nearestFood.speed
            self.nearestFood.life = self.nearestFood.life - .05
            # self.full += .05
        else:
            if self.speed == 0:
                self.eating = False
                self.speed = (self.speed + .01) * 1.5
                self._setRandomDirection()
            self.life -= .002
            self.speed = (self.life * 1.5) * .01
        
        # if self.full >= 100:
            # self._grow()
            # self.full = 0

    def _draw(self, screen):
        pass
    
    def _search(self, food):
        pass
        
    def _foundFood(self, nFood):
        if nFood.life > 0:
            self.eating = True

    # def checkDanger(self, mp):
        # if mp:
            # distance = math.sqrt(((self.position.x - mp[0]) ** 2) + ((self.position.y - mp[1]) ** 2))
            # if distance < 100:
                # self._goAwayPoint(mp)
        
    # def _grow(self):
        # friends = self.groups()
        # newchild = Creep(len(friends[0]) + 1, self.position, None)
        # self.children.append(newchild)
        # for f in friends:
            # f.add(newchild)


class Food(Static, pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        Static.__init__(self)
        self.image, self.rect = load_image("cherries.png", -1)
        self.size = (20, 20)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect.size = self.size
        self.rect.center = (self.position.x, self.position.y)
        self.life = 25
        self.grazers = []
        
    def update(self):
        if self.life <= 0:
            # for g in self.grazers:
                # g.eating = False
            self.kill()

        else:
            for g in self.grazers:
                # g.eating = True
                self.life -= .01
            
    def checkGrazers(self, grazers):
        self.grazers = []
        for g in grazers:
            if self.rect.colliderect(g.rect) and g.nearestFood is self:
                self.grazers.append(g)
    
    def draw(self, screen): 
        font = pygame.font.Font(None, 12)
        screen.blit(font.render("%s | %s" % (self.life, len(self.grazers)), 1, WHITE), (self.rect.left, self.rect.bottom+11))     
        
        screen.blit(self.image, self.rect)

class Structure(Static, pygame.sprite.DirtySprite):
    def __init__(self, type, position):
        pygame.sprite.DirtySprite.__init__(self)
        Static.__init__(self, position)
        self.image, self.rect = load_image(type[0], -1)
        self.size = MAPTILE_SIZE
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect.size = self.size
        self.rect.topleft = (self.position.x, self.position.y)

        