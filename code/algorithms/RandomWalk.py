import random

class RandomWalk:

    def __init__(self, location):
        self.location = location
        self.dir = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def getLocation(self):
        return self.location

    def act(self):
        nextStep = random.randint(0, 3)
        x, y = self.location
        x = x + self.dir[nextStep][0]
        y = y + self.dir[nextStep][1]
        self.location = (x, y)
