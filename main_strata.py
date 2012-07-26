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
NUM_HUNTERS = 6

SCROLL_SPEED = 6
GAME_TITLE = 'Strata %sx%s' % WINDOW_SIZE
MOVE_KEYS = (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT,
            pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a)

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
        self.entities = None
        
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
        while(worldgenthread.isAlive()):
            clock.tick(5)
            screen.fill(BLACK)
            numdots = random.randint(1, 5)
            screen.blit(font.render("Loading the map%s" % ("." * numdots), 1, WHITE), ((WINDOW_SIZE[0] /2) - 100, WINDOW_SIZE[1]/2))
            pygame.display.flip()
        return map
        
    def initEntities(self):
        self.cm = CreepManager(self, NUM_CREEPS)
        
        
        self.pm = PlantManager(self, NUM_FOOD)
        
        
        self.hm = HunterManager(self, NUM_HUNTERS)
        
        self.cm.seed()
        self.pm.seed()
        self.hm.seed()
        
        # self.entities = pygame.sprite.RenderUpdates(self.creeps, self.hunters, self.food)
        # self.entities.add(self.pm)
        self.entities = [self.hm, self.pm, self.cm]
        
    def main(self):
        random.seed()
        
        #init objects
        self.initEntities()
        self.mousepos = self.getRelativeMousePos()
        
        #main loop
        while self.running:
            eventsthread = threading.Thread(target=self.userEvents())
            eventsthread.start()
            
            self.clock.tick(60)
            
            self.map.rect.topleft = (self.mapDX, self.mapDY)
            

            if not self.paused:
                self.startDaemons()
                updatethread = threading.Thread(target=self.update())
                updatethread.start()
                renderthread = threading.Thread(target=self.render())
                renderthread.start()
                
            self.drawInfo()
            if self.mousepos:
                font = pygame.font.Font(None, 14)
                self.screen.blit(font.render("Mouse Position : %s, %s" % (self.mousepos[0], self.mousepos[1]), 1, WHITE), (0, WINDOW_SIZE[1] + 29))


            #check for game over
            if len(self.creeps) == 0:
                running = False
            
            #wait for threads
            
            while renderthread.isAlive() or updatethread.isAlive():
                pass
            
            pygame.display.flip()

        self.stopDaemons()
        self.gameOver(self.screen)
        
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
                self.stopDaemons()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    self.stopDaemons()
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
                            collision.selected = True
                            self.selected = collision
                            break
                elif event.button == 3:
                    pass
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
        
    def startDaemons(self):
        for t in self.timers:
            if not t.isRunning():
                t.startTimer()
            
    def stopDaemons(self):
        for t in self.timers:
            t.stopTimer()
        
    #Function set on a timer to spawn more hunters if they die out    
    def spawnHunters(self):
        if len(self.hunters) <= 0:
            print "no more hunters!"
          
    def spawnFood(self):
        if len(self.food) < (NUM_CREEPS / 4) :
            newfood = Cherry(len(self.food) + 1, None, self)
            self.food.add(newfood)
            self.entities.add(newfood)
    
# util functions
            
    def gameOver(self, screen):
        font = pygame.font.Font(None, 50)
        self.screen.blit(font.render("GAME OVER", 1, RED), ((WINDOW_SIZE[0] /2) - 100, WINDOW_SIZE[1]/2))
        pygame.display.update()
        pygame.time.delay(3000)

    def drawInfo(self):
        numcreeps = len(self.cm)
        numhunters = len(self.hm)
        numfood = len(self.pm)
        mappos = self.map.rect.topleft
        self.screen.fill(BLACK, pygame.Rect((0, WINDOW_SIZE[1]), (WINDOW_SIZE[0], WINDOW_SIZE[1])))
        pygame.draw.line(self.screen, WHITE, (0, WINDOW_SIZE[1]), (WINDOW_SIZE[0], WINDOW_SIZE[1]))
        font = pygame.font.Font(None, 14)
        self.screen.blit(font.render("FPS: %s | Creeps: %s | Hunters: %s | Food: %s | Map Position : %s" % \
                        (int(self.clock.get_fps()), numcreeps, numhunters, numfood, mappos), 1, WHITE), (0, WINDOW_SIZE[1] + 7))
                        
        if self.selected and type(self.selected) is Creep or type(self.selected) is Hunter:
            self.screen.blit(font.render("Selected entity: %s | Looking for food?: %s, Speed Modifier: %s | Speed: %s, Life: %s, Full: %s | Direction: %s | Position: %s" % \
                        (self.selected.id, self.selected.searching, round(self.selected.speedmod, 3), round(self.selected.speed, 1), round(self.selected.life, 1), round(self.selected.full, 1), self.selected.direction, self.selected.position), \
                        1, WHITE), (0, WINDOW_SIZE[1] + 18))
                        
        if self.selected and type(self.selected) is Cherry:
            self.screen.blit(font.render("Selected entity: %s | Value: %s | Grazers: %s" % \
                        (self.selected.id, round(self.selected.life, 2), len(self.selected.grazers)), 1, WHITE), (0, WINDOW_SIZE[1] + 18))
    
    def getRelativeMousePos(self):
        mpos = pygame.mouse.get_pos()
        output = (mpos[0] - self.mapDX, mpos[1] - self.mapDY)
        return output
    
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
