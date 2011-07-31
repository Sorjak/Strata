import pygame, random, os, sys, re, math
from time import time
from pygame.locals import *
from utils_strata import *

# drag = 0.999
# elasticity = 0.7
# gravity = (math.pi, 0.002)
drag = 1
elasticity = 1
gravity = (math.pi, 0)

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
    

class Particle(object):
    def __init__(self):
        random.seed()
        self.x = random.randint(0, WINDOW_SIZE[0])
        self.y = random.randint(0, WINDOW_SIZE[1])
        self.angle = random.uniform(0, math.pi*2)
        self.speed = random.random()
    
    def move(self):
        # self.speed *= drag
        (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.bounce()
    
    def bounce(self):
        width = WINDOW_SIZE[0]
        height = WINDOW_SIZE[1]
        if self.x >= width - self.rect.size[0]:
            self.angle = 2*math.pi - self.angle
            self.x = width - self.rect.size[0]
            self.speed *= elasticity
        elif self.x <= 0:
            self.angle = 2*math.pi - self.angle
            self.x = 1
            self.speed *= elasticity

        if self.y >= height - self.rect.size[1]:
            self.angle = math.pi - self.angle
            self.y = height - self.rect.size[1]
            self.speed *= elasticity
        elif self.y <= 0:
            self.angle = math.pi - self.angle
            self.y = 1
            self.speed *= elasticity

class Creep(Particle, pygame.sprite.DirtySprite):
    def __init__(self, id):
        pygame.sprite.DirtySprite.__init__(self)
        Particle.__init__(self)
        self.image_raw, self.rect = load_image("creep" + str(random.randint(1, 2)) + ".png", -1)
        self.image = pygame.transform.scale(self.image_raw, (15, 15))
        self.rect.size = (15, 15)
        self.rect.topleft = (self.x, self.y)
        rndcolor = random.randint(1, 254)
        self.color = (rndcolor, rndcolor, rndcolor)
        self.id = id
        self.kills = 0
        self.selected = False
    
    def update(self):
        self.move()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw(self, screen):
        if self.selected:
            pygame.draw.rect(screen, RED, self.rect, 2)
        else:
            pygame.draw.rect(screen, BLUE, self.rect, 2)
        # screen.blit(self.image, self.rect)
    
        
    def grow(self, kills = 1):
        self.kills += kills
        grow_factor = (self.kills + 1) * 15
        self.image = pygame.transform.scale(self.image_raw, (grow_factor, grow_factor))
        self.rect.size = (grow_factor, grow_factor)
        
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
        mini = (None, 99999)
        for e in enemies:
            dto_topleft = hypot(e.rect.topleft[0] - self.rect.center[0], e.rect.topleft[1] - self.rect.center[1])
            dto_topright = hypot(e.rect.topright[0] - self.rect.center[0], e.rect.topright[1] - self.rect.center[1])
            dto_bottomleft = hypot(e.rect.bottomleft[0] - self.rect.center[0], e.rect.bottomleft[1] - self.rect.center[1])
            dto_bottomright = hypot(e.rect.bottomright[0] - self.rect.center[0], e.rect.bottomright[1] - self.rect.center[1])
            
            distance = min(dto_topleft, dto_topright, dto_bottomleft, dto_bottomright)

            if distance < mini[1]:
                mini = (e, distance)
                
        return mini[0]

class MapSquare(object):
    def __init__(self):
        self.terrain = "normal"
        self.image, self.rect = load_image("grass.jpg")
        