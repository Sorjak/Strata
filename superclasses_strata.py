import pygame, random, math
from pygame.locals import *
from pygame.sprite import DirtySprite, RenderPlain
from basic_objects_strata import Particle
from utils_strata import *

class Animal(Particle, pygame.sprite.DirtySprite):
    def __init__(self, id, image, pos, speed, life):
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
        self.children = []
        self.selected = False
        self.searching = False
        self.nearestFood = None
        
    def update(self, food):
        self._update()
        
        self.search(food)
        
        self.move()
        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y
        

        if self.life <= 0:
            self.kill()

        
    def draw(self, screen):
        self._draw(screen)
    
        if self.selected:
            pygame.draw.rect(screen, RED, self.rect, 2)
        displacement = Vector2(self.direction.x * (self.speed * 30), self.direction.y * (self.speed * 30))
        
        if self.searching:
            pygame.draw.line(screen, WHITE, self.rect.center, self.nearestFood.position)
        else:
            pygame.draw.line(screen, WHITE, self.rect.center, self.position + displacement)
        screen.blit(self.image, self.rect)
        
    def search(self, food):
        self.nearestFood = self._findNearestFood(food)
        
        self.searching = self.nearestFood is not None
        
        if self.searching:
            if self.rect.colliderect(self.nearestFood.rect):
                self._foundFood(self.nearestFood)
                self.searching = False
            else:
                self._goToPoint(self.nearestFood.position)
        
        self._search(food)
                
    def _update(self):
        pass
    
    def _draw(self):
        pass
    
    def _foundFood(self, nFood):
        pass
    
    def _findNearestFood(self, food):
        mini = (None, 99999)
        for f in food:
            distance = math.sqrt(((self.position.x - f.position.x) ** 2) + ((self.position.y - f.position.y) ** 2))
            
            if distance < mini[1]:
                mini = (f, distance)  
        if mini[1] < 200:
            return mini[0]
        else:
            return None