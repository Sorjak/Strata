import os, sys, pygame, random, threading
from pygame.locals import *
from creep_strata import Creep
from hunter_strata import Hunter
from food_strata import Cherry
from utils_strata import *
from maps_strata import Map

from globals_strata import *
from pygame.examples.mask import Sprite

class StrataGame(object):
    def __init__(self, self.screen, bg, clock):
        self.running = True
        self.entities = []
        self.screen = self.screen
        self.bg = bg
        self.clock = clock
        
    def main(self):
        #map stuff
        mapDX = mapDY = 0
        map = Map(WORLD_SIZE)
        map.convert()
        # map.generateWorld()
        worldgenthread = threading.Thread(target=map.generateWorld)
        worldgenthread.start()
        #end map stuff
        font = pygame.font.Font(None, 24)
        while(worldgenthread.isAlive()):
            clock.tick(5)
            self.screen.fill(BLACK)
            numdots = random.randint(1, 5)
            self.screen.blit(font.render("Loading the map%s" % ("." * numdots), 1, WHITE), ((WINDOW_SIZE[0] /2) - 100, WINDOW_SIZE[1]/2))
            pygame.display.flip()

        #init objects
        creeps = StrataGroup("Creeps")
        for i in range(0, random.randint(NUM_CREEPS / 2 , NUM_CREEPS)-1):
            creeps.add(Creep(i, map, None, None))
        
        food = StrataGroup("Food")
        for i in range(0, random.randint(NUM_FOOD /2 , NUM_FOOD) - 1):
            food.add(Cherry(i, None, map))
        
        hunters = StrataGroup("Hunters")
        for i in range(0, random.randint(3, 6)):
            hunters.add(Hunter(i, map, None, None, life=25.0))
        timers = [RepeatTimer(5.0, self.spawnHunters, hunters), RepeatTimer(5.0, self.spawnFood, food)]
        
        
        self.entities = pygame.sprite.RenderUpdates(creeps, hunters, food)
        # allhunters = pygame.sprite.RenderPlain(hunters)
        #end init objects
        
        selected = None
        mousepos = False
        #main loop
        while self.running:
            #Listen for user events ######################################################
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = 0
                    self.stopDaemons(timers)
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_q:
                        self.stopDaemons(timers)
                        self.running= 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    event.pos = (event.pos[0] - mapDX, event.pos[1] - mapDY)
                    if event.button == 1:
                        self.clearSelections(selected)
                        selected = None
                        for e in self.entities:
                            if e.rect.collidepoint(event.pos):
                                print e
                                e.selected = True
                                selected = e
                                break
                    elif event.button == 3:
                        mousepos = event.pos
                else:
                    pygame.event.pump()

            key=pygame.key.get_pressed()
            if key[K_LEFT] or key[K_a]:
                if mapDX >= 0:
                    mapDX = 0
                else:
                    mapDX += SCROLL_SPEED
            if key[K_RIGHT] or key[K_d]:
                if mapDX <= -(WORLD_SIZE[0] - WINDOW_SIZE[0]):
                    mapDX = -(WORLD_SIZE[0] - WINDOW_SIZE[0])
                else:
                    mapDX -= SCROLL_SPEED
            if key[K_UP] or key[K_w]:
                if mapDY >= 0:
                    mapDY = 0
                else:
                    mapDY += SCROLL_SPEED
            if key[K_DOWN] or key[K_s]:
                if mapDY <= -(WORLD_SIZE[1] - WINDOW_SIZE[1]):
                    mapDY = -(WORLD_SIZE[1] - WINDOW_SIZE[1])
                else:
                    mapDY -= SCROLL_SPEED
            #End event listening #########################################################
                        
            clock.tick(60)
            map.rect.topleft = (mapDX, mapDY)
            map.draw(self.screen)
            self.startDaemons(timers)
            
            
            #Entity updates
            for e in creeps:
                if mousepos:
                    e.mouseEvent(mousepos)
                e.checkDanger(hunters)
                e.update(food)
                e.draw(map)

                
            for h in hunters:
                if mousepos:
                    h.mouseEvent(mousepos)
                h.update(creeps)
                h.draw(map)

            for f in food:
                f.update()
                f.checkGrazers(creeps)
                f.draw(map)
                
            #End Entity Updates    
            
            drawInfo(self.screen, bg, clock.get_fps(), len(creeps.sprites()), len(hunters.sprites()), selected, map.rect.topleft)
            if mousepos:
                font = pygame.font.Font(None, 14)
                self.screen.blit(font.render("Mouse Position : %s, %s" % (mousepos[0], mousepos[1]), 1, WHITE), (0, WINDOW_SIZE[1] + 29))
            # entities.draw(map)
            #check for game over
            if len(creeps) == 0:
                running = False
            
            pygame.display.flip()
            
            
            
            

        self.stopDaemons(timers)
        self.gameOver(self.screen)
        
    def startDaemons(self, timers):
        for t in timers:
            if not t.isRunning():
                t.startTimer()
            
    def stopDaemons(self, timers):
        for t in timers:
            t.stopTimer()
        
    #Function set on a timer to spawn more hunters if they die out    
    def spawnHunters(self, hunters):
        if len(hunters) <= 0:
            print "no more hunters!"
          
    def spawnFood(self, food):
        if len(food) < (NUM_CREEPS / 4) :
            newfood = Cherry(len(food) + 1, None, map)
            food.add(newfood)
            self.entities.add(newfood)
    
# util functions
    def clearSelections(self, sel):
        if sel:
            sel.selected = False
            
    def gameOver(self, self.screen):
        font = pygame.font.Font(None, 50)
        self.screen.blit(font.render("GAME OVER", 1, RED), ((WINDOW_SIZE[0] /2) - 100, WINDOW_SIZE[1]/2))
        pygame.display.update()
        pygame.time.delay(3000)
                
# def handleTextInput(st, font):
    # if re.match(r"ask\s(?P<words>.*?)\sfen", st):
        # textcolor = RED
        # inspell = True
    # else:
        # textcolor = WHITE
        # inspell = False
    # message = font.render("Say: %s" % "".join(st), 1, textcolor)
    # return (message, inspell)

def drawInfo(self.screen, bg, fps, numcreeps, numhunters, selected, mappos):
    self.screen.blit(bg, (0, WINDOW_SIZE[1]))
    pygame.draw.line(self.screen, WHITE, (0, WINDOW_SIZE[1]), (WINDOW_SIZE[0], WINDOW_SIZE[1]))
    font = pygame.font.Font(None, 14)
    self.screen.blit(font.render("FPS: %s | Creeps: %s | Hunters: %s | Map Position : %s" % \
                    (int(fps), numcreeps, numhunters, mappos), 1, WHITE), (0, WINDOW_SIZE[1] + 7))
                    
    if selected and type(selected) is Creep or type(selected) is Hunter:
        self.screen.blit(font.render("Selected entity: %s | Looking for food?: %s, Speed Modifier: %s | Speed: %s, Life: %s, Full: %s | Direction: %s | Position: %s" % \
                    (selected.id, selected.searching, round(selected.speedmod, 3), round(selected.speed, 1), round(selected.life, 1), round(selected.full, 1), selected.direction, selected.position), \
                    1, WHITE), (0, WINDOW_SIZE[1] + 18))
                    
    if selected and type(selected) is Cherry:
        self.screen.blit(font.render("Selected entity: %s | Value: %s | Grazers: %s" % \
                    (selected.id, round(selected.life, 2), len(selected.grazers)), 1, WHITE), (0, WINDOW_SIZE[1] + 18))

def initialize():
    adjust_to_correct_appdir()
    pygame.init()
    pygame.key.set_repeat(1, 1)
    random.seed()
    full_window = (WINDOW_SIZE[0], WINDOW_SIZE[1] + 50)
    self.screen = pygame.display.set_mode(full_window)
    pygame.display.set_caption(GAME_TITLE)

    return self.screen


if __name__ == '__main__':
    self.screen = initialize()
    bg = pygame.Surface((WINDOW_SIZE[0], 50))
    bg.convert()
    bg.fill(BLACK)
    clock = pygame.time.Clock()
    timers = []
    random.seed()
    mGame = StrataGame(self.screen, bg, clock)
    mGame.main()
