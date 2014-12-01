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
		if self.step == 'up':
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
			self.moveUp()
		else:
			self.step = 'down'
			self.moveDown()

	def moveUp(self):
		if random.random() > (1.0/self.D):
			(x0 , y0) = self.location
			self.location = (x0 , y0 + 1)
		elif random.random() < 0.5:
			self.step = 'left'
			self.moveLeft()
		else:
			self.step = 'right'
			self.moveRight()

	def moveDown(self):
		if random.random() > (1.0/self.D):
			(x0 , y0) = self.location
			self.location = (x0 , y0 - 1)
		elif random.random() < 0.5:
			self.step = 'left'
			self.moveLeft()
		else:
			self.step = 'right'
			self.moveRight()

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
		self.j = 1
		self.step = 'simulate'
		self.simulation = LinesNonUniform(self.source, 1)


	def getLocation(self):
		if self.simulation is None:
			return self.source
		return self.simulation.getLocation()

	def act(self):
		if self.step == 'advance':
			self.advance()
		elif self.step == 'simulate':
			self.simulate()

	def advance(self):
		p = self.K + max( self.i - math.floor( math.log(self.n , 2) ) , 0 )
		max_j = int(2**p)
		if self.j == max_j:
			self.i += 1
			self.j = 1
			LinesNonUniform(self.source, 2**self.i)
		else:
			self.j += 1

		self.step = 'simulate'
		self.simulate()

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

	def __init__(self, location, K):
		self.source = location
		self.K = K
		self.i = 0
		self.n = 1
		self.j = 1
		self.step = 'simulate'
		self.simulation = LinesNonUniform(self.source, 1)

	def getLocation(self):
		if self.simulation is None:
			return self.source
		return self.simulation.getLocation()

	def act(self):
		if self.step == 'advance':
			self.advace()
		elif self.step == 'simulate':
			self.simulate()

	def advance(self):
		p = self.K + max( self.i - math.floor( math.log(self.n , 2) ) , 0 )
		max_j = int(2**p)
		if self.j == max_j:
			if self.n >= 2**self.i:
				self.i += 1
				self.n = 1
				self.j = 1
				self.simulation = LinesNonUniform(self.source, 2**self.i)
			else:
				self.n *= 2
				self.j = 1
		else:
			self.j += 1

		self.step = 'simulate'
		self.simulate()


	def simulate(self):
		if self.simulation.step == 'origin':
			self.simulation.act()
			self.step = 'advance'
		else:
			self.simulation.act()


