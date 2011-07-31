import os, pygame, math
from pygame.locals import *

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BG_COLOR = BLACK
WINDOW_SIZE = (800, 600)
GAME_TITLE = 'Strata'
MOVE_KEYS = (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT,
            pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a)
NUM_CREEPS = 40
NUM_FOOD = 10

#TERRAIN_TYPES = ("normal", "ice", "desert", "")


def findNearest(myrect, things):
    mini = (None, 99999)
    for e in things:
        dto_topleft = hypot(e.rect.topleft[0] - myrect.center[0], e.rect.topleft[1] - myrect.center[1])
        dto_topright = hypot(e.rect.topright[0] - myrect.center[0], e.rect.topright[1] - myrect.center[1])
        dto_bottomleft = hypot(e.rect.bottomleft[0] - myrect.center[0], e.rect.bottomleft[1] - myrect.center[1])
        dto_bottomright = hypot(e.rect.bottomright[0] - myrect.center[0], e.rect.bottomright[1] - myrect.center[1])
        
        distance = min(dto_topleft, dto_topright, dto_bottomleft, dto_bottomright)

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
        

from math import sqrt,hypot

class Vector2(object):
    
    __slots__ = ('_x', '_y')
    
    def __init__(self, x=0., y=0.):
        """Initialise a vector
        x -- The x value (defaults to 0.)
        y -- The y value (defaults to 0.)
        
        """
        self._x = float(x)
        self._y = float(y)
    
        
    @staticmethod
    def from_iterable(iterable):
        """Creates a Vector2 object from an iterable.
        iterable -- An iterable of at least 2 numeric values
        
        """
        it = iter(iterable)
        x = it.next()
        y = it.next()
        v = Vector2(x, y)        
        
    @staticmethod
    def from_points(p1, p2):
        """Creates a Vector2 object between two points.
        p1  -- First point
        p2 -- Second point
        
        """
        v = Vector2.__new__(Vector2, object)
        v._x = p2[0] - p1[0]
        v._y = p2[1] - p1[1]
        return v
    
    def copy(self):
        """Returns a copy of this object."""
        return Vector2(self._x, self._y)
        
    def get_x(self):
        return self._x
    def set_x(self, x):
        self._x = float(x)
    x = property(get_x, set_x, None, "x component.")
    
    def get_y(self):
        return self._y
    def set_y(self, y):
        self._y = float(y)
    y = property(get_y, set_y, None, "y component.")
        
    u = property(get_x, set_y, None, "u component (alias for x).")
    v = property(get_y, set_y, None, "v component (alias for y).")
        
    def __str__(self):
        
        return "( %s, %s )" % (self._x, self._y)
    
    def __repr__(self):
        
        return "Vector2(%s, %s)" % (self._x, self._y)
        
    def help(self):
        
        return "This is a Vector2 object used to represent direction and magnitude (length) or a position - in 2 dimensions"\
                "\n\tIts has the value %s\n\tIt is %s units long" % (self, self.get_length())        
                
    def __iter__(self):
        
        yield self._x
        yield self._y
        
    def __len__(self):
        
        return 2
    
    
    def __getitem__(self, index):
        """Gets a component as though the vector were a list."""
        try:            
            return getattr(self, self.__slots__[index])
        except IndexError:
            raise IndexError, "There are 2 values in this object, index should be 0 or 1!"
            
    def __setitem__(self, index, value):
        """Sets a component as though the vector were a list."""
        try:
            setattr( self, self.__slots__[index], value )            
        except IndexError:
            raise IndexError, "There are 2 values in this object, index should be 0 or 1!"
     
          
    def __add__(self, rhs):
        
        return Vector2(self._x+rhs[0], self._y+rhs[1])
        
        
    def __iadd__(self, rhs):
        
        self._x += rhs[0]
        self._y += rhs[1]
        return self
        
        
    def __sub__(self, rhs):
        
        return Vector2(self._x-rhs[0], self._y-rhs[1])
        
        
    def _isub__(self, rhs):
        
        self._x -= rhs[0]
        self._y -= rhs[1]
        return self
        
        
    def __mul__(self, rhs):
        """Return the result of multiplying this vector with a scalar or a vector-list object."""        
        if hasattr(rhs, "__getitem__"):
            return Vector2(self._x*rhs[0], self._y*rhs[1])
        else:
            return Vector2(self._x*rhs, self._y*rhs)
            
            
    def __rmul__(self, rhs):
        """Multiplys this vector with a scalar or a vector-list object.""" 
        if hasattr(rhs, "__getitem__"):
            self._x *= rhs[0]
            self._y *= rhs[1]            
        else:
            self._x *= rhs
            self._y *= rhs
        return self
        
        
    def __div__(self, rhs):
        """Return the result of dividing this vector by a scalar or a vector-list object."""        
        if hasattr(rhs, "__getitem__"):
            return Vector2(self._x/rhs[0], self._y/rhs[1])
        else:
            return Vector2(self._x/rhs, self._y/rhs)
            
            
    def __idiv__(self, rhs):
        """Divides this vector with a scalar or a vector-list object."""
        if hasattr(rhs, "__getitem__"):
            self._x /= rhs[0]
            self._y /= rhs[1]            
        else:
            self._x /= rhs
            self._y /= rhs
        return self
       
       
    def __neg__(self):
        """Return the negation of this vector."""
        return Vector2(-self._x, -self._y)
    
    def __call__(self, keys):
        """Used to swizzle a vector.
        keys -- A string containing a list of component names
        i.e. vec = Vector(1, 2)
        vec('yx') --> (2, 1)"""
        return tuple( getattr(self, "_"+key) for key in keys )


    def as_tuple(self):
        """Converts this vector to a tuple."""
        return (self._x, self._y)


    def get_length(self):
        """Returns the length of this vector."""
        return hypot(self._x,self._y)
        
    
    def get_magnitude(self):
        """Returns the length of this vector."""
        return hypot(self._x,self._y)
        
    
    def get_normalized(self):
        length = self.get_length()
        return Vector2(self._x / length, self._y / length)
    
    def normalise(self):
        """Normalises this vector."""
        length = self.get_length()
        if length:
            self._x /= length
            self._y /= length
            
    
    def get_distance(self, p):
        """Returns the distance to a point.
        
        p -- A Vector2 or list-like object with at least 2 values."""
        return sqrt( (self._x - p[0])**2 + (self._y - p[1])**2 );
