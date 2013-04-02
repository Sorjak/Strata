import pygame, random, os, sys, re, math
from pygame.locals import *
from utils_strata import *
from superclasses_strata import Animal
from basic_objects_strata import Static

# from math import sin, cos



class Structure(Static, pygame.sprite.DirtySprite):
    def __init__(self, type, position):
        pygame.sprite.DirtySprite.__init__(self)
        Static.__init__(self, position)
        self.image, self.rect = load_image(type[0], -1)
        self.size = MAPTILE_SIZE
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect.size = self.size
        self.rect.topleft = (self.position.x, self.position.y)

        