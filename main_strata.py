import os, sys, pygame, random, threading
from pygame.locals import *
from creep_strata import Creep
from hunter_strata import Hunter
from food_strata import Cherry
from utils_strata import *
from maps_strata import Map
from group_strata import StrataGroup

# from globals_strata import *
# from pygame.examples.mask import Sprite

class StrataGame(object):
    def __init__(self, screen, bg, clock):
        self.running = True
        self.entities = []
        self.screen = screen
        self.bg = bg
        self.clock = clock
        self.map = self.initMap(screen, clock)
        self.mapDX = self.mapDY = 0
        self.creeps = StrataGroup("Creeps")
        self.food = StrataGroup("Food")
        self.hunters = StrataGroup("Hunters")
        self.timers = []
        self.entities = None
        self.selected = None
        
        
    def initMap(self, screen, clock):
        map = Map(WORLD_SIZE)
        map.convert()
        # map.generateWorld()
        worldgenthread = threading.Thread(target=map.generateWorld)
        worldgenthread.start()
        #end map stuff
        font = pygame.font.Font(None, 24)
        while(worldgenthread.isAlive()):
            clock.tick(5)
            screen.fill(BLACK)
            numdots = random.randint(1, 5)
            screen.blit(font.render("Loading the map%s" % ("." * numdots), 1, WHITE), ((WINDOW_SIZE[0] /2) - 100, WINDOW_SIZE[1]/2))
            pygame.display.flip()
        return map
        
    def initEntities(self):
        for i in range(0, random.randint(NUM_CREEPS / 2 , NUM_CREEPS)-1):
            self.creeps.add(Creep(i, self, None, None))
        
        
        for i in range(0, random.randint(NUM_FOOD /2 , NUM_FOOD) - 1):
            self.food.add(Cherry(i, None, self.map))
        
        
        for i in range(0, random.randint(3, 6)):
            self.hunters.add(Hunter(i, self, None, None, life=25.0))
        
        
    def main(self):
        random.seed()
        #map stuff
        
        #init objects
        self.initEntities()

        self.timers = [RepeatTimer(5.0, self.spawnHunters), RepeatTimer(5.0, self.spawnFood)]
        
        self.entities = pygame.sprite.RenderUpdates(self.creeps, self.hunters, self.food)
        # allhunters = pygame.sprite.RenderPlain(hunters)
        #end init objects
        
        mousepos = False
        #main loop
        while self.running:
            #Listen for user events ######################################################
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = 0
                    self.stopDaemons()
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_q:
                        self.stopDaemons()
                        self.running= 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    event.pos = (event.pos[0] - self.mapDX, event.pos[1] - self.mapDY)
                    if event.button == 1:
                        if self.selected:
                            self.selected.selected = False
                        self.selected = None
                        for e in self.entities:
                            if e.rect.collidepoint(event.pos):
                                e.selected = True
                                self.selected = e
                                break
                    elif event.button == 3:
                        mousepos = event.pos
                else:
                    pygame.event.pump()

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
            #End event listening #########################################################
                        
            self.clock.tick(60)
            self.map.rect.topleft = (self.mapDX, self.mapDY)
            self.map.draw(self.screen)
            self.startDaemons()
            
            
            #Entity updates

            for e in self.creeps:
                if mousepos:
                    e.mouseEvent(mousepos)
                e.checkDanger(self.hunters)
                e.update()
                e.draw(self.map)
            
                
            for h in self.hunters:
                if mousepos:
                    h.mouseEvent(mousepos)
                h.update()
                h.draw(self.map)

            for f in self.food:
                f.update()
                f.checkGrazers(self.creeps)
                f.draw(self.map)
                
            #End Entity Updates    
            
            self.drawInfo(self.screen, self.bg, self.clock.get_fps())
            if mousepos:
                font = pygame.font.Font(None, 14)
                self.screen.blit(font.render("Mouse Position : %s, %s" % (mousepos[0], mousepos[1]), 1, WHITE), (0, WINDOW_SIZE[1] + 29))
            # entities.draw(map)
            #check for game over
            if len(self.creeps) == 0:
                running = False
            
            pygame.display.flip()
            
            
            
            

        self.stopDaemons()
        self.gameOver(self.screen)
        
    def render(self):
        pass
        
    def update(self):
        pass
        
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
            newfood = Cherry(len(self.food) + 1, None, map)
            self.food.add(newfood)
            self.entities.add(newfood)
            print "added more food!"
    
# util functions
            
    def gameOver(self, screen):
        font = pygame.font.Font(None, 50)
        self.screen.blit(font.render("GAME OVER", 1, RED), ((WINDOW_SIZE[0] /2) - 100, WINDOW_SIZE[1]/2))
        pygame.display.update()
        pygame.time.delay(3000)

    def drawInfo(self, screen, bg, fps):
        numcreeps = len(self.creeps.sprites())
        numhunters = len(self.hunters.sprites())
        mappos = self.map.rect.topleft
        self.screen.blit(bg, (0, WINDOW_SIZE[1]))
        pygame.draw.line(self.screen, WHITE, (0, WINDOW_SIZE[1]), (WINDOW_SIZE[0], WINDOW_SIZE[1]))
        font = pygame.font.Font(None, 14)
        self.screen.blit(font.render("FPS: %s | Creeps: %s | Hunters: %s | Map Position : %s" % \
                        (int(fps), numcreeps, numhunters, mappos), 1, WHITE), (0, WINDOW_SIZE[1] + 7))
                        
        if self.selected and type(self.selected) is Creep or type(self.selected) is Hunter:
            self.screen.blit(font.render("Selected entity: %s | Looking for food?: %s, Speed Modifier: %s | Speed: %s, Life: %s, Full: %s | Direction: %s | Position: %s" % \
                        (self.selected.id, self.selected.searching, round(self.selected.speedmod, 3), round(self.selected.speed, 1), round(self.selected.life, 1), round(self.selected.full, 1), self.selected.direction, self.selected.position), \
                        1, WHITE), (0, WINDOW_SIZE[1] + 18))
                        
        if self.selected and type(self.selected) is Cherry:
            self.screen.blit(font.render("Selected entity: %s | Value: %s | Grazers: %s" % \
                        (self.selected.id, round(self.selected.life, 2), len(self.selected.grazers)), 1, WHITE), (0, WINDOW_SIZE[1] + 18))

def initialize():
    adjust_to_correct_appdir()
    pygame.init()
    pygame.key.set_repeat(1, 1)
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
    timers = []
    random.seed()
    mGame = StrataGame(screen, bg, clock)
    mGame.main()
