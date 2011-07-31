import pygame, random, os, sys, re, math
from time import time
from pygame.locals import *
from utils_strata import *

drag = 1
elasticity = 1
gravity = (math.pi, 0)

class Particle(object):
    def __init__(self):
        random.seed()
        self.x = random.randint(0, WINDOW_SIZE[0])
        self.y = random.randint(0, WINDOW_SIZE[1])
        self.angle = random.uniform(0, math.pi*2)
        self.speed = random.random()
    
    def move(self):
        # self.speed *= drag
        (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.bounce()
    
    def bounce(self):
        width = WINDOW_SIZE[0]
        height = WINDOW_SIZE[1]
        if self.x >= width - self.rect.size[0]:
            self.angle = 2*math.pi - self.angle
            self.x = width - self.rect.size[0]
            self.speed *= elasticity
        elif self.x <= 0:
            self.angle = 2*math.pi - self.angle
            self.x = 1
            self.speed *= elasticity
            
        if self.y >= height - self.rect.size[1]:
            self.angle = math.pi - self.angle
            self.y = height - self.rect.size[1]
            self.speed *= elasticity
        elif self.y <= 0:
            self.angle = math.pi - self.angle
            self.y = 1
            self.speed *= elasticity
    


class Static(object):
    def __init__(self):
        random.seed()
        self.x = random.randint(0, WINDOW_SIZE[0])
        self.y = random.randint(0, WINDOW_SIZE[1])