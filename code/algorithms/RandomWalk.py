import random

class RandomWalk:

    def __init__(self, location, k):
        self.location = location
        self.k = k

    def getLocation(self):
        return self.location

    dir = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def act(self):
        nextStep = random.randint(0, 4)
        x, y = self.location
        self.location = (x + dir[nextStep][0], y + dir[nextStep][1])
