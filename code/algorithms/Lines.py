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
			self.act()
		else:
			self.step = 'down'
			self.act()

	def moveUp(self):
		if random.random() > (1.0/self.D):
			(x0 , y0) = self.location
			self.location = (x0 , y0 + 1)
		elif random.random() < 0.5:
			self.step = 'left'
			self.act()
		else:
			self.step = 'right'
			self.act()

	def moveDown(self):
		if random.random() > (1.0/self.D):
			(x0 , y0) = self.location
			self.location = (x0 , y0 - 1)
		elif random.random() < 0.5:
			self.step = 'left'
			self.act()
		else:
			self.step = 'right'
			self.act()

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
		self.i = 1
		self.j = 1
		self.step = 'simulate'
		self.simulation = LinesNonUniform(self.source, 2**self.i)


	def getLocation(self):
		if self.simulation is None:
			return self.source
		return self.simulation.getLocation()

	def act(self):
		if self.step == 'advance':
			self.advance()
		if self.step == 'simulate':
			self.simulate()

	def advance(self):
		p = self.K + max( self.i - math.floor( math.log(self.n , 2) ) , 0 )
		max_j = int(2**p)
		if self.j == max_j:
			self.i += 1
			self.j = 1
			self.simulation = LinesNonUniform(self.source, 2**self.i)
		else:
			self.j += 1
		self.step = 'simulate'

	# def start(self):
	# 	self.simulation = LinesNonUniform(self.source, math.pow(2 , self.i))
	# 	self.trySearch()

	# def trySearch(self):
	# 	p = self.K + max( self.i - math.floor( math.log(self.n , 2) ) , 0 )
	# 	if random.random() > (1.0 / (2**p)):
	# 		self.step = 'simulate'
	# 		self.simulate()
	# 	else:
	# 		self.i += 1
	# 		self.step = 'start'

	def simulate(self):
		if self.simulation.step == 'origin':
			self.simulation.act()
			self.step = 'advance'
		else:
			self.simulation.act()


class LinesUniformInAll(LinesUniformInD):

	def __init__(self, location, K, f=(lambda x: x**2 + 1)):
		self.source = location
		self.K = K
		self.f = f
		self.i = 1
		self.logn = 0
		self.j = 1
		self.step = 'simulate'
		self.simulation = LinesNonUniform(self.source, math.sqrt( 2**(self.i+self.logn) / self.f(self.logn) ) )

	def getLocation(self):
		return self.simulation.getLocation()

	def act(self):
		if self.step == 'advance':
			self.advance()
		if self.step == 'simulate':
			self.simulate()

	def advance(self):
		p = self.K + max( self.i - self.logn , 0 )
		max_j = int(2**p)
		if self.j == max_j:
			if self.logn == self.i:
				self.i += 1
				self.logn = 0
				self.j = 1
			else:
				self.logn += 1
				self.j = 1
			D_in = math.sqrt( 2**(self.i+self.logn) / self.f(self.logn) )
			self.simulation = LinesNonUniform(self.source, D_in)

		else:
			self.j += 1
		self.step = 'simulate'


	def simulate(self):
		if self.simulation.step == 'origin':
			self.simulation.act()
			self.step = 'advance'
		else:
			self.simulation.act()


