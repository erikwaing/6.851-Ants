import random
import math

class FKLS1:
    
    def __init__(self, location, k):
        self.location = location
        self.source = location
        self.j = 1
        self.i = 1
        self.step = None
        self.u = None
        self.t = 0
        self.spiralSide = 0
        self.spiralIndex = -1
        self.spiralNumber = 0
        self.spiralParity = 0
        self.k = k

    def getLocation(self):
        return self.location

    def act(self):
        if self.step == None or self.step == 'choosing node':
            self.step = 'choosing node'
            self.chooseNode()
        elif self.step == 'going to node':
            self.goToNode()
        elif self.step == 'spiral':
            self.spiral()
        elif self.step == 'return':
            self.returnToSource()

    def chooseNode(self):
        assert self.step == 'choosing node'
        self.u = self.chooseUniformly(self.i)
        self.step = 'going to node'

    def chooseUniformly(self, i):
        x = None
        y = None
        while x == None or y == None or x*x + y*y > i:
            x = random.randint(-i, i)
            y = random.randint(-i, i)
        return (x,y)

    def goToNode(self):
        assert self.step == 'going to node'
        (x0,y0) = self.location
        (x1,y1) = self.u
        (l, w) = (x1 - x0, y1 - y0)
        if l != 0:
            self.location = (x0 + l/abs(l), y0)
        elif w != 0:
            self.location = (x0, y0 + w/abs(w))
        elif l == 0 and w == 0:
            self.step = 'spiral'

    def spiral(self):
        assert self.step == 'spiral'
        if self.t < math.pow(2, 2*self.i + 2)/float(self.k):
            self.stepSpiral()
        else:
            self.resetSpiral()

    def stepSpiral(self):
        self.checkSpiralIndex()
        if self.spiralSide == 0:
            if self.spiralIndex == -1:
                self.spiralNumber += 2
                self.spiralMoveUpAndFinish() # so that it extends one farther.
            else:
                self.spiralRightDown()
        elif self.spiralSide == 1:
            self.spiralLeftDown()
        elif self.spiralSide == 2:
            self.spiralLeftUp()
        elif self.spiralSide == 3:
            self.spiralRightUp()
        self.spiralIndex += 1
        self.t += 1
        self.spiralParity = 1 - self.spiralParity

    def checkSpiralIndex(self):
        if self.spiralIndex >= self.spiralNumber:
            self.spiralSide = (self.spiralSide + 1) % 4
            self.spiralIndex = 0
            if self.spiralSide == 0:
                self.spiralIndex = -1
            
    def spiralMoveUpAndFinish(self):
        (x,y) = self.location
        self.location = (x, y+1)
        self.spiralParity = 1 - self.spiralParity # we don't want to change the parity. also hacky. 

    def spiralRightDown(self):
        (x,y) = self.location
        if self.spiralParity == 0:
            self.location = (x+1, y)
        elif self.spiralParity == 1:
            self.location = (x, y-1)
            
    def spiralLeftDown(self):
        (x,y) = self.location
        if self.spiralParity == 0:
            self.location = (x, y-1)
        elif self.spiralParity == 1:
            self.location = (x-1, y)
            
    def spiralLeftUp(self):
        (x,y) = self.location
        if self.spiralParity == 0:
            self.location = (x-1, y)
        elif self.spiralParity == 1:
            self.location = (x, y+1)
            
    def spiralRightUp(self):
        (x,y) = self.location
        if self.spiralParity== 0:
            self.location = (x, y+1)
        elif self.spiralParity == 1:
            self.location = (x+1, y)

    def resetSpiral(self):
        self.t = 0
        self.spiralSide = 0
        self.spiralNumber = 0
        self.spiralParity = 0
        self.spiralLength = 0
        self.spiralIndex = -1
        self.step = 'return'

    def returnToSource(self):
        assert self.step == 'return'
        self.location = self.source
        if self.i == self.j:
            self.j += 1
            self.i = 1
        elif self.i < self.j:
            self.i += 1
        self.step = 'choosing node'
