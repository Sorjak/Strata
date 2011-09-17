import pygame, random, os, sys, re, math
from random import choice
from time import time
from pygame.locals import *
from utils_strata import *
from math import hypot, atan2, radians, degrees
from pygame.math import Vector2


class Particle(object):
    def __init__(self):
        random.seed()
        thing1 = round(choice([x * 0.1 for x in range(-10, 10)]) , 3)
        thing2 = round(choice([x * 0.1 for x in range(-10, 10)]) , 3)
        self.position = Vector2(random.randint(0, GAME_SIZE[0]), random.randint(0, GAME_SIZE[1]))
        self.direction = Vector2(thing1, thing2)
        self.speed = random.random()
    
    def move(self):
        displacement = Vector2(self.direction.x * self.speed, self.direction.y * self.speed)
        self.position = self.position + displacement
        self.bounce()
    
    def bounce(self):
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

class Static(object):
    def __init__(self, position = None):
        random.seed()
        if position:
            self.position = position
        else:
            self.position = Vector2(random.randint(0, GAME_SIZE[0]), random.randint(0, GAME_SIZE[1]-20))
