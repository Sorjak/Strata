import pygame, random, os, sys, re, math
from time import time
from pygame.locals import *
from utils_strata import *
from basic_objects_strata import *

# drag = 0.999
# elasticity = 0.7
# gravity = (math.pi, 0.002)


class Player(pygame.sprite.DirtySprite):
    def __init__(self, power):
        pygame.sprite.DirtySprite.__init__(self)
        self.image, self.rect = load_image("playericon.png", -1)
        self.rect.topleft = 5, WINDOW_SIZE[1] - self.rect.height - 1
        self.move_amount = 2
        self.x, self.y = self.rect.topleft
        self.typemode = self.showaoe = False
        self.shielding = True
        self.jumping = 0
        self.AOE = power * 20
        self.spellhistory = []
    
    def update(self):
        if self.jumping > 0:
            self.jumping -= 1
            self.rect = self.rect.move(0, -self.move_amount)
        else:
            self.rect = self.rect.move(0, 0.5)
    
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_SIZE[0]:
            self.rect.right = WINDOW_SIZE[0]
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_SIZE[1]:
            self.rect.bottom = WINDOW_SIZE[1]
    
    def draw(self, screen):
        if self.showaoe:
            pygame.draw.circle(screen, RED, self.rect.center, self.AOE, 1)
        if self.shielding:
            pos = self.rect.center
            pygame.draw.circle(screen, BLUE, pos, self.rect.width/2, 1)
        screen.blit(self.image, self.rect)
    
    def move(self, keys, invol=(False,0,0)):
        if invol[0]:
            self.rect = self.rect.move(amount)
            return
            
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect = self.rect.move(0, -self.move_amount)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            pass
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect = self.rect.move(self.move_amount, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect = self.rect.move(-self.move_amount, 0)
            
    def handleInput(self, phrase, enemies):
        words = re.findall(r"ask\s(?P<words>.*?)\sfen", phrase)
        einr = self._enemiesInRange(enemies)
        success = False
        if "fire" in words:
            for e in einr:
                e.kill()
                del e
            success = True
        if "freeze" in words:
            for e in einr:
                e.freeze()
            success = True
        if "showaoe" in words:
            self.showaoe = not self.showaoe
            success = True
        if "shield" in words:
            self.shielding = not self.shielding
            success = True
            
        if success:
            self.spellhistory.append(phrase)
    
    def _enemiesInRange(self, enemies):
        out = []
        for e in enemies:
            dist = math.sqrt((self.rect.centerx - e.rect.centerx) ** 2 + (self.rect.centery- e.rect.centery) ** 2)
            if dist <= self.AOE:
                out.append(e)
        return out
    


class Creep(Particle, pygame.sprite.DirtySprite):
    def __init__(self, id):
        pygame.sprite.DirtySprite.__init__(self)
        Particle.__init__(self)
        self.image_raw, self.rect = load_image("creep" + str(random.randint(1, 3)) + ".png", -1)
        self.image = pygame.transform.scale(self.image_raw, (15, 15))
        self.rect.size = (15, 15)
        self.rect.topleft = (self.x, self.y)
        rndcolor = random.randint(1, 254)
        self.color = (rndcolor, rndcolor, rndcolor)
        self.id = id
        self.growth = 0
        self.selected = False
        self.fleeing = False
        self.grazing = False
        self.nearestFood = None
    
    def update(self):
        if not self.grazing:
            self.move()
            self.rect.x = self.x
            self.rect.y = self.y
        
    def draw(self, screen):
        if self.selected:
            pygame.draw.rect(screen, RED, self.rect, 2)
        else:
            pygame.draw.rect(screen, BLUE, self.rect, 2)
        # screen.blit(self.image, self.rect)
    
    def graze(self, food):
        if not self.nearestFood:
            self.grazing = False
            self.nearestFood = self._findNearestFood(food)
        else:
            if self.rect.colliderect(self.nearestFood.rect):
                self.grazing = True
                # self.nearestFood.value = self.nearestFood.value - 1
                # self.grow()
            else:
                tempX = self.nearestFood.rect.centerx - self.rect.centerx
                tempY = self.nearestFood.rect.centery - self.rect.centery
                self.angle = degrees(atan2(tempY, tempX))
            
        
    def grow(self, amount=1):
        self.growth += amount
        self.image = pygame.transform.scale(self.image_raw, (self.growth, self.growth))
        self.rect.size = (self.growth, self.growth)
        
    def _findNearestFood(self, food):
        return findNearest(self.rect, food)
        
from math import hypot, atan2, degrees
        
class Hunter(Particle, pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        Particle.__init__(self)
        self.image, self.rect = load_image("playericon.png", -1)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect.size = (30, 30)
        self.rect.topleft = (self.x, self.y)
        rndcolor = random.randint(1, 254)
        self.color = (rndcolor, rndcolor, rndcolor)
        self.nearestEnemy = None
        self.hunting = False
        self.speed = random.uniform(.3, .6)
    
    def update(self):
        self.move()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen):
            
        font = pygame.font.Font(None, 12)
        screen.blit(font.render("%s" % self.speed, 1, WHITE), (self.rect.left, self.rect.bottom))
        
        screen.blit(self.image, self.rect)
    
    def hunt(self, enemies):
        if not self.hunting:
            self.nearestEnemy = self._findNearestEnemy(enemies)
        if self.nearestEnemy:
            self.hunting = True
            self.nearestEnemy.selected = True
            if self.rect.colliderect(self.nearestEnemy.rect):
                self.hunting = False
                self.nearestEnemy.kill()
            else:
                tempX = self.nearestEnemy.rect.centerx - self.rect.centerx
                tempY = self.nearestEnemy.rect.centery - self.rect.centery
                self.angle = degrees(atan2(tempY, tempX))

        
            
    def _findNearestEnemy(self, enemies):
        return findNearest(self.rect, enemies)

class Food(Static, pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        Static.__init__(self)
        self.image, self.rect = load_image("grass.jpg", -1)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect.size = (20, 20)
        self.rect.topleft = (self.x, self.y)
        self.value = 25
    def update(self):
        if self.value <= 0:
            self.kill()
        

        