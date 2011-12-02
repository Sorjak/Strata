import pygame, random
from pygame.locals import *
try:
    from pygame.math import Vector2 as Point
except ImportError:
    from math_strata import Vector2 as Point

from utils_strata import *
from basic_objects_strata import Square

TILE_TYPES = {"grass" : ("grass.png", 1.0), "water" : ("water.png", 2.0), "mountain" : ("mountain.png", 4.0)}

class Map(pygame.Surface):
    def __init__(self, dimensions):
        pygame.Surface.__init__(self, dimensions)
        self.fill(WHITE)
        self.size = dimensions
        self.rect = pygame.Rect((0, 0), dimensions)
        self.tiles = []
        self.root = None
        
    def generateWorld(self):
        random.seed()

        mapGenArray = [[0 for col in range(MAP_GEN_NUM)] for row in range(MAP_GEN_NUM)]
        
        mapGenArray[0][0] = random.uniform(.1, .9)
        mapGenArray[0][MAP_GEN_NUM - 1] = random.uniform(.1, .9)
        mapGenArray[MAP_GEN_NUM - 1][0] = random.uniform(.1, .9)
        mapGenArray[MAP_GEN_NUM- 1][MAP_GEN_NUM - 1] = random.uniform(.1, .9)
        
        self.root = MapTile(Point(0, 0), Point(MAP_GEN_NUM - 1, MAP_GEN_NUM - 1), mapGenArray, MAP_GEN_ROUGH)
        
        self.root.divide(self.tiles)
        
        # print self._getRootHeight(self.root, 0)
        
    def makeMapTile(self, where, height):
        mt = MapTile(where, height)
        self.tiles.append(mt)
    
    def getTilesFromRect(self, myrect):
        root = self.root
        result = []
        self._getTilesRecursive(myrect, root, result)
        return result
        
    def _getTilesRecursive(self, myrect, region, result):
        if not region.children[0]:
            return region
        
        for child in region.children:
            if myrect.colliderect(child.rect):
                node = self._getTilesRecursive(myrect, child, result)
                if node:
                    result.append(node)
    
    def _getRootHeight(self, node, count):
        if not node.children[0]:
            return count
        
        return self._getRootHeight(node.children[0], count + 1)
        
    
    def draw(self, screen):
        screen.blit(self, self.rect)
        bottomBound = WINDOW_SIZE[1] - self.rect.top
        rightBound = WINDOW_SIZE[0] - self.rect.left
        leftBound = -(self.rect.left)
        topBound = -(self.rect.top)
        renderRect = pygame.Rect((leftBound, topBound), WINDOW_SIZE)
            
        tiles = self.getTilesFromRect(renderRect)
        
        for maptile in tiles:
            maptile.draw(self, renderRect)


class MapTile(Square, pygame.sprite.DirtySprite):
    def __init__(self, tl, br, myarr, rough):
        Square.__init__(self, tl, br, myarr, rough)
        pygame.sprite.DirtySprite.__init__(self)
        self.size = MAPTILE_SIZE

    def draw(self, screen, renderRect):
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
        elif self.value < -.0075:
            self.type = TILE_TYPES["water"]
        elif self.value >= .07:
            self.type = TILE_TYPES["mountain"]
        
        self.image_raw, self.rect = load_image(self.type[0], -1)
        self.image = pygame.transform.scale(self.image_raw, self.size)
        self.rect.size = self.size
        self.rect.topleft = (self.tl.x * MAPTILE_SIZE[0], self.tl.y * MAPTILE_SIZE[1])
        self.modifier = self.type[1]
        tiles.append(self)
        