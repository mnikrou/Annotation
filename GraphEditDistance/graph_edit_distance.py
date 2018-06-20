# -*- coding: UTF-8 -*-

from .munkres import Munkres
import sys
import math


def compareGraphs(g1, g2):
    m = Munkres()
    cost_matrix = create_cost_matrix(g1, g2)
    print_matrix(cost_matrix)
    index = m.compute(cost_matrix)
    costs = [cost_matrix[i][j] for i, j in index]
    distance = sum(costs) / g1.size()
    print(str(distance) + ' - ' + str(costs))
    return distance


def substitute_cost(node1, node2):
    if node1.equals(node2):
        return 0
    return euclidean_distance(node1, node2)


def delete_cost():
    return 1000


def insert_cost():
    return 1000


def euclidean_distance(node1, node2):
    return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)


def create_cost_matrix(g1, g2):
    n = g1.size()
    m = g2.size()
    cost_mat = [[0 for i in range(n + m)] for j in range(n + m)]

    nodes1 = g1.get_nodes()
    nodes2 = g2.get_nodes()

    for i in range(n):
        for j in range(m):
            cost_mat[i][j] = substitute_cost(nodes1[i], nodes2[j])

    for i in range(m):
        for j in range(m):
                cost_mat[i + n][j] = float('inf')

    for i in range(n):
        for j in range(n):
                cost_mat[j][i + m] = float('inf')

    return cost_mat


def print_matrix(matrix):
    print ("cost matrix:")
    print(
        '\n'.join([''.join(['{:10.4f}'.format(item) for item in row]) for row in matrix]))
