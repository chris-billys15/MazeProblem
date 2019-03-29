#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

"""The labyrinth has no walls, but pits surround the path on each side. If a players falls into a pit, they lose. The labyrinth is presented as a matrix (a list of lists): 1 is a pit and 0 is part of the path. The labyrinth's size is 12 x 12 and the outer cells are also pits. Players start at cell (1,1). The exit is at cell (10,10). You need to find a route through the labyrinth. Players can move in only four directions--South (down [1,0]), North (up [-1,0]), East (right [0,1]), West (left [0, -1]). The route is described as a string consisting of different characters: "S"=South, "N"=North, "E"=East, and "W"=West.

Input: A labyrinth's map. A list of lists with 1 and 0.

Output: A route. A string that contain "W", "E", "N" and "S".

How it is used: This is a classical problem for path-finding in graphs -- Yes, the maze can be represented as a graph. It can be used in navigation software for a to b navigation and computer games for artificial intelligence. You can find your way anywhere you wish. Just divide a map into square cells and mark up the "bad" cells.

Precondition: Outer cells are pits.
|labyrinth| = 12 x 12

The solution presented here is very generic.
It features a Edge, Node, Graph and Astar class that can be re-used as-is, also for other graph and path-finding problems. There is no assumption on the shape of the maze. It may be a different size, and does not need the '1' boundary.
"""

from collections import UserList

class Edge(object):
    """An edge is a unidirectional link between two nodes in a graph."""
    def __init__(self, source, destination, ref=None, weight=0):
        self.source = source
        self.destination = destination
        self.ref = ref
        self.weight = weight
    def __str__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, str(self.source), str(self.destination))
    def __repr__(self):
        return "%s(%s, %s, %s, %s)" % (self.__class__.__name__, str(self.source), str(self.destination), self.ref, self.weight)

class Node(object):
    """A node (or vertex) in a graph."""
    def __init__(self, ref=None, weight=0, edges=[]):
        self.ref = ref
        self.weight = weight
        self.edges = edges[:]
    def add_edge(self, neighbour, ref=None, weight=0):
        self.edges.append(Edge(self, neighbour, ref, weight))
    def add_bidirectional_edge(self, neighbour, ref=None, weight=0):
        self.add_edge(neighbour, ref, weight)
        neighbour.add_edge(self, ref, weight)
    def neigbours(self):
        return [edge.destination for edge in self.edges]
    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, str(self.ref))
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, str(self.ref))
        # return "%s(%s, %s)" % (self.__class__.__name__, str(self.ref), self.weight)
    
class Graph(UserList):
    """A graph is a list of nodes, which have associated edges."""
    def __init__(self):
        UserList.__init__(self)
        self._noderefs = {}
    def add_node(self, ref=None, weight=0):
        n = Node(ref=ref, weight=weight)
        if ref != None:
            self._noderefs[ref] = n
        self.append(n)
    def get_node(self, ref):
        return self._noderefs[ref]


class NoPath(Exception):
    """Raised if not path exists between a given source and destination"""
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
    def __str__(self):
        return "No path exists between %s and %s." % (self.source, self.destination)

class Astar(object):
    """Implmentation of the A* shortest path finding algorithm. 
    This is a variant of Edsgar W. Dijkstra's shortest path algorithm, with 
    a heuristic based on the mimimum distance between two points."""
    def heuristic_cost_estimate(node1, node2):
        """Heuristic method that returns a lower boundary of the.
        In case this function always returns 0, the A* algorithm is the same 
        as the Dijkstra algorithm."""
        return 0
    def __init__(self, graph, start, destination, heuristic_cost_function=heuristic_cost_estimate):
        self.graph = graph # list of nodes
        self.path = []
        self.mincost = {}       # node: minumum cost from start to 'node'
        self.minpathcost = {}   # node: minimum cost from start via 'node' to destination
        self.prev = {}          # node: previous node for minimum cost path
        self.path = None
        self.cost = None
        self.iterations = 0
        self.heurist_lower_boundary_fn = heuristic_cost_function
        self.shortestpath(start, destination)
    def shortestpath(self, start, destination):
        """Calculate a shortest path"""
        print(self.graph)
        print("find a path", start, "-->", destination)
        queue = [start]
        self.prev[start] = None
        self.mincost[start] = start.weight
        self.minpathcost[start] = start.weight + self.heurist_lower_boundary_fn(start, destination)
        while True:
            self.iterations += 1
            queue.sort(key = lambda n: self.minpathcost[n])
            # print("queue:",queue)
            if len(queue) == 0:
                raise NoPath(start, destination)
            node = queue.pop(0)
            if node == destination:
                self.setsolution(destination)
                return
            curcost = self.mincost[node]
            # print("node:",node,"cost:",curcost)
            for edge in node.edges:
                neighbour = edge.destination
                cost = edge.weight + neighbour.weight
                totalcost = curcost + cost
                if (neighbour in self.mincost) and (totalcost >= self.mincost[neighbour]):
                    # print("skip %s (%d >= %d)" % (neighbour, totalcost, self.mincost[neighbour]))
                    continue
                self.mincost[neighbour] = totalcost
                self.minpathcost[neighbour] = totalcost + self.heurist_lower_boundary_fn(neighbour, destination)
                self.prev[neighbour] = edge
                # print("append %s (prev: %s, cost: %d)" % (neighbour, node, totalcost))
                # prepend instead of append: A* works best for LIFO queues
                queue.insert(0, neighbour)
    def setsolution(self, destination):
        self.cost = self.mincost[destination]
        # path is a list of edges
        # hops is a list of nodes
        self.path = []
        self.hops = [destination]
        edge = self.prev[destination]
        while edge != None:
            self.path = [edge] + self.path
            self.hops = [edge.source] + self.hops
            edge = self.prev[edge.source]
    

def maze_to_graph(maze_map):
    """Translate the matrix-defined maze into a Graph object."""
    graph = Graph()
    # create nodes
    for i, row in enumerate(maze_map):
        print("%2d" % i,":"," ".join([str(n) for n in row]))
        for j, n in enumerate(row):
            if n == 1: # a wall
                continue
            graph.add_node((i,j))
    # create edges
    for i, row in enumerate(maze_map):
        for j, n in enumerate(row):
            try:
                node = graph.get_node((i,j))
            except KeyError:
                continue
            for di,dj,move in ((1,0,"S"), (-1,0,"N"), (0,-1,"W"), (0,1,"E")):
                try:
                    neighbour = graph.get_node((i+di,j+dj))
                except KeyError:
                    continue
                # print("Add edge %s -> %s (move=%s, weight=1)" % (node, neighbour, move))
                node.add_edge(neighbour, ref=move, weight=1)
    start = graph.get_node((1,1))
    i = len(maze_map)
    j = len(maze_map[-2])
    destination = graph.get_node((i-2,j-2))
    return graph, start, destination

def planar_coord_distance(node1, node2):
    """Heuristic method that returns a lower boundary of the distance
    between node1 and node2."""
    return abs(node1.ref[0] - node2.ref[0]) + abs(node1.ref[1] - node2.ref[1])

def checkio(maze_map):
    g, start, destination = maze_to_graph(maze_map)
    a = Astar(g, start, destination, heuristic_cost_function=planar_coord_distance)
    instructions = "".join([edge.ref for edge in a.path])
    print(a.iterations,"iterations")
    print("cost",a.cost)
    print (instructions)
    return instructions


if __name__ == '__main__':
    #This code using only for self-checking and not necessary for auto-testing
    def check_route(func, labyrinth):
        MOVE = {"S": (1, 0), "N": (-1, 0), "W": (0, -1), "E": (0, 1)}
        #copy maze
        route = func([row[:] for row in labyrinth])
        pos = (1, 1)
        goal = (10, 10)
        for i, d in enumerate(route):
            move = MOVE.get(d, None)
            if not move:
                print("Wrong symbol in route")
                return False
            pos = pos[0] + move[0], pos[1] + move[1]
            if pos == goal:
                if i+1 == len(route):
                    return True
                else:
                    print("Route continuous after reaching the goal")
                    return False
            if labyrinth[pos[0]][pos[1]] == 1:
                print("Player in the pit")
                return False
        print("Player did not reach exit")
        return False

    # These assert are using only for self-testing as examples.
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1],
        [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "First maze"
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "Empty maze"
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "Up and down maze"
    assert check_route(checkio, [
        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]]), "Up and down maze, no boundaries"
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "Dotted maze"
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "Need left maze"
    assert check_route(checkio, [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]), "The big dead end."
    print("The local tests are done.")