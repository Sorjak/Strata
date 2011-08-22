import pygame, random
from pygame.locals import *
from utils_strata import *


class Map(pygame.Surface):
    def __init__(self, dimensions):
        pygame.Surface.__init__(self, dimensions)
        self.fill(WHITE)
        self.size = dimensions
        self.movelayer = pygame.Surface(dimensions)
        self.movelayer.fill((255,0,255))
        self.movelayer.set_colorkey((255,0,255))
        self.rect = pygame.Rect((0, 0), dimensions)
    
    def generateWorld(self, screen):
        for ix in range(0, self.size[0], MAPTILE_SIZE[0]):
            for iy in range(0, self.size[1], MAPTILE_SIZE[1]):
                mt = MapTile((ix, iy))
                self.blit(mt.image, mt.rect)
     
    def draw(self, screen):
        screen.blit(self, self.rect)
        screen.blit(self.movelayer, self.rect)
    
class MapTile(pygame.sprite.DirtySprite):
    def __init__(self, where):
        pygame.sprite.DirtySprite.__init__(self)
        self.size = MAPTILE_SIZE
        random.seed()
        num = random.randint(1, 2)
        if num == 1:
            self.image_raw, self.rect = load_image("water.png", -1)
        elif num == 2:
            self.image_raw, self.rect = load_image("grass.png", -1)
        self.image = pygame.transform.scale(self.image_raw, self.size)
        self.rect.size = self.size
        self.rect.topleft = where