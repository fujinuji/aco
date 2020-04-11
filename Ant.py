from random import randint, uniform


class Ant:
    def __init__(self, params):
        self.__params = params
        self.__path = []
        self.__visited = [False] * params['noNodes']
        self.__initialize()
        self.__isBadAnt = False

    def __initialize(self):
        self.__path.append(randint(0, self.__params['noNodes'] - 1))
        self.__visited[self.__path[0]] = True

    def distance(self):
        if self.__isBadAnt:
            return 999999
        distance = 0

        for i in range(len(self.__path) - 1):
            distance += self.__params['matrix'][self.__path[i]][self.__path[i + 1]]
        distance += self.__params['matrix'][self.__path[len(self.__path) - 1]][self.__path[0]]

        return distance

    def __nextNode(self):
        q = uniform(0, 1)
        current_node = self.__path[len(self.__path) - 1]

        if q < self.__params["q0"]:
            something = []
            for i in range(len(self.__params['local_pheromone_matrix'][current_node])):
                if i != current_node and not self.__visited[i] and not self.__params['matrix'][current_node][i] == 0:
                    rapport = pow(self.__params['local_pheromone_matrix'][current_node][i], self.__params["alpha"]) / \
                              pow(1 / self.__params['matrix'][current_node][i], self.__params["beta"])
                    something.append((rapport, i))

            something.sort(reverse=True)

            # The ant may have a deadlock (even if there are other nodes to visit, there is no way to escape from
            # current node)
            if len(something) == 0:
                raise Exception("Id bad and")
            return something[0][1]
        else:
            sum = 0
            something = []
            for i in range(0, self.__params['noNodes']):
                if not self.__visited[i] and i != current_node and not self.__params['matrix'][current_node][i] == 0:
                    sum += pow(self.__params['local_pheromone_matrix'][current_node][i], self.__params["alpha"]) / \
                           pow(1 / self.__params['matrix'][current_node][i], self.__params["beta"])

            for j in range(0, self.__params['noNodes']):
                if not self.__visited[j] and j != current_node and not self.__params['matrix'][current_node][j] == 0:
                    rapport = self.__params['local_pheromone_matrix'][current_node][j] / \
                              self.__params['matrix'][current_node][j]
                    something.append((rapport / sum, j))

            something.sort(reverse=True)

            for i in range(len(something)):
                for j in range(i + 1, len(something)):
                    something[i] = (something[i][0] + something[j][0], something[i][1])

            prob = uniform(0, 1)

            for i in range(len(something) - 1):
                if something[i][0] <= prob < something[i + 1][0]:
                    return something[i][1]

            # The ant may have a deadlock (even if there are other nodes to visit, there is no way to escape from
            # current node) => it is a bad ant
            if len(something) == 0:
                raise Exception("Is bad ant")
            return something[len(something) - 1][1]

    def explore(self):
        try:
            next_node = self.__nextNode()
        except:
            self.__isBadAnt = True
            return

        current_node = self.__path[len(self.__path) - 1]
        self.__visited[next_node] = True
        self.__path.append(next_node)

        self.__params['local_pheromone_matrix'][current_node][next_node] = (1 - self.__params[
            "pheromone_persistence"]) * self.__params["local_pheromone_matrix"][current_node][next_node] + \
                                                                           self.__params[
                                                                               "pheromone_persistence"] * (0.00001)
        self.__params['local_pheromone_matrix'][next_node][current_node] = \
            self.__params['local_pheromone_matrix'][current_node][next_node]

    def path(self):
        return self.__path
