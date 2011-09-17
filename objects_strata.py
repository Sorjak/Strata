import pygame, random, os, sys, re, math
from time import time
from pygame.locals import *
from utils_strata import *
from maps_strata import *
from basic_objects_strata import *

from math import sin, cos


class Creep(Particle, pygame.sprite.DirtySprite):
    def __init__(self, id):
        pygame.sprite.DirtySprite.__init__(self)
        Particle.__init__(self)
        self.size = (15, 15)
        self.image_raw, self.rect = load_image("creep" + str(random.randint(1, 3)) + ".png", -1)
        self.image = pygame.transform.scale(self.image_raw, self.size)
        self.rect.size = self.size
        self.rect.center = (self.position.x, self.position.y)
        rndcolor = random.randint(1, 254)
        self.color = (rndcolor, rndcolor, rndcolor)
        self.id = id
        self.life = 50.0
        self.full = 0
        self.children = []
        self.selected = False
        self.fleeing = False
        self.grazing = False
        self.eating = False
        self.nearestFood = None
        
    def update(self):
        if self.eating:
            self.speed = 0
        else:
            if self.speed == 0:
                self._setRandomDirection()
                # self.speed = self.absoluteSpeed
            self.life -= .002
            self.speed = (self.life * 1.5) * .01

        self.move()
        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y
        
        if self.full >= 100:
            self.grow()

        if self.life <= 0:
            self.kill()

        
    def draw(self, screen):
        if self.selected:
            pygame.draw.rect(screen, RED, self.rect, 2)
        displacement = Vector2(self.direction.x * (self.speed * 30), self.direction.y * (self.speed * 30))
        
        if self.grazing:
            pygame.draw.line(screen, WHITE, self.rect.center, self.nearestFood.position)
        else:
            pygame.draw.line(screen, WHITE, self.rect.center, self.position + displacement)
        screen.blit(self.image, self.rect)
    
    def graze(self, food):
        self.nearestFood = self._findNearestFood(food)

        if self.nearestFood:
            self.grazing = True
            # if self in self.nearestFood.grazers:
                # self.eating = True
            # else:
                # self.eating = False
            self._goToPoint(self.nearestFood.position)
        else:
            self.grazing = False
            # self.eating = False

    def checkDanger(self, mp):
        if mp:
            distance = math.sqrt(((self.position.x - mp[0]) ** 2) + ((self.position.y - mp[1]) ** 2))
            if distance < 100:
                self._goAwayPoint(mp)
        
    def grow(self, enemies):
        self.children.append(Creep(NUM_CREEPS + 1))
        NUM_CREEPS += 1
        # if self.absoluteSpeed < .3:
            # self.absoluteSpeed += amount + .00005
        # elif self.absoluteSpeed > .75:
            # self.absoluteSpeed += amount - .00004
        # else:
            # self.absoluteSpeed += amount
        # if self.absoluteSpeed > .85:
            # self.absoluteSpeed = .85
        
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
            
    def _goToPoint(self, vector):
        self.direction = Vector2(vector - self.position).normalize()
        
    def _goAwayPoint(self, vector):
        self.direction = Vector2(vector - self.position).normalize()
        self.direction = self.direction.elementwise() * -1
        

class Food(Static, pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        Static.__init__(self)
        self.image, self.rect = load_image("cherries.png", -1)
        self.size = (20, 20)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect.size = self.size
        self.rect.center = (self.position.x, self.position.y)
        self.value = 25
        self.grazers = []
        
    def update(self):
        if self.value <= 0:
            for g in self.grazers:
                g.eating = False
            self.kill()

        else:
            for g in self.grazers:
                g.eating = True
                self.value -= .01
            
    def checkGrazers(self, grazers):
        self.grazers = []
        for g in grazers:
            if self.rect.colliderect(g.rect) and g.nearestFood is self:
                self.grazers.append(g)
    
    def draw(self, screen): 
        font = pygame.font.Font(None, 12)
        screen.blit(font.render("%s | %s" % (self.value, len(self.grazers)), 1, WHITE), (self.rect.left, self.rect.bottom+11))     
        
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

        