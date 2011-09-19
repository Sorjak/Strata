import random, math, pygame
from pygame.math import Vector2 as Point

class Square(object):
    def __init__(self, tl, br, myarr, rough):
        self.tl = tl #Top left
        self.tr = Point(br.x, tl.y) #Top right
        self.br = br #Bottom right
        self.bl = Point(tl.x, br.y) #Bottom left
        self.dimensions = [self.tl, self.tr, self.br, self.bl]
        self.center = Point(br.x - ((br.x - tl.x) / 2), br.y - ((br.y - tl.y) / 2))
        self.myarr = myarr
        self.children = [None, None, None, None]
        self.rough = rough
        self.size = br.x - tl.x
        self.value = self.getValue()
        self.myarr[int(self.center.x)][int(self.center.y)] = self.value
        
    def divide(self, done):
        if self.size == 1:
            done(self.tl, self.value)
            return True
        self.children[0] = Square(self.tl, self.center, self.myarr, self.rough/2.0)
        self.children[3] = Square(self.center, self.br, self.myarr, self.rough/2.0)
        self.children[1] = Square(self.children[0].tr, self.children[3].tr, self.myarr, self.rough/2.0)
        self.children[2] = Square(self.children[0].bl, self.children[3].bl, self.myarr, self.rough/2.0)
        for child in self.children:
            child.divide(done)
        
    def getValue(self):
        avg = 0
        for d in self.dimensions:
            avg += self.myarr[int(d.x)][int(d.y)]
        
        avg = avg / 4
        return round(avg + random.uniform(-self.rough, self.rough), 3)
    
def doNothing(thing, thing2):
    pass
    
def main():
    random.seed()
    
    roughness = 1.0
    
    arraysize = 129

    tensidearray = [[0 for col in range(arraysize)] for row in range(arraysize)]
    
    tensidearray[0][0] = .9
    tensidearray[0][arraysize - 1] = .5
    tensidearray[arraysize - 1][0] = .3
    tensidearray[arraysize - 1][arraysize - 1] = .7
    
    sq = Square(Point(0, 0), Point(arraysize - 1, arraysize - 1), tensidearray, roughness)
    # print sq.topleft, sq.topright, sq.bottomleft, sq.bottomright
    # print sq.center
    
    sq.divide(doNothing)
    
    Max = -9999
    Min = 9999
    for y in range(arraysize):
        for x in range(arraysize):
            if tensidearray[x][y] < Min:
                Min = tensidearray[x][y]
            if tensidearray[x][y] > Max:
                Max = tensidearray[x][y]
    
    print Max, Min
    
if __name__ == '__main__':
    main()