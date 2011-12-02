import os, sys, pygame, random
from pygame.locals import *
from globals_strata import *

class StrataGroup(pygame.sprite.RenderPlain):
    def __init__(self, type):
        pygame.sprite.RenderPlain.__init__(self)
        self.type = type
    
    def getType(self):
        return self.type