import random
import math

class LinesNonUniform:

	def __init__(self, location, D):
		self.location = location
		self.source = location
		self.step = 'start'
		self.D = D

	def getLocation(self):
		return self.location

	def act(self):
		if self.step == 'start':
			self.start()
		elif self.step == 'up':
			self.moveUp()
		elif self.step == 'down':
			self.moveDown()
		elif self.step == 'left':
			self.moveLeft()
		elif self.step == 'right':
			self.moveRight()
		elif self.step == 'origin':
			self.backToOrigin()

	def start(self):
		if random.random() < 0.5:
			self.step = 'up'
		else:
			self.step = 'down'

	def moveUp(self):
		if random.random() > (1.0/self.D):
			(x0 , y0) = self.location
			self.location = (x0 , y0 + 1)
		elif random.random() < 0.5:
			self.step = 'left'
		else:
			self.step = 'right'

	def moveDown(self):
		if random.random() > (1.0/self.D):
			(x0 , y0) = self.location
			self.location = (x0 , y0 - 1)
		elif random.random() < 0.5:
			self.step = 'left'
		else:
			self.step = 'right'

	def moveLeft(self):
		if random.random() > (1.0/self.D):
			(x0 , y0) = self.location
			self.location = (x0 - 1 , y0)
		else:
			self.step = 'origin'

	def moveRight(self):
		if random.random() > (1.0/self.D):
			(x0 , y0) = self.location
			self.location = (x0 + 1 , y0)
		else:
			self.step = 'origin'

	def backToOrigin(self):
		self.location = self.source
		self.step = 'start'


class LinesUniformInD(LinesNonUniform):

	def __init__(self, location, n, K):
		self.source = location
		self.n = n
		self.K = K
		self.i = 0
		self.step = 'start'
		self.simulation = None


	def getLocation(self):
		if self.simulation is None:
			return self.source
		return self.simulation.getLocation()

	def act(self):
		if self.step == 'start':
			self.start()
		elif self.step == 'try':
			self.trySearch()
		elif self.step == 'simulate':
			self.simulate()

	def start(self):
		self.simulation = LinesNonUniform(self.source, math.pow(2 , 2*self.i))
		self.step = 'try'

	def trySearch(self):
		p = self.K + max( self.i - math.floor( math.log(self.n , 2) ) , 0 )
		if random.random() > (1.0 / p):
			self.step = 'simulate'
		else:
			self.i += 1
			self.step = 'start'

	def simulate(self):
		if self.simulation.step == 'origin':
			self.simulation.act()
			self.step = 'try'
		else:
			self.simulation.act()


