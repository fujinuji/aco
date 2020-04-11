from random import randint

from Ant import Ant


class ACO:
    def __init__(self, params, probParams):
        self.__params = params
        self.__probParams = probParams
        self.__ants = []

    def initialize(self):
        self.__ants = []
        for _ in range(self.__probParams["noAnts"]):
            self.__ants.append(Ant(self.__params))

    def initializePheromone(self):
        for i in range(self.__params['noNodes']):
            v = [0.00001] * self.__params['noNodes']
            self.__params['local_pheromone_matrix'].append(v)
            self.__params['global_pheromone_matrix'].append(v)

    def explore(self):
        #self.__initializePheromoneMatrix()

        for _ in range(self.__params['noNodes'] - 1):
            for ant in self.__ants:
                ant.explore()
        self.fillWithPheromoneBestAnt(self.bestAnd())

    def bestAnd(self):
        bestAnt = self.__ants[0]

        for ant in self.__ants:
            if ant.distance() < bestAnt.distance():
                bestAnt = ant
        return bestAnt

    def fillWithPheromoneBestAnt(self, ant):
        path = ant.path()
        distance = ant.distance()

        for i in range(len(path) - 1):
            x = path[i]
            y = path[i + 1]
            self.__params['global_pheromone_matrix'][x][y] = (1 - self.__params['pheromone_persistence']) * self.__params['global_pheromone_matrix'][x][y] + self.__params['pheromone_persistence'] * (1 / distance)
            self.__params['global_pheromone_matrix'][y][x] = self.__params['global_pheromone_matrix'][x][y]

    def initializePheromoneMatrix(self):
        self.__params['local_pheromone_matrix'] = []
        for i in range(0, self.__params['noNodes']):
            v = [0] * self.__params['noNodes']
            self.__params['local_pheromone_matrix'].append(v)

        for i in range(0, self.__params['noNodes']):
            for j in range(0, self.__params['noNodes']):
                self.__params['local_pheromone_matrix'][i][j] = self.__params['global_pheromone_matrix'][i][j]

    def getBestPath(self):
        path = []
        current = 0
        distance = 0
        for i in range(0, self.__params['noNodes']):
            best = 0
            valB = 0
            for j in range(0, self.__params['noNodes']):
                if self.__params['global_pheromone_matrix'][current][j] > valB and j not in path:
                    valB = self.__params['global_pheromone_matrix'][current][j]
                    best = j
            path.append(best)
            distance += self.__params['matrix'][current][best]
            current = best
        path.append(path[0])
        distance += self.__params['matrix'][path[-1]][path[-2]]

        return [path, distance]

    def perturbation(self):
        x = randint(0, self.__params['noNodes'] - 1)
        y = randint(0, self.__params['noNodes'] - 1)

        while x == y and self.__params['matrix'][x][y] == 0:
            y = randint(0, self.__params['noNodes'] - 1)

        print ("Make perturbation: delete edge between:" + str(x) + " and " + str(y))

        self.__params['matrix'][x][y] = 0
        self.__params['matrix'][y][x] = 0

        self.__params['global_pheromone_matrix'][x][y] = 0
        self.__params['global_pheromone_matrix'][y][x] = 0

