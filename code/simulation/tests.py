from algorithms.FKLS import *
from algorithms.Lines import *
from algorithms.RandomWalk import *
from simulation.board import *
import sys
import random
import math
import pickle
import datetime

class Tests:

    def runAllTests(self, numAgents, D, trialsPerAgent):
        types = [{'name':'FKLS1', 'args': None, 'argsName':'no args'},
                 {'name':'FKLS2', 'args':lambda x: x**2+1, 'argsName': 'function f square'},
                 {'name':'LinesNonUniform', 'args': 0, 'argsName': 'D'}, # need to overwrite D
                 {'name':'LinesUniformInD', 'args': 6, 'argsName': 'K = 6'},
                 {'name':'LinesUniformInAll', 'args': 6, 'argsName': 'K = 6'},
                 {'name':'HarmonicSearch', 'args': 1, 'argsName': 'delta = 1'}
                ]

        for anttype in types:
            print anttype
            print "Starting Tests..."
            results = self.testUniform(numAgents, D, trialsPerAgent, anttype)
            print results
            print "Pickling..."
            exp = {'numAgents':numAgents, 'D': D, 'trialsPerAgent':trialsPerAgent}
            testInfo = {'type': anttype['name'], 'argsDesc': anttype['argsName'], 'data':results,
                        'experiment': exp }
            name = 'data/' + anttype['name'] + str(datetime.date.today())
            outputFile = open(name, 'wr')
            pickle.dump(testInfo, outputFile)
            outputFile.close()

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
        totalNumExperiments = len(numAgents) * trialsPerAgent
        current = 0
        for i in range(len(numAgents)):
            k = numAgents[i]
            distance = D[i]
            experiment = []
            for j in range(trialsPerAgent):
                if type['name'] == 'LinesNonUniform':            # Super hacky
                    type['args'] = distance
                ants = self.generateAnts(k, type)
                treasureLoc = self.selectTreasureLocation(distance)
                board = Board(treasureLoc, ants)
                self.drawProgressBar(current / float(totalNumExperiments))
                experiment.append(board.runAnts())
                current += 1
            results.append(experiment)
        return results

    def generateAnts(self, n, type):
        if type['name'] == "FKLS2":
            return self.generateUniformFKLSAnts(n, type['args'])
        elif type['name'] == "FKLS1":
            return self.generateNonUniformFKLSAnts(n)
        elif type['name'] == "LinesNonUniform":
            return self.generateNonUniformLinesAnts(n, type['args'])
        elif type['name'] == "LinesUniformInD":
            return self.generateUniformInDLinesAnts(n, type['args'])
        elif type['name'] == "HarmonicSearch":
            return self.generateHarmonicSearchAnts(n, type['args'])
        elif type['name'] == "LinesUniformInAll":
            return self.generateUniformInAllLinesAnts(n, type['args'])
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

    def generateNonUniformLinesAnts(self, n, D):
        return [LinesNonUniform((0,0), D) for i in range(n)]

    def generateUniformInDLinesAnts(self, n, K):
        return [LinesUniformInD((0,0), n, K) for i in range(n)]

    def generateUniformInAllLinesAnts(self, n, K):
        return [LinesUniformInAll((0,0), K) for i in range(n)]

    def generateHarmonicSearchAnts(self, n, delta):
        return [HarmonicSearch((0,0), delta) for i in range(n)]

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
        
