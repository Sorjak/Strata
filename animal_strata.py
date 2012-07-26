import pygame, random, math
from pygame.locals import *
from pygame.sprite import DirtySprite, RenderPlain
from basic_objects_strata import Particle
from utils_strata import *

try:
    from pygame.math import Vector2
except ImportError:
    from math_strata import Vector2

class Animal(Particle, pygame.sprite.DirtySprite):
    def __init__(self, id, image, pos, speed, life, range, predators, prey):
        Particle.__init__(self, pos, speed)
        pygame.sprite.DirtySprite.__init__(self)
        self.size = (15, 15)
        self.image_raw, self.rect = load_image(image, -1)
        self.image = pygame.transform.scale(self.image_raw, self.size)
        self.rect.size = self.size
        self.rect.center = (self.position.x, self.position.y)
        self.id = id
        self.life = life
        self.full = 0
        self.range = range
        self.children = []
        self.selected = False
        self.searching = False
        self.nearestFood = None
        self.speedmod = None
        self.predators = predators
        self.prey = prey
        self.dirty = 0
        
    def update(self):
        self.life -= ANIMAL_DECAY
        self.speed = (self.life * self.speedmod) * .01
    
        self._update()
        
        self.search(self.prey)
        temp = self.position
        self.move()
        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y
        
        if temp != self.position:
            self.dirty = 1
        
        if self.full >= 100:
            self._grow()
            self.full = 0
        
        if self.life <= 0:
            self.kill()

        
    def draw(self, screen):
        self._draw(screen)
    
        if self.selected:
            pygame.draw.rect(screen, RED, self.rect, 2)
            pygame.draw.circle(screen, RED, self.rect.center, self.range, 1)
        displacement = Vector2(self.direction.x * (self.speed * 30), self.direction.y * (self.speed * 30))
        
        if self.searching:
            pygame.draw.line(screen, WHITE, self.rect.center, self.nearestFood.position)
        else:
            pygame.draw.line(screen, WHITE, self.rect.center, self.position + displacement)
        screen.blit(self.image, self.rect)
        self.dirty = 0
        
    def search(self, food):
        self.nearestFood = self._findNearestEntity(food)
        
        self.searching = self.nearestFood is not None
        
        if self.searching:
            self._foundFood(self.nearestFood)

        
        self._search(food)
                
    def _update(self):
        pass
    
    def _draw(self):
        pass
    
    def _foundFood(self, nFood):
        pass
        
    def _grow(self):
        pass
            
    def _findNearestEntity(self, entities):
        mini = (None, MAX_INT)
        for e in entities:
            distance = math.sqrt(((self.position.x - e.position.x) ** 2) + ((self.position.y - e.position.y) ** 2))
            
            if distance < mini[1]:
                mini = (e, distance)  
        if mini[1] < self.range:
            return mini[0]
        else:
            return None
    def _grow(self):
        pass
    