# This file uses Depth-First Search to solve the Topological Sorting Problem
class Graph():
  def __init__(self):
    self.directed_connections = {}
    self.unique_nodes = []
  def add_connection(self, a, b):
    self.directed_connections[(a, b)] = 1
    self.unique_nodes += [a]
    self.unique_nodes += [b]
    self.unique_nodes = list(set(self.unique_nodes))
  def empty(self):
    return len(self.unique_nodes) == 0
class Stack():
  def __init__(self):
    self.stack = []
  def enstack(self, val):
    self.stack += [val]
  def destack(self):
    val = self.stack[-1]
    self.stack = self.stack[0: -1]
    return val
class Solution():
  def __init__(self, graph):
    self.graph = graph
  def nodes_connected(self, start_node):
    vals = []
    for A, B in self.graph.directed_connections:
      if start_node == A:
        vals += [(A, B)]
    return vals
  def DFS(self, start_node, searched_nodes, current_number):
    vals = []
    for _, node in self.nodes_connected(start_node):
      if not searched_nodes[node]:
        searched_nodes, current_number, values = self.DFS(node, searched_nodes, current_number)
        vals += values
    vals += [{start_node: current_number}]
    current_number -= 1
    searched_nodes[start_node] = True
    return searched_nodes, current_number, vals

  def topological_sort(self):
    '''
    Returns a topologically sorted graph, in a list:
    Performs this using DFS
    Returns: List({key: int})
    '''
    searched_nodes = {}
    vals = []
    for node in self.graph.unique_nodes:
      searched_nodes[node] = False
    cur_val = len(self.graph.unique_nodes)
    for node in self.graph.unique_nodes:
      if not searched_nodes[node]:
        searched_nodes, cur_val, values= self.DFS(node, searched_nodes, cur_val)
        vals += values

    return vals 



graph = Graph()
graph.add_connection(('a',), ('b', ))
graph.add_connection(('a',), ('c', ))
graph.add_connection(('c',), ('d', ))
graph.add_connection(('b',), ('d', ))
graph.add_connection(('d',), ('e', ))
# Answer: [a, b, c, d, e]
# or [a, c, b, d, e]
solution = Solution(graph)
print(solution.topological_sort())