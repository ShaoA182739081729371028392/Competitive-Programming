'''
Solves an unweighted Bipartite Matching problem using Dinitz' algorithm with dead-end pruning.
'''
import copy
class LevelGraph():
  def __init__(self):
    self.edges = {}
    self.level = {}
    self.unique_nodes = []
  def neighbour_nodes(self, source):
    vals = []
    for A, B in self.edges:
      if A == source:
        vals += [B]
    return vals
  def in_edges(self, source, node):
    return (source, node) in self.edges or (node, source) in self.edges
  def backward_pass(self, sink):
    vals = []
    for A, B in self.edges:
      if B == sink:
        vals += [A]
    return vals
  def add_level(self, a, level):
    self.level[a] = level
  def get_level(self, a):
    if a in self.level:
      return self.level[a]
  def add_edge(self, a, b):
    self.edges[(a, b)] = True
    self.unique_nodes += [a]
    self.unique_nodes += [b]
    self.unique_nodes = list(set(self.unique_nodes))
class Graph():
  def __init__(self):
    self.capacity = {}
    self.flow = {}
  def add_connection(self, a, b, weight):
    self.capacity[(a, b)] = weight
    self.flow[(a, b)] = 0
  def update_flow(self, source, sink, flow):
    '''
    Adds the bottle neck capacity to the flow. If the source and sink is backward, it will subtract from the flow as required
    '''
    if (source, sink) in self.capacity:
      self.flow[(source, sink)] += flow
      return
    elif (sink, source) in self.capacity:
      self.flow[(sink, source)] -= flow
      return
    raise Exception("Something terribly wrong has occured. Please Try again.")
  def get_capacity_remaining(self, source, sink):
    '''
    Returns the remaining capacity for a given edge, even if it's backwards
    '''
    if (source, sink) in self.capacity:
      return self.capacity[(source, sink)] - self.flow[(source, sink)]
    elif (sink, source) in self.capacity:
      return self.flow[(sink, source)]
    raise Exception("Something terribly has gone wrong. Uh Oh! Please Try Again.")
  def neighbour_nodes(self, source):
    val = []
    for A, B in self.flow:
      if B == source:
        if self.flow[(A, B)] > 0:
          val += [A]
      elif A == source:
        if self.capacity[(A, B)] - self.flow[(A, B)] > 0:
          val += [B]
    return val
  def backward(self, source):
    '''
    Gets all of the backward nodes
    '''
    vals = []
    for A, B in self.flow:
      if B == source:
        if self.capacity[(A, B)] - self.flow[(A, B)] > 0:
          vals += [A]
    return vals
graph = Graph()
graph.add_connection('s', 'a', 10)
#graph.flow[('s', 'a')] = 10
graph.add_connection('s', 'b', 10)
graph.add_connection('a', 'b', 2)

graph.add_connection('a', 'c', 8)
graph.add_connection('b', 'c', 9)
graph.add_connection('a', 'd', 4)

graph.add_connection('c', 'd', 6)
graph.add_connection('d', 't', 10)
graph.add_connection('c', 't', 10)
class Queue():
  def __init__(self):
    self.queue = []
  def enqueue(self, a):
    self.queue += [a]
  def dequeue(self):
    val = self.queue[0]
    self.queue = self.queue[1: ]
    return val
  def empty(self):
    '''
    Returns if the queue is empty
    '''
    return len(self.queue) == 0


class BFS():
  '''
  Solves for a level graph using BFS
  '''
  def __init__(self, graph):
    self.graph = graph
  def BFS(self, source, sink):
    '''
    Solves for Level Graph. It is assumed that the sink is the last node to be reached with BFS
    '''
    levelGraph = LevelGraph()
    queue = Queue()
    queue.enqueue(source)
    levelGraph.add_level(source, 0)
    found = False
    while not queue.empty():
      value = queue.dequeue()
      possible = self.graph.neighbour_nodes(value)
      for node in possible:
        if node == sink:
          found = True
        if node not in levelGraph.level:
          queue.enqueue(node)
          levelGraph.add_edge(value, node)
          levelGraph.add_level(node, levelGraph.level[value] + 1)
        elif levelGraph.level[value] < levelGraph.level[node]:
          queue.enqueue(node)
          levelGraph.add_edge(value, node)
          levelGraph.add_level(node, levelGraph.level[value] + 1)
    if found:
      # Prune any nodes that don't reach the sink
      queue = Queue()
      queue.enqueue(sink)
      edges = {}
      unique_nodes = [sink]
      while not queue.empty():
        value = queue.dequeue()
        possible = levelGraph.backward_pass(value)
        for node in possible:
          edges[(node, value)] = True
          queue.enqueue(node)
          unique_nodes += [node]
      levelGraph.edges = edges
      levelGraph.unique_nodes = unique_nodes
      return levelGraph
    return None
class Solution():
  '''
  Solves the Graph problem with Dinitz Algorithm
  3 Steps:
  Repeat:
    1) Solve for Level graph using BFS
    2) Solves for all DFS paths
    3) Update flow
  '''
  def __init__(self, graph):
    self.graph = graph
  def DFS(self, levelGraph, source, sink, path, visited_nodes):
    possible = self.graph.neighbour_nodes(source)
    visited_nodes[source] = True
    for node in possible:
      if levelGraph.in_edges(source, node):
        if not visited_nodes[node]:
          if node == sink:
            return path + [(source, sink)], visited_nodes
          copied_path = copy.deepcopy(path) + [(source, node)]
          tmp_path, visited_nodes = self.DFS(levelGraph, node, sink, copied_path, copy.deepcopy(visited_nodes))
          if tmp_path != None:
            return tmp_path, visited_nodes
    return None, visited_nodes

  def max_flow(self, source, sink):
    while True:
      Bfs = BFS(self.graph)
      levelGraph = Bfs.BFS(source, sink)
      if levelGraph == None:
        # No Level graph available, so Dinitz Algorithm stops
        break
      while True:
        path = []
        visited_nodes = {}
        for node in levelGraph.unique_nodes:
          visited_nodes[node] = False
        path, _ = self.DFS(levelGraph, source, sink, path, visited_nodes)
        if path == None:
          # No more DFS used
          break
        else:
          # Update Weights with bottleneck value
          bottleneck = 999
          for SOURCE, SINK  in path:
            bottleneck = min(bottleneck, self.graph.get_capacity_remaining(SOURCE, SINK))
          for SOURCE, SINK in path:
            self.graph.update_flow(SOURCE, SINK, bottleneck)
class BipartiteMatching():
  '''
  Sets up the BipartiteMatching problem
  '''
  def __init__(self):
    self.graph = Graph() 
    self.A_nodes = []
    self.B_nodes = []
  def add_nodes(self, A_nodes, B_nodes):
    self.A_nodes = A_nodes
    self.B_nodes = B_nodes
    for node in A_nodes:
      self.graph.add_connection('s', node, 1)
    for node in B_nodes:
      self.graph.add_connection(node, 't', 1)
  def add_A_B_connection(self, A_node, B_node):
    assert A_node in self.A_nodes
    assert B_node in self.B_nodes
    self.graph.add_connection(A_node, B_node, 1)
  def solve(self):
    solver = Solution(self.graph)
    solver.max_flow('s', 't')
    return solver.graph.flow
Bipartite = BipartiteMatching()
Bipartite.add_nodes(['PersonA', 'PersonB', 'PersonC', 'PersonD', 'PersonE'], ['BookA', 'BookB', 'BookC', 'BookD', 'BookE'])

# Add connections
Bipartite.add_A_B_connection('PersonA', 'BookB')
Bipartite.add_A_B_connection('PersonA', 'BookC')

Bipartite.add_A_B_connection('PersonB', 'BookB')
Bipartite.add_A_B_connection('PersonB', 'BookC')
Bipartite.add_A_B_connection('PersonB', 'BookD')

Bipartite.add_A_B_connection('PersonC', 'BookA')
Bipartite.add_A_B_connection('PersonC', 'BookB')
Bipartite.add_A_B_connection('PersonC', 'BookC')
Bipartite.add_A_B_connection('PersonC', 'BookE')

Bipartite.add_A_B_connection('PersonD', 'BookC')

Bipartite.add_A_B_connection('PersonE', 'BookC')
Bipartite.add_A_B_connection('PersonE', 'BookD')
Bipartite.add_A_B_connection('PersonE', 'BookE')

print(Bipartite.solve())