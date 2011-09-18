import os, sys, pygame, random
from pygame.locals import *
from objects_strata import *
from utils_strata import *
from maps_strata import Map
from pygame.examples.mask import Sprite

def main():
    screen = initialize()
    bg = pygame.Surface((WINDOW_SIZE[0], 50))
    bg.convert()
    bg.fill(BLACK)
    clock = pygame.time.Clock()
    running = 1
    random.seed()
    font = pygame.font.Font(None, 24)
    
    #init objects
    enemies = pygame.sprite.RenderPlain()
    for i in range(0, random.randint(NUM_CREEPS / 2 , NUM_CREEPS)-1):
        enemies.add(Creep(i, None, None))
    
    food = pygame.sprite.RenderPlain()
    for i in range(0, random.randint(NUM_FOOD /2 , NUM_FOOD) - 1):
        food.add(Food())
    
    hunters = pygame.sprite.RenderPlain()
    for i in range(0, random.randint(1, 4)):
        hunters.add(Hunter(i, None, None))
    
    
    entities = pygame.sprite.RenderUpdates(enemies, hunters, food)
    # allhunters = pygame.sprite.RenderPlain(hunters)
    #end init objects
    
    
    selected = None
    
    #map stuff
    mapDX = mapDY = 0
    map = Map(WORLD_SIZE)
    map.convert()
    map.generateWorld(screen)
    #end map stuff
    
    #main loop
    while running:
        #Listen for user events
        mousepos = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key in MOVE_KEYS:
                    if event.key == K_LEFT or event.key == K_a:
                        if mapDX >= 0:
                            mapDX = 0
                        else:
                            mapDX += SCROLL_SPEED
                    elif event.key == K_RIGHT or event.key == K_d:
                        if mapDX <= -(WORLD_SIZE[0] - WINDOW_SIZE[0]):
                            mapDX = -(WORLD_SIZE[0] - WINDOW_SIZE[0])
                        else:
                            mapDX -= SCROLL_SPEED
                    elif event.key == K_UP or event.key == K_w:
                        if mapDY >= 0:
                            mapDY = 0
                        else:
                            mapDY += SCROLL_SPEED
                    elif event.key == K_DOWN or event.key == K_s:
                        if mapDY <= -(WORLD_SIZE[1] - WINDOW_SIZE[1]):
                            mapDY = -(WORLD_SIZE[1] - WINDOW_SIZE[1])
                        else:
                            mapDY -= SCROLL_SPEED
                        
                else:
                    print "whoopsie!"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                event.pos = (event.pos[0] - mapDX, event.pos[1] - mapDY)
                if event.button == 1:
                    clearSelections(entities)
                    selected = None
                    for e in entities:
                        if e.rect.collidepoint(event.pos):
                            e.selected = True
                            selected = e
                            break
                elif event.button == 3:
                    mousepos = event.pos
            else:
                pygame.event.pump()
        #End event listening             
                    
        clock.tick(70)
        map.rect.topleft = (mapDX, mapDY)
        map.draw(screen)
        drawInfo(screen, bg, clock.get_fps(), len(enemies.sprites()), selected, map.rect.topleft, mousepos)
        
        #Enemy updates
        for e in enemies:
            e.update(food)
            e.draw(map)
            
        for h in hunters:
            h.update(enemies)
            h.draw(map)

        spawnFood = random.randint(1, 10000)
        if spawnFood > 9970 and len(food) < (NUM_CREEPS / 4) :
            food.add(Food())
        for f in food:
            f.update()
            f.checkGrazers(enemies)
            f.draw(map)
            

        # entities.draw(map)
        #check for game over
        if len(enemies) == 0:
            running = False
        
        pygame.display.flip()

    gameOver(screen)

    
# util functions
def clearSelections(es):
    for e in es:
        e.selected = False
                
def handleTextInput(st, font):
    if re.match(r"ask\s(?P<words>.*?)\sfen", st):
        textcolor = RED
        inspell = True
    else:
        textcolor = WHITE
        inspell = False
    message = font.render("Say: %s" % "".join(st), 1, textcolor)
    return (message, inspell)

def drawInfo(screen, bg, fps, numEnemies, selected, mappos, mousepos):
    screen.blit(bg, (0, WINDOW_SIZE[1]))
    pygame.draw.line(screen, WHITE, (0, WINDOW_SIZE[1]), (WINDOW_SIZE[0], WINDOW_SIZE[1]))
    font = pygame.font.Font(None, 14)
    screen.blit(font.render("FPS: %s | Number of Enemies: %s | Map Position : %s" % (fps, numEnemies, mappos), 1, WHITE), (0, WINDOW_SIZE[1] + 7))
    if selected and type(selected) is Creep or type(selected) is Hunter:
        screen.blit(font.render("Selected entity: %s | Eating?: %s | Speed: %s, Life: %s, Full: %s | Direction: %s | Position: %s" % \
                    (selected.id, selected.eating, round(selected.speed, 3), round(selected.life, 3), round(selected.full, 3), selected.direction, selected.position), \
                    1, WHITE), (0, WINDOW_SIZE[1] + 18))
    if mousepos:
        screen.blit(font.render("Mouse Position : %s, %s" % (mousepos[0], mousepos[1]), 1, WHITE), (0, WINDOW_SIZE[1] + 29))

def initialize():
    adjust_to_correct_appdir()
    pygame.init()
    pygame.key.set_repeat(1, 1)
    random.seed()
    full_window = (WINDOW_SIZE[0], WINDOW_SIZE[1] + 50)
    screen = pygame.display.set_mode(full_window)
    pygame.display.set_caption(GAME_TITLE)

    return screen

def gameOver(screen):
    font = pygame.font.Font(None, 50)
    screen.blit(font.render("GAME OVER", 1, RED), ((WINDOW_SIZE[0] /2) - 100, WINDOW_SIZE[1]/2))
    pygame.display.update()
    pygame.time.delay(3000)


if __name__ == '__main__':
    main()
