import random
import math
import copy
# Class to Organize the Value of the Graph
class WeightedGraph():
  def __init__(self):
    self.weighted_graph = {}
    self.connections = []
  def add_connection(self, a, b, weight):
    # Adds a Weighted Connection in the Graph
    self.weighted_graph[(a, b)] = weight
    self.weighted_graph[(b, a)] = 0
    self.connections += [(a, b)]
# Create a Sample Graph
graph = WeightedGraph()
graph.add_connection((1,), (5,), 3)
graph.add_connection((1,), (2,), 2)
graph.add_connection((5,), (2,), 2)
graph.add_connection((2,), (6,), 2)

graph.add_connection((2,), (3,), 3)
graph.add_connection((6,), (7,), 1)
graph.add_connection((3,), (7,), 2)
graph.add_connection((3,), (4,), 4)

graph.add_connection((7,), (4,), 2)
graph.add_connection((7,), (8,), 3)
graph.add_connection((4,), (8,), 2)
graph.add_connection((5,), (6,), 3)
class StoerWagner():
  def __init__(self, weightedGraph):
    self.weighted_graph = weightedGraph
  def in_arr(self, arr, Val_To_Search):
    Array = []
    for a, b in arr:
      if a== Val_To_Search:
        Array += [(a, b)]
      elif b == Val_To_Search:
        Array += [(a, b)]
    return Array
  def remove_element(self, arr, thing_to_remove):
    new = []
    for i in arr:
      if i != thing_to_remove:
        new += [i]
    return new
  def find_max_node(self, nodes):
    max_node = None
    max_val = 0
    for node in nodes:
      if self.weighted_graph.weighted_graph[node] > max_val:
        max_val = self.weighted_graph.weighted_graph[node]
        max_node = node
    return max_node
  def combine_nodes(self, A, B):
    vals = []
    for i in A:
      vals += [i]
    for i in B:
      vals += [i]
    return tuple(vals)
  def get(self, arr, A):
    vals = []
    for a, b in arr:
      if a== A:
        vals += [(a, b)]
      elif b == A:
        vals += [(b, a)]
    return vals
  def common_nodes(self, A, B):
    A_nodes = self.get(self.weighted_graph.connections, A)
    B_nodes = self.get(self.weighted_graph.connections, B)
    total = {}
    self.weighted_graph.weighted_graph[(A, B)] = 0
    self.weighted_graph.connections = self.remove_element(self.weighted_graph.connections, (A, B))
    for _, a in A_nodes:
      for _, b in B_nodes:
        if a == b:
          val = 0
          val += self.weighted_graph.weighted_graph[(A, a)]
          self.weighted_graph.weighted_graph[(A, a)] = 0
          val += self.weighted_graph.weighted_graph[(a, A)]
          self.weighted_graph.weighted_graph[(a,A)] = 0
          self.weighted_graph.connections = self.remove_element(self.weighted_graph.connections, (A, a))
          self.weighted_graph.connections = self.remove_element(self.weighted_graph.connections, (a, A))

          val += self.weighted_graph.weighted_graph[(B, a)]
          self.weighted_graph.weighted_graph[(B, a)] = 0
          val += self.weighted_graph.weighted_graph[(a, B)]
          self.weighted_graph.weighted_graph[(a,B)] = 0
          self.weighted_graph.connections = self.remove_element(self.weighted_graph.connections, (B, a))
          self.weighted_graph.connections = self.remove_element(self.weighted_graph.connections, (a, B))
          total[a] = val
    return total
  def minCut(self, topCornerLeftNumber):
    '''
    topCornerLeftNumber: int(), top corner number used, where the minCut Starts
    returns the minimum Cut(s)
    The return value is one grou
    '''
    cuts = {}
    cur_super_node = (topCornerLeftNumber,)
    while len(self.weighted_graph.connections) > 2:
      values = self.in_arr(self.weighted_graph.connections, cur_super_node)
      max_node = self.find_max_node(values)
      A, B = max_node
      cur_super_node = self.combine_nodes(A, B)
      total = self.common_nodes(A, B)
      for a in total:
        self.weighted_graph.add_connection(cur_super_node, a, total[a])
      in_B = self.in_arr(self.weighted_graph.connections, B)
      in_A = self.in_arr(self.weighted_graph.connections, A)
      for a, b in in_A:
        if a == A:
          self.weighted_graph.add_connection(cur_super_node, b, self.weighted_graph.weighted_graph[(a, b)])
          self.weighted_graph.weighted_graph[(a, b)] = 0
          self.weighted_graph.connections = self.remove_element(self.weighted_graph.connections, (a, b))
        else:
          self.weighted_graph.add_connection(cur_super_node, a, self.weighted_graph.weighted_graph[(a, b)])
          self.weighted_graph.weighted_graph[(a, b)] = 0
          self.weighted_graph.connections = self.remove_element(self.weighted_graph.connections, (a, b))
      for a, b in in_B:
        if a == B:
          self.weighted_graph.add_connection(cur_super_node, b, self.weighted_graph.weighted_graph[(a, b)])
          self.weighted_graph.weighted_graph[(a, b)] = 0
          self.weighted_graph.connections = self.remove_element(self.weighted_graph.connections, (a, b))
        else:
          self.weighted_graph.add_connection(cur_super_node, a, self.weighted_graph.weighted_graph[(a, b)])
          self.weighted_graph.weighted_graph[(a, b)] = 0
          self.weighted_graph.connections = self.remove_element(self.weighted_graph.connections, (a, b))
      counted = self.count_cut(cur_super_node)
      group = self.group(cur_super_node)
      cuts[(cur_super_node, group)] = counted
    # Compute Min Vals
    min_cuts = []
    min_val = 999
    for i in cuts:
      if cuts[i] <= min_val:
        min_val = cuts[i]
    for i in cuts:
      if cuts[i] == min_val:
        min_cuts += [i]
    return min_cuts
  def group(self, super_node):
    '''
    Groups the for final cut
    '''
    all = []
    for A, B in self.weighted_graph.connections:
      for a in A:
        all += [a]
      for b in B:
        all += [b]
    all = list(set(all))
    group2 = []
    for i in all:
      if i not in super_node:
        group2 += [i]
    return tuple(group2)
  def count_cut(self, super_node):
    '''
    Computes the cut from the super_node
    '''
    in_super = self.in_arr(self.weighted_graph.connections, super_node)
    total = 0
    for i in in_super:
      total += self.weighted_graph.weighted_graph[i]
    return total
      

    

stoerWagner = StoerWagner(graph)
print(stoerWagner.minCut(1))

