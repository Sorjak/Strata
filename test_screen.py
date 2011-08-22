import os, sys, pygame, random
from pygame.locals import *
from utils_strata import *
from objects_strata import Map, MapTile, Food

WORLD_SIZE = (1400, 600)
SCROLL_SPEED = 2

def main():
    screen , background = initialize()
    clock = pygame.time.Clock()
    running = 1
    # viewport = background.subsurface((0, 0) + (WINDOW_SIZE[0], WINDOW_SIZE[1]))
    # viewport.fill(BLACK)
    # viewrect = pygame.Rect((0,0), WINDOW_SIZE)
    
    food = pygame.sprite.RenderPlain()
    for i in range(0, random.randint(NUM_FOOD /2 , NUM_FOOD) - 1):
        food.add(Food())
        
    bgrdDX = bgrdDY = 0
    
    map = Map(WORLD_SIZE)
    print map
    
    map.generateWorld(screen)
    while running:
        #Listen for user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key in MOVE_KEYS:
                    if event.key == K_LEFT or event.key == K_a:
                        if bgrdDX >= 0:
                            bgrd = 0
                        else:
                            bgrdDX += SCROLL_SPEED
                    elif event.key == K_RIGHT or event.key == K_d:
                        if bgrdDX <= -(WORLD_SIZE[0] - WINDOW_SIZE[0]):
                            bgrd = WORLD_SIZE[0] - WINDOW_SIZE[0]
                        else:
                            bgrdDX -= SCROLL_SPEED
                    elif event.key == K_UP or event.key == K_w:
                        pass
                    elif event.key == K_DOWN or event.key == K_s:
                        pass
                        
                else:
                    print "whoopsie!"
                    
        clock.tick(70)
        # screen.blit(background, (bgrdDX, bgrdDY))
        # screen.blit(background, (0, 0))
        print bgrdDX, bgrdDY
        # for f in food:
            # f.update()
            # f.checkGrazers(enemies)
            # f.draw(screen)
        
        # screen.blit(viewport, (0, 0))
        screen.blit(map, (bgrdDX, bgrdDY))
        # pygame.draw.rect(screen, RED, viewrect, 1)
        font = pygame.font.Font(None, 14)
        
        
        pygame.display.flip()
        

def drawBackground(screen, bgrd):
    pass

def initialize():
    adjust_to_correct_appdir()
    pygame.init()
    pygame.key.set_repeat(1, 1)
    random.seed()
    full_window = (WINDOW_SIZE[0], WINDOW_SIZE[1] + 50)
    screen = pygame.display.set_mode(full_window)
    screen.fill(BLACK)
    pygame.display.set_caption(GAME_TITLE)
    background = pygame.Surface((2000, 400))
    background = background.convert()
    background.fill(WHITE)
    return (screen, background)
    
    
if __name__ == '__main__':
    main()