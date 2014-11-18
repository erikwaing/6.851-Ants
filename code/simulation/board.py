class Board:
    
    def __init__(self, location, ants):
        self.treasure = location
        self.ants = ants

    def act(self):
        for ant in self.ants:
            ant.act()

    def check(self):
        for ant in self.ants:
            if ant.getLocation() == self.treasure:
                return True
        return False

    def runAnts(self):
        steps = 0
        while not self.check():
            self.act()
            steps += 1
        return steps
