from ACO import ACO
from Utils import readData, read_berlin, showNetwork

file = "data/hardE.txt"

#params = readData(file)
params = read_berlin(file)

probParams = {"noAnts": 100, "generations": 50, "perturbationStep": 2000}
params['local_pheromone_matrix'] = []
params['global_pheromone_matrix'] = []
params['q0'] = 0.2
params['alpha'] = 1
params['beta'] = 5
params['pheromone_persistence'] = 0.5

aco = ACO(params, probParams)
aco.initialize()
aco.initializePheromone()

best_ant = None
aco.initializePheromone()
for i in range(1, probParams['generations']):
    aco.explore()
    bestAnt = aco.bestAnd()
    print ("Gen " + str(i) + ": best ant: " + str(bestAnt.distance()) + " with path " + str(bestAnt.path()))

    if best_ant == None or bestAnt.distance() < best_ant.distance():
        best_ant = bestAnt

    if i % probParams['perturbationStep'] == 0:
        aco.perturbation()

    aco.initialize()

showNetwork(params['matrix'])
print ("Gen OVERALL best ant: " + str(best_ant.distance()) + " with path " + str(best_ant.path()))
[path, distance] = aco.getBestPath()
print ("Gen OVERALL pheromone: " + str(distance) + " with path " + str(path))