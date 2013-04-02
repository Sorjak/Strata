import os, sys, pygame, random, threading
from pygame.locals import *
from creep_strata import Creep
from hunter_strata import Hunter
from cherry_strata import Cherry
from utils_strata import *
from maps_strata import Map
from group_strata import StrataGroup
from managers_strata import *

# from globals_strata import *
# from pygame.examples.mask import Sprite

NUM_CREEPS = 50
NUM_FOOD = 10
NUM_PREDS = 6

SCROLL_SPEED = 6
GAME_TITLE = 'Strata %sx%s' % WINDOW_SIZE
MOVE_KEYS = (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT,
            pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a)

PLANT_GROWTH = pygame.USEREVENT+1

class StrataGame(object):
    def __init__(self, screen, bg, clock):
        self.running = True
        self.paused = False
        
        self.screen = screen
        self.bg = bg
        self.clock = clock
        self.map = self.initMap(screen, clock)
        self.mapDX = self.mapDY = 0
        self.creeps = StrataGroup("Creeps")
        self.food = StrataGroup("Food")
        self.hunters = StrataGroup("Hunters")
        self.entities = []
        self.oEntities = {}
        
        # self.timers = [RepeatTimer(5.0, self.spawnHunters), RepeatTimer(5.0, self.spawnFood)]
        self.timers = []
        self.selected = None
        self.mousepos = None
        self.cm = self.hm = self.pm = None
        
        
    def initMap(self, screen, clock):
        map = Map(WORLD_SIZE)
        map.convert()
        worldgenthread = threading.Thread(target=map.generateWorld)
        worldgenthread.start()
        
        font = pygame.font.Font(None, 24)
        numdots = 0
        while(worldgenthread.isAlive()):
            clock.tick(5)
            screen.fill(BLACK)
            numdots += 1
            screen.blit(font.render("Loading the map%s" % ("." * (numdots % 5)), 1, WHITE), ((WINDOW_SIZE[0] /2) - 100, WINDOW_SIZE[1]/2))
            pygame.display.flip()
        return map
        
    def initEntities(self):
        self.oEntities['food'] = []
        self.oEntities['creeps'] = []
        self.oEntities['preds'] = []

        for p in range(0, NUM_FOOD):
            x = random.randint(0, GAME_SIZE[0])
            y = random.randint(0, GAME_SIZE[1])
            cherry = Cherry(p, (x, y), self)
            self.addEntity(cherry, 'food')


        for c in range(0, NUM_CREEPS):
            x = random.randint(0, GAME_SIZE[0])
            y = random.randint(0, GAME_SIZE[1])
            creep = Creep(1000 + c, self, None, None)
            self.addEntity(creep, 'creeps')

        for h in range(0, NUM_PREDS):
            x = random.randint(0, GAME_SIZE[0])
            y = random.randint(0, GAME_SIZE[1])
            hunter = Hunter(2000 + h, self, None, None)
            self.addEntity(hunter, 'preds')
        
        # self.entities = pygame.sprite.RenderUpdates(self.creeps, self.hunters, self.food)
        # self.entities.add(self.pm)

    def initTimers(self):
        pygame.time.set_timer(PLANT_GROWTH, 5000)          #plant growth timer
        
    def main(self):
        random.seed()
        
        #init objects
        self.initEntities()
        self.initTimers()
        self.mousepos = self.getRelativeMousePos()
        
        #main loop
        while self.running:
            eventsthread = threading.Thread(target=self.userEvents())
            eventsthread.start()
            
            self.clock.tick(60)
            
            self.map.rect.topleft = (self.mapDX, self.mapDY)
            
            self.screen.blit(self.bg, (0, 0))
            if not self.paused:
                updatethread = threading.Thread(target=self.update())
                updatethread.start()
                renderthread = threading.Thread(target=self.render())
                renderthread.start()
                
            self.drawInfo()
            if self.mousepos:
                font = pygame.font.Font(None, 14)
                self.screen.blit(font.render("Mouse Position : %s, %s" % (self.mousepos[0], self.mousepos[1]), 1, WHITE), (0, WINDOW_SIZE[1] + 29))


            #check for game over
            if len(self.entities) == 0:
                self.running = False
            
            #wait for threads
            
            while renderthread.isAlive() or updatethread.isAlive():
                pass
            
            pygame.display.flip()

        sys.exit(0)
        
    def render(self):
        self.map.draw(self.screen)
        for e in self.entities:
            e.draw(self.map)
        
    def update(self):
        for e in self.entities:
            e.update()
            
    def userEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = 0
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    self.running= 0
                elif event.key == K_p:
                    self.paused = not self.paused
            elif event.type == pygame.MOUSEBUTTONDOWN:
                event.pos = (event.pos[0] - self.mapDX, event.pos[1] - self.mapDY)
                if event.button == 1:
                    if self.selected:
                        self.selected.selected = False
                    self.selected = None
                    for e in self.entities:
                        collision = e.collidesWith(event.pos)
                        if collision:
                            e.selected = True
                            self.selected = e
                            break
                elif event.button == 3:
                    pass
            elif event.type == PLANT_GROWTH:
                plants = [p for p in self.entities if type(p) is Cherry]
                for p in plants:
                    p.grow(plants)
            else:
                pygame.event.pump()
        temp = pygame.key.get_repeat()
        pygame.key.set_repeat(1, 1)
        key=pygame.key.get_pressed()
        if key[K_LEFT] or key[K_a]:
            if self.mapDX >= 0:
                self.mapDX = 0
            else:
                self.mapDX += SCROLL_SPEED
        if key[K_RIGHT] or key[K_d]:
            if self.mapDX <= -(WORLD_SIZE[0] - WINDOW_SIZE[0]):
                self.mapDX = -(WORLD_SIZE[0] - WINDOW_SIZE[0])
            else:
                self.mapDX -= SCROLL_SPEED
        if key[K_UP] or key[K_w]:
            if self.mapDY >= 0:
                self.mapDY = 0
            else:
                self.mapDY += SCROLL_SPEED
        if key[K_DOWN] or key[K_s]:
            if self.mapDY <= -(WORLD_SIZE[1] - WINDOW_SIZE[1]):
                self.mapDY = -(WORLD_SIZE[1] - WINDOW_SIZE[1])
            else:
                self.mapDY -= SCROLL_SPEED
        pygame.key.set_repeat(temp[0], temp[1])
        self.mousepos = self.getRelativeMousePos()
    
    # util functions

    def drawInfo(self):
        numentities = len(self.entities)
        mappos = self.map.rect.topleft
        self.screen.fill(BLACK, pygame.Rect((0, WINDOW_SIZE[1]), (WINDOW_SIZE[0], WINDOW_SIZE[1])))
        pygame.draw.line(self.screen, WHITE, (0, WINDOW_SIZE[1]), (WINDOW_SIZE[0], WINDOW_SIZE[1]))
        font = pygame.font.Font(None, 14)
        self.screen.blit(font.render("FPS: %s | Entities: %s | Map Position : %s" % \
                        (int(self.clock.get_fps()), numentities, mappos), 1, WHITE), (0, WINDOW_SIZE[1] + 7))
                        
        if self.selected and type(self.selected) is Creep or type(self.selected) is Hunter:
            self.screen.blit(font.render("Eating?: %s | Looking for food?: %s, Speed Modifier: %s | Speed: %s, Life: %s, Full: %s | Direction: %s | Position: %s" % \
                        (self.selected.eating, self.selected.nearestFood, round(self.selected.speedmod, 3), round(self.selected.speed, 1), round(self.selected.life, 1), round(self.selected.full, 1), self.selected.direction, self.selected.position), \
                        1, WHITE), (0, WINDOW_SIZE[1] + 18))
                        
        if self.selected and type(self.selected) is Cherry:
            self.screen.blit(font.render("Selected entity: %s | Value: %s | Grazers: %s" % \
                        (self.selected.id, round(self.selected.life, 2), len(self.selected.grazers)), 1, WHITE), (0, WINDOW_SIZE[1] + 18))
    
    def getRelativeMousePos(self):
        mpos = pygame.mouse.get_pos()
        output = (mpos[0] - self.mapDX, mpos[1] - self.mapDY)
        return output

    def addEntity(self, e, eType):
        self.entities.append(e)
        self.oEntities[eType].append(e)

    def removeEntity(self, obj, eType):
        self.entities[:] = [x for x in self.entities if x is not obj]
        self.oEntities[eType][:] = [x for x in self.oEntities[eType] if x is not obj]

    def getNextId(self, eType):
        return len(self.oEntities[eType]) + 1
    
def initialize():
    adjust_to_correct_appdir()
    pygame.init()
    
    full_window = (WINDOW_SIZE[0], WINDOW_SIZE[1] + 50)
    screen = pygame.display.set_mode(full_window)
    pygame.display.set_caption(GAME_TITLE)

    return screen


if __name__ == '__main__':
    screen = initialize()
    bg = pygame.Surface((WINDOW_SIZE[0], 50))
    bg.convert()
    bg.fill(BLACK)
    clock = pygame.time.Clock()
    mGame = StrataGame(screen, bg, clock)
    mGame.main()
