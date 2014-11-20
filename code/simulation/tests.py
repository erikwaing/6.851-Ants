from algorithms.FKLS import *
from algorithms.Lines import *
from algorithms.RandomWalk import *
from simulation.board import *
import sys
import random
import math

class Tests:

    def testUniform(self, numAgents, D, trialsPerAgent, type):
        '''
        numAgents, a list of the number of agents
        D, a list of the distances upper bound - should be same size as numAgents
        trialsPerAgent, an integer, indicating how many trails per element in list
        type, an object with type.name being the name of the algorithm and 
              type.args being any arguments to the algorithms
        returns a list of lists with the times that it took to find treasure
        '''
        results = []
        for i in range(len(numAgents)):
            k = numAgents[i]
            distance = D[i]
            experiment = []
            for j in range(trialsPerAgent):
                ants = self.generateAnts(k, type)
                treasureLoc = self.selectTreasureLocation(distance)
                board = Board(treasureLoc, ants)
                self.drawProgressBar((i*len(numAgents)+j)/float(len(numAgents)*trialsPerAgent))
                experiment.append(board.runAnts())
                results.append(experiment)
        return results

    def generateAnts(self, n, type):
        if type['name'] == "FKLS2":
            return self.generateUniformFKLSAnts(n, type['args'])
        elif type['name'] == "FKLS1":
            return self.generateNonUniformFKLSAnts(n)
        elif type['name'] == "LinesNonUniform":
            return self.generateNonUniformLinesAnts(n, type['args'])
        elif type['name'] == "Random":
            return self.generateRandomAnts(n)

    def generateNonUniformFKLSAnts(self, n):
        return [FKLS1((0,0), n) for i in range(n)]

    def generateUniformFKLSAnts(self, n, f):
        '''
        n, number of ants
        returns a list of FKLS ants, all with origin (0,0)
        '''
        ants = [FKLS2((0,0), f) for i in range(n)]
        return ants

    def generateNonUniformLinesAnts(n, D):
        return [LinesNonUniform((0,0), D) for i in range(n)]

    def generateRandomAnts(self, n):
        return [RandomWalk((0,0)) for i in range(n)]

    def selectTreasureLocation(self, distance):
        x = random.randint(-distance, distance)
        y = random.randint(-distance, distance)
        if x*x + y*y > distance*distance:
            return self.selectTreasureLocation(distance)
        else:
            return (x,y)

    def drawProgressBar(self, percent, barLen = 20):
        sys.stdout.write("\r")
        progress = ""
        for i in range(barLen):
            if i < int(barLen * percent):
                progress += "="
            else:
                progress += " "
        sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
        sys.stdout.flush()
        
