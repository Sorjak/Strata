import pygame, random, math
from pygame.locals import *
from pygame.sprite import DirtySprite
from utils_strata import *
from globals_strata import *
from basic_objects_strata import Static

class Plant(Static, pygame.sprite.DirtySprite):
    def __init__(self, id, image, pos, game, life):
        Static.__init__(self, pos)
        pygame.sprite.DirtySprite.__init__(self)
        self.size = (16, 16)
        self.rect = pygame.Rect((0, 0), self.size)
        # self.image_raw, self.rect = load_image(image, -1)
        # self.image = pygame.transform.scale(self.image_raw, self.size)
        self.rect.center = (self.position.x, self.position.y)
        self.id = id
        self.life = life
        self.full = 0
        self.children = []
        self.game = game
        self.growRadius = 100
        self.child = None

    def grow(self, typeClass, plants):
        if self.canGrow(plants):
            t = 2*math.pi*random.random()
            u = random.randint(0, self.growRadius)+random.randint(0, self.growRadius)
            r = 2-u if u>1 else u
            xpos = abs(self.rect.centerx - (r*math.cos(t) / 2))
            ypos = abs(self.rect.centery - (r*math.sin(t) / 2)) 
            if xpos > GAME_SIZE[0]:
                xpos = GAME_SIZE[0] 
            if ypos > GAME_SIZE[1]:
                ypos = GAME_SIZE[1] 

            nextid = self.game.getNextId('food')
            newPlant = typeClass(nextid, (xpos, ypos), self.game)
            self.game.addEntity(newPlant, 'food')
            self.child = newPlant
    
    def update(self):
        self._update()
        
        if self.life <= 0:
            self.kill()
            self.game.removeEntity(self, 'food')
        
    def draw(self, screen):
        if self.selected:
            pygame.draw.rect(screen, RED, self.rect, 2)
            pygame.draw.circle(screen, RED, self.rect.center, self.growRadius,  1)
            if self.child:
                pygame.draw.aaline(screen, RED, self.rect.center, self.child.rect.center)
        self._draw(screen)

    def canGrow(self, plants):
        if not self.child or not self.child.alive:
            allow = []

            for p in plants:
                if (p.rect.centerx - self.rect.centerx)**2 + \
                   (p.rect.centery - self.rect.centery)**2 \
                   <= self.growRadius**2:
                   allow.append(p)

            return len(allow) >= 0 and len(allow) <= 3

    
