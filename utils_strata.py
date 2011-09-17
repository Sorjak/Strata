import os, pygame, math
from pygame.locals import *
from pygame.math import Vector2

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BG_COLOR = BLACK
WINDOW_SIZE = (800, 600)
WORLD_SIZE = (1000, 1000)
GAME_SIZE = WORLD_SIZE
SCROLL_SPEED = 2
GAME_TITLE = 'Strata'
MOVE_KEYS = (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT,
            pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a)
NUM_CREEPS = 40
NUM_FOOD = 10
MAPTILE_SIZE = (20, 20)

#TERRAIN_TYPES = ("normal", "ice", "desert", "")

from math import hypot

def findNearest(mypos, things, exclude=None):
    mini = (None, 99999)
    for e in things:
        if exclude:
            if e in exclude:
                pass
            else:
                distance = math.sqrt(((mypos.x - e.position.x) ** 2) + ((mypos.y - e.position.y) ** 2))
                
                if distance < mini[1]:
                    mini = (e, distance)  
    return mini[0]

def load_image(name, colorkey=None):
    fullname = os.path.join("media", name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('media', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return sound

def addVectors((angle1, length1), (angle2, length2)):
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2    
    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return (angle, length)
    
def adjust_to_correct_appdir():
    import os, sys
    try:
        appdir = sys.argv[0] #feel free to use __file__
        if not appdir:
            raise ValueError
        appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
        os.chdir(appdir)
        if not appdir in sys.path:
            sys.path.insert(0,appdir)
    except:
        #placeholder for feedback, adjust to your app.
        #remember to use only python and python standart libraries
        #not any resource or module into the appdir 
        #a window in Tkinter can be adequate for apps without console
        #a simple print with a timeout can be enough for console apps
        print 'Please run from an OS console.'
        import time
        time.sleep(10)
        sys.exit(1)
        
