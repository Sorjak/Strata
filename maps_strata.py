import pygame, random
from pygame.locals import *
from pygame.math import Vector2 as Point

from utils_strata import *
from basic_objects_strata import Square

TILE_TYPES = {"grass" : ("grass.png", 1), "water" : ("water.png", 0.5), "mountain" : ("mountain.png", 0)}

class Map(pygame.Surface):
    def __init__(self, dimensions):
        pygame.Surface.__init__(self, dimensions)
        self.fill(WHITE)
        self.size = dimensions
        self.rect = pygame.Rect((0, 0), dimensions)
        self.tiles = []
        self.root = None
    
    def generateWorld(self, screen):
        pass 
        
    def generateWorld2(self):
        random.seed()

        mapGenArray = [[0 for col in range(MAP_GEN_NUM)] for row in range(MAP_GEN_NUM)]
        
        mapGenArray[0][0] = .7
        mapGenArray[0][MAP_GEN_NUM - 1] = .5
        mapGenArray[MAP_GEN_NUM - 1][0] = .3
        mapGenArray[MAP_GEN_NUM- 1][MAP_GEN_NUM - 1] = .1
        
        self.root = MapTile(Point(0, 0), Point(MAP_GEN_NUM - 1, MAP_GEN_NUM - 1), mapGenArray, MAP_GEN_ROUGH)
        # print sq.topleft, sq.topright, sq.bottomleft, sq.bottomright
        # print sq.center
        
        self.root.divide(self.tiles)
    
    def makeMapTile(self, where, height):
        mt = MapTile(where, height)
        self.tiles.append(mt)
    
    def draw(self, screen):
        screen.blit(self, self.rect)
        bottomBound = WINDOW_SIZE[1] - self.rect.top
        rightBound = WINDOW_SIZE[0] - self.rect.left
        leftBound = -(self.rect.left)
        topBound = -(self.rect.top)
        renderRect = pygame.Rect((leftBound, topBound), WINDOW_SIZE)
        for mt in self.tiles:
            mt.draw(self, renderRect)

class MapTile(Square, pygame.sprite.DirtySprite):
    def __init__(self, tl, br, myarr, rough):
        Square.__init__(self, tl, br, myarr, rough)
        pygame.sprite.DirtySprite.__init__(self)
        self.size = MAPTILE_SIZE

    def draw(self, screen, renderRect):
        if self.rect.colliderect(renderRect):
            screen.blit(self.image, self.rect)
    
    def divide(self, tiles):
        if self.sqSize == 1:
            self._mapify(tiles)
            return True
        self.children[0] = MapTile(self.tl, self.center, self.myarr, self.rough/2.0)
        self.children[3] = MapTile(self.center, self.br, self.myarr, self.rough/2.0)
        self.children[1] = MapTile(self.children[0].tr, self.children[3].tr, self.myarr, self.rough/2.0)
        self.children[2] = MapTile(self.children[0].bl, self.children[3].bl, self.myarr, self.rough/2.0)
        for child in self.children:
            child.divide(tiles)
            
    def _mapify(self, tiles):
        self.type = TILE_TYPES["grass"]
        
        if self.value > -.008 and self.value < .07:
            self.type = TILE_TYPES["grass"]
        elif self.value < -.008:
            self.type = TILE_TYPES["water"]
        elif self.value >= .07:
            self.type = TILE_TYPES["mountain"]
        
        self.image_raw, self.rect = load_image(self.type[0], -1)
        self.image = pygame.transform.scale(self.image_raw, self.size)
        self.rect.size = self.size
        self.rect.topleft = (self.tl.x * MAPTILE_SIZE[0], self.tl.y * MAPTILE_SIZE[1])
        tiles.append(self)