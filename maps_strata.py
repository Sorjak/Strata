import pygame, random
from pygame.locals import *
from utils_strata import *

TILE_TYPES = {"grass" : ("grass.png", 8), "water" : ("water.png", 2)}

class Map(pygame.Surface):
    def __init__(self, dimensions):
        pygame.Surface.__init__(self, dimensions)
        self.fill(WHITE)
        self.size = dimensions
        self.rect = pygame.Rect((0, 0), dimensions)
        self.tiles = []
    
    def generateWorld(self, screen):
        random.seed()
        rowSize = self.size[0] / MAPTILE_SIZE[0]
        columnSize = self.size[1] / MAPTILE_SIZE[1]
        waterDict = {}
        temp = []
        tileListPos = 0
        for iy in range(0, self.size[1], MAPTILE_SIZE[1]):
            realy = iy / MAPTILE_SIZE[1]
            for ix in range(0, self.size[0], MAPTILE_SIZE[0]):   
                realx = ix / MAPTILE_SIZE[0] 
                tileListPos = (realx + (rowSize * (realy))) - 1
                num = random.randint(1, 100)
                type = "grass"
                
                #checking if a water tile needs to be created
                if len(self.tiles) > 1:
                    waterFlag = False
                    if len(temp) == 4:
                        waterDict[temp[0]] = temp
                        temp = []
                        type = "water"
                    elif len(temp) > 0:
                        temp.append(tileListPos)
                        type = "water"
                                        
                    if (tileListPos - rowSize) in waterDict:
                        if num > 50:
                            waterFlag = True
                    elif (tileListPos - (rowSize * 2))  in waterDict and (tileListPos - rowSize) in waterDict:
                        if num > 50:
                            waterFlag = True
                    else:
                        if num == 100:
                            waterFlag = True

                    if waterFlag:
                        if len(temp) == 0:
                            temp.append(tileListPos)
                            type = "water"
                                
                mt = MapTile((ix, iy), type, tileListPos)
                self.tiles.append(mt)
                
        print waterDict
    def draw(self, screen):
        screen.blit(self, self.rect)
        bottomBound = WINDOW_SIZE[1] - self.rect.top
        rightBound = WINDOW_SIZE[0] - self.rect.left
        leftBound = -(self.rect.left)
        topBound = -(self.rect.top)
        renderRect = pygame.Rect((leftBound, topBound), WINDOW_SIZE)
        for mt in self.tiles:
            mt.draw(self, renderRect)

class MapTile(pygame.sprite.DirtySprite):
    def __init__(self, where, type, truex = None):
        pygame.sprite.DirtySprite.__init__(self)
        self.size = MAPTILE_SIZE
        self.typeName = type
        self.type = TILE_TYPES[type]
        self.image_raw, self.rect = load_image(self.type[0], -1)
        self.truex = truex
        self.image = pygame.transform.scale(self.image_raw, self.size)
        self.rect.size = self.size
        self.rect.topleft = where
    def draw(self, screen, renderRect):
        if self.rect.colliderect(renderRect):
            screen.blit(self.image, self.rect)