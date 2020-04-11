import warnings
from math import sqrt

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def readData(file_name):
    params = {}

    costs = []
    file = open(file_name, "r")
    n = int(file.readline())
    for i in range(n):
        line = file.readline()
        costs.append(list(line.strip().split(",")))

    for row in costs:
        for i in range(len(row)):
            row[i] = int(row[i])

    file.close()
    params["noNodes"] = n
    params["matrix"] = costs
    return params

def read_berlin(fileName):
    params = {}
    coordinates = []
    with open(fileName) as f:
        number = int(f.readline())
        for n in range(number):
            coordinates.append(f.readline().strip().split(" "))
    cities = []

    for n in range(number):
        line = []
        for i in range(number):
            p1 = (float(coordinates[n][1]), float(coordinates[n][2]))
            p2 = (float(coordinates[i][1]), float(coordinates[i][2]))
            line.append(calcDistance( p1, p2))
        cities.append(line)

    params["noNodes"] = number
    params["matrix"] = cities

    return params

def calcDistance(p1,p2):
    x = (p1[0] - p2[0])
    y = (p1[1] - p2[1])
    return sqrt(pow(x, 2) + pow(y,2))

def showNetwork(network):
    warnings.simplefilter('ignore')
    A = np.matrix(network)
    G = nx.from_numpy_matrix(A)
    pos = nx.spring_layout(G)  # compute graph layout
    for edge in G.edges:
        if network[edge[0]][edge[1]] == 0:
            del edge
    plt.figure(figsize=(4, 4))  # image is 8 x 8 inches
    nx.draw_networkx_nodes(G, pos, node_size=600, cmap=plt.cm.RdYlGn)
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    plt.show()
