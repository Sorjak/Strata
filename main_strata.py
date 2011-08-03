import os, sys, pygame, random
from pygame.locals import *
from objects_strata import *
from utils_strata import *
from pygame.examples.mask import Sprite

def main():
    screen , background = initialize()
    clock = pygame.time.Clock()
    running = 1
    
    font = pygame.font.Font(None, 24)
    
    enemies = pygame.sprite.RenderPlain()
    for i in range(0, random.randint(NUM_CREEPS / 2 , NUM_CREEPS)-1):
        enemies.add(Creep(i))
    print len(enemies.sprites())
    allenemies = pygame.sprite.RenderUpdates(enemies)
    
    food = pygame.sprite.RenderPlain()
    for i in range(0, random.randint(NUM_FOOD /2 , NUM_FOOD) - 1):
        food.add(Food())
    
    
    hunters = [Hunter()]
    
    allhunters = pygame.sprite.RenderPlain(hunters)
    
    #main loop
    while running:
        #Listen for user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key in MOVE_KEYS:
                    print "You pressed %s!" % event.key
                else:
                    print "whoopsie!"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clearSelections(enemies)
                    for e in enemies:
                        if e.rect.collidepoint(event.pos):
                            e.selected = True
                            # print "%s has %s kills" % (e.id, e.kills)
        #End event listening             
                    
        clock.tick(60)
        drawBackground(screen, background)
        
        #Enemy updates
        for e in enemies:
            e.update()
            handleEnemyCollisions(e, enemies)
            e.graze(food)
            e.draw(screen)
            
        #End enemy updates
        clearSelections(enemies)
        for h in hunters:
            h.update()
            h.hunt(enemies)
            h.draw(screen)
        
        food.update()
        food.draw(screen)
        
        #check for game over
        if len(enemies.sprites()) == 1:
            running = False
        
            
        allenemies.draw(screen)
        allhunters.draw(screen)
        pygame.display.flip()

    gameOver(screen)

    
# util functions
def clearSelections(es):
    for e in es:
        e.selected = False


def handleEnemyCollisions(e, enemies):
    for ei in enemies:
        if e is not ei:
            if e.rect.colliderect(ei.rect):
                if e.growth > ei.growth:
                    ei.kill()
                    e.grow(ei.growth)
                elif ei.growth > e.growth:
                    e.kill()
                    ei.grow(e.growth)
                else:
                    temp = e.angle
                    e.angle = ei.angle
                    ei.angle = temp
                # print "%s vs %s, %s has %s kills." % (e.id, ei.id, ei.id, ei.kills )
                break
                
def handleTextInput(st, font):
    if re.match(r"ask\s(?P<words>.*?)\sfen", st):
        textcolor = RED
        inspell = True
    else:
        textcolor = WHITE
        inspell = False
    message = font.render("Say: %s" % "".join(st), 1, textcolor)
    return (message, inspell)

def drawBackground(screen, bgrd):
    screen.blit(bgrd, (0, 0))
    pygame.draw.line(screen, WHITE, (0, WINDOW_SIZE[1]), (WINDOW_SIZE[0], WINDOW_SIZE[1]))
    #for x in range(int(screen.get_width() / 80) + 1):
    #    for y in range(int(screen.get_height() / 80) + 1):
    #        tsquare = MapSquare()
    #        tsquare.rect.topleft = (x * tsquare.rect.width, y * tsquare.rect.height)
    #        screen.blit(tsquare.image, tsquare.rect)

def initialize():
    adjust_to_correct_appdir()
    pygame.init()
    pygame.key.set_repeat(1, 1)
    random.seed()
    full_window = (WINDOW_SIZE[0], WINDOW_SIZE[1] + 50)
    screen = pygame.display.set_mode(full_window)
    pygame.display.set_caption(GAME_TITLE)
    background = pygame.Surface(full_window)
    background = background.convert()
    background.fill(BG_COLOR)
    return (screen, background)

def gameOver(screen):
    font = pygame.font.Font(None, 50)
    screen.blit(font.render("GAME OVER", 1, RED), ((WINDOW_SIZE[0] /2) - 100, WINDOW_SIZE[1]/2))
    pygame.display.update()
    pygame.time.delay(3000)


if __name__ == '__main__':
    main()
