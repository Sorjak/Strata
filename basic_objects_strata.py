import pygame, random, os, sys, re, math
from random import choice
from time import time
from pygame.locals import *
from utils_strata import *
from math import hypot, atan2, radians, degrees
try:
    from pygame.math import Vector2
except ImportError:
    from math_strata import Vector2


class Particle(object):
    def __init__(self, pos=None, speed=None):
        random.seed()
        thing1 = round(choice([x * 0.1 for x in range(-10, 10)]) , 3)
        thing2 = round(choice([x * 0.1 for x in range(-10, 10)]) , 3)
        self.direction = Vector2(thing1, thing2)
        
        self.position = pos if pos else Vector2(random.randint(0, GAME_SIZE[0]), random.randint(0, GAME_SIZE[1]))
            
        self.speed = speed if speed else random.random()
    
    def move(self):
        displacement = Vector2(self.direction.x * self.speed, self.direction.y * self.speed)
        self.position = self.position + displacement
        self._bounce()
    
    def mouseEvent(self, pos):
        pass
    def _bounce(self):
        width = GAME_SIZE[0]
        height = GAME_SIZE[1]
        # x coords
        if self.position.x >= width - (self.rect.size[0] / 2):
            self.position.x = width - (self.rect.size[0] / 2)
            self.direction.reflect_ip(Vector2(-1, 0))
        elif self.position.x <= (self.rect.size[0] / 2):
            self.position.x = (self.rect.size[0] / 2)
            self.direction.reflect_ip(Vector2(1, 0))   
        # y coords  
        if self.position.y >= height - (self.rect.size[1] / 2):
            self.position.y = height - (self.rect.size[1] / 2)
            self.direction.reflect_ip(Vector2(0, -1))   
        elif self.position.y <= (self.rect.size[1] / 2):
            self.position.y = (self.rect.size[1] / 2)
            self.direction.reflect_ip(Vector2(0, 1))   
    
    
    def _setRandomPosition(self):
        self.position = Vector2(random.randint(0, GAME_SIZE[0]), random.randint(0, GAME_SIZE[1]))
        
    def _setRandomDirection(self):
        thing1 = round(choice([x * 0.1 for x in range(-10, 10)]) , 3)
        thing2 = round(choice([x * 0.1 for x in range(-10, 10)]) , 3)
        self.direction = Vector2(thing1, thing2)
        
    def _goToPoint(self, vector):
        self.direction = Vector2(vector - self.position).normalize()
        
    def _goAwayPoint(self, vector):
        temp = Vector2(vector - self.position)
        try:
            temp = temp.normalize()
        except ValueError:
            pass
        self.direction = temp.elementwise() * -1

        
class Static(object):
    def __init__(self, position = None):
        random.seed()
        if position:
            self.position = position
        else:
            self.position = Vector2(random.randint(0, GAME_SIZE[0]), random.randint(0, GAME_SIZE[1]-20))
    def mouseEvent(self, pos):
        pass
        
        
class Square(object):
    def __init__(self, tl, br, myarr, rough):
        self.tl = tl #Top left
        self.tr = Vector2(br.x, tl.y) #Top right
        self.br = br #Bottom right
        self.bl = Vector2(tl.x, br.y) #Bottom left
        self.dimensions = [self.tl, self.tr, self.br, self.bl]
        self.center = Vector2(br.x - ((br.x - tl.x) / 2), br.y - ((br.y - tl.y) / 2))
        self.myarr = myarr
        self.children = [None, None, None, None]
        self.rough = rough
        self.sqSize = br.x - tl.x
        self.value = self.getValue()
        self.myarr[int(self.center.x)][int(self.center.y)] = self.value
        self.makeRect()
        
    def divide(self, tiles):
        pass
        
    def getValue(self):
        avg = 0
        for d in self.dimensions:
            avg += self.myarr[int(d.x)][int(d.y)]
        
        avg = avg / 4
        return round(avg + random.uniform(-self.rough, self.rough), 3)
        
    def makeRect(self):
        self.rect = pygame.Rect((self.tl.x * MAPTILE_SIZE[0], self.tl.y * MAPTILE_SIZE[1]), (self.sqSize * MAPTILE_SIZE[0], self.sqSize * MAPTILE_SIZE[1]))