import copy
import math
import random
import time
class Graph():
  def __init__(self):
    self.nodes = {}
    self.edges = []
  def add_nodes(self, nodes):
    for i in nodes:
      for j in nodes:
        self.nodes[((i,), (j,))] = 0
  def add_edge(self, a, b):
    self.nodes[((a,), (b,))] += 1
    self.nodes[((b,), (a,))] += 1
    self.edges += [((a,), (b,))]
class Solver():
  def __init__(self, graph):
    '''
    This graph should be full
    '''
    self.graph = graph
  def remove_from_list(self, arr, val):
    valz = []
    for i in arr:
      if i != val:
        valz += [i]
    return valz
  def compute_unique_nodes(self):
    unique_vals = []
    for a, b in self.graph.edges:
      unique_vals += [a]
      unique_vals += [b]
    return len(set(unique_vals))
  def min_cut(self):
    '''
    Solves for Minimum Cut of the Algorithm
    '''
    while self.compute_unique_nodes() > 2:
      A, B = self.graph.edges[random.randint(0, len(self.graph.edges)-1)] # (A, B)
      self.graph.nodes[(A, B)] = 0
      self.graph.nodes[(B, A)] = 0
      while (A, B) in self.graph.edges:
        self.graph.edges = self.remove_from_list(self.graph.edges, (A, B))
      while (B, A) in self.graph.edges:
        self.graph.edges = self.remove_from_list(self.graph.edges, (B, A))
      new_super_node = []
      for i in A:
        new_super_node += [i]
      for i in B:
        new_super_node += [i]
      super_node = tuple(new_super_node)
      for C, D in self.graph.edges:
        if C == A:
          self.graph.nodes[(C, D)] = 0 
          self.graph.nodes[(D, C)] = 0 
          while (C, D) in self.graph.edges:
            self.graph.edges = self.remove_from_list(self.graph.edges, (C, D))
          
          if (super_node, D) in self.graph.nodes:
            self.graph.nodes[(super_node, D)] += 1
          else:
            self.graph.nodes[(super_node, D)] = 1
          self.graph.edges += [(super_node, D)]
        elif C == B:
          self.graph.nodes[(C, D)] = 0
          self.graph.nodes[(D, C)] = 0 
          while (C, D) in self.graph.edges:
            self.graph.edges = self.remove_from_list(self.graph.edges, (C, D))
          
          if (super_node, D) in self.graph.nodes:
            self.graph.nodes[(super_node, D)] += 1
          else:
            self.graph.nodes[(super_node, D)] = 1
          self.graph.edges += [(super_node, D)]
        elif D == A:
          self.graph.nodes[(C, D)] = 0 
          self.graph.nodes[(D, C)] = 0
          while (C, D) in self.graph.edges:
            self.graph.edges = self.remove_from_list(self.graph.edges, (C, D))
          
          if (C, super_node) in self.graph.nodes:
            self.graph.nodes[(C, super_node)] += 1
          else:
            self.graph.nodes[(C, super_node)] = 1
          self.graph.edges += [(C, super_node)]
        elif D == B:
          self.graph.nodes[(C, D)] = 0
          self.graph.nodes[(D, C)] = 0 
          while (C, D) in self.graph.edges:
            self.graph.edges = self.remove_from_list(self.graph.edges, (C, D))
          
          if (C, super_node) in self.graph.nodes:
            self.graph.nodes[(C, super_node)] += 1
          else:
            self.graph.nodes[(C, super_node)] = 1
          self.graph.edges += [(C, super_node)]
    


      




graph = Graph()
graph.add_nodes(['a', 'b', 'c', 'd', 'e'])
graph.add_edge('a', 'b')
graph.add_edge('d', 'b')
graph.add_edge('a', 'd')
graph.add_edge('a', 'c')
graph.add_edge('c', 'd')
graph.add_edge('d', 'e')
graph.add_edge('c', 'e')
solver = Solver(graph)
solver.min_cut()
print(solver.graph.edges)
print(solver.graph.nodes)