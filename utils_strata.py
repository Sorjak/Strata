import os, pygame, math, sys
from pygame.locals import *

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BG_COLOR = BLACK
MAP_GEN_NUM = 129
MAP_GEN_ROUGH = 0.75
WINDOW_SIZE = (800, 600)
WORLD_SIZE = (MAP_GEN_NUM * 15, MAP_GEN_NUM * 15)
GAME_SIZE = WORLD_SIZE


MAPTILE_SIZE = (20, 20)

MAX_INT = sys.maxint

ANIMAL_DECAY = .002

GAME_STATUS = True

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
        print 'Please run from an OS console.'
        import time
        time.sleep(10)
        sys.exit(1)

import threading

class RepeatTimer(object):
    def __init__(self, interval, callable, *args, **kwargs):
        self.interval = interval
        self.callable = callable
        self.args = args
        self.kwargs = kwargs
        self.mThread = None

    def startTimer(self):
        self.mThread = threading.Timer(self.interval, self.callable,
                            self.args, self.kwargs)
        self.mThread.start()
        # t.join()
    def isRunning(self):
        if self.mThread:
            return self.mThread.isAlive()
        else:
            return False
    def stopTimer(self):
        if self.isRunning():
            self.mThread.cancel()
