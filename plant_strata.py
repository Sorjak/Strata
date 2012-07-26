import pygame, random, math
from pygame.locals import *
from pygame.sprite import DirtySprite
from utils_strata import *
from globals_strata import *
from basic_objects_strata import Particle

class Plant(Particle, pygame.sprite.DirtySprite):
    def __init__(self, id, image, pos, game, life):
        Particle.__init__(self, pos, 0)
        pygame.sprite.DirtySprite.__init__(self)
        self.size = (20, 20)
        self.image_raw, self.rect = load_image(image, -1)
        self.image = pygame.transform.scale(self.image_raw, self.size)
        self.rect.size = self.size
        self.rect.center = (self.position.x, self.position.y)
        self.id = id
        self.life = life
        self.full = 0
        self.children = []
        self.game = game
        # self.spawn(map)
        
    def spawn(self, map):
        r = random.randint(1, 10)
        pass
    
    def update(self):
        self._update()
        

        if self.life <= 0:
            self.kill()
        
    def draw(self, screen):
        self._draw(screen)
    
        if self.selected:
            pygame.draw.rect(screen, RED, self.rect, 2)

        screen.blit(self.image, self.rect)
        
    def _update(self):
        pass
    
    def _draw(self):
        pass
    
