
class FKLS:
    
    def __init__(self, location, j, i):
        self.location = location
        self.source = location
        self.j = j
        self.i = i
        self.step = None
        self.u = None
        self.t = 0
        self.spiralSide = 0
        self.spiralIndex = -1
        self.spiralNumber = 0
        self.spiralParity = 0

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
        
        # IMPLEMENT IN SUBCLASS
        raise NotImplementedError('must implement chooseNode() in subclass')

        self.step = 'going to node'

    def chooseUniformly(self, r):
        x = None
        y = None
        while x == None or y == None or x*x + y*y > r*r:
            x = random.randint(-r, r)
            y = random.randint(-r, r)
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

    def t_max(self):
        #IMPLEMENT IN SUBCLASS
        raise NotImplementedError('must implement t_max() in subclass')
        return 0

    def spiral(self):
        assert self.step == 'spiral'

        if self.t < self.t_max():
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
        
        # IMPLEMENT IN SUBCLASS
        raise NotImplementedError('must implement returnToSource() in subclass')

        self.step = 'choosing node'


class FKLS1(FKLS):

    def __init__(self, location, k):
        FKLS.__init__(self, location, 1, 1)
        self.k = k

    def chooseNode(self):
        assert self.step == 'choosing node'
        self.u = self.chooseUniformly( math.pow(2, 2*self.i) )
        self.step = 'going to node'

    def returnToSource(self):
        assert self.step == 'return'
        self.location = self.source
        if self.i == self.j:
            self.j += 1
            self.i = 1
        elif self.i < self.j:
            self.i += 1
        self.step = 'choosing node'

    def t_max(self):
        return math.pow(2, 2*self.i + 2)/float(self.k)


class FKLS2(FKLS):

    def __init__(self, location, f):
        FKLS.__init__(self, location, 0, 0)
        self.l = 0
        self.f = f

    def chooseNode(self):
        assert self.step == 'choosing node'
        D_i_j = math.sqrt( math.pow( 2, self.i+self.j ) / self.f(self.j) )
        self.u = self.chooseUniformly( math.round(D_i_j) )
        self.step = 'going to node'

    def returnToSource(self):
        assert self.step == 'return'
        self.location = self.source
        if self.i == self.j:

            if self.j == self.l:
                self.l += 1
                self.j = 0
                self.i = 0
            else:            
                self.j += 1
                self.i = 0

        elif self.i < self.j:
            self.i += 1

        self.step = 'choosing node'

    def t_max(self):
        return math.round( math.pow( 2, self.i+2 ) / self.f(self.j) )


