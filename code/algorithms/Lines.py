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






