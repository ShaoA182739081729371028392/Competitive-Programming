# Computes the Strongly Connected Components of a Graph
class Graph():
  def __init__(self):
    self.edges = {}
    self.nodes = []
  def add_connection(self, a, b):
    self.edges[(a, b)] = True
    self.nodes += [a]
    self.nodes += [b]
    self.nodes = list(set(self.nodes))
# Generate Sample Graph
graph = Graph()
graph.add_connection((1, ), (7, ))
graph.add_connection((7, ), (4, ))
graph.add_connection((4, ), (1, ))
graph.add_connection((7, ), (9, ))

graph.add_connection((9, ), (6, ))
graph.add_connection((6, ), (3, ))
graph.add_connection((3, ), (9, ))
graph.add_connection((6, ), (8, ))

graph.add_connection((8, ), (2, ))
graph.add_connection((2, ), (5, ))
graph.add_connection((5, ), (8, ))
class Stack():
  def __init__(self):
    self.stack = []
  def enqueue(self, val):
    self.stack = self.stack + [val]
  def dequeue(self):
    val = self.stack[-1]
    self.stack = self.stack[:-1]
    return val
  def empty(self):
    return len(self.stack) == 0
  def clear(self):
    self.stack = []


class Solution():
  def __init__(self, graph):
    self.stack = Stack()
    self.graph = graph
  def connected(self, start_node, reverse = False):
    possible = []
    for A, B in self.graph.edges:
      if reverse:
        if B == start_node:
          possible += [A]
      else:
        if A == start_node:
          possible += [B]
    return possible
  def DFS(self, start_node, searched_nodes, map_node, highest_val):
    '''
    Runs DFS on the nodes 
    '''
    possible = self.connected(start_node, reverse = True)
    searched_nodes[start_node] = True
    for node in possible:
      if not searched_nodes[node]:
        searched_nodes, map_node, highest_val = self.DFS(node, searched_nodes, map_node, highest_val)
    map_node[start_node] = highest_val
    highest_val -= 1
    return searched_nodes, map_node, highest_val
  def DFS_tmp(self, start_node, searched_nodes):
    possible = self.connected(start_node)
    searched_nodes[start_node] = True
    for node in possible:
      if not searched_nodes[node]:
        searched_nodes = self.DFS_tmp(node, searched_nodes)
    
    return searched_nodes
  def DFS_SCC(self, start_node, global_searched_nodes):
    '''
    Computes searched_nodes
    '''
    possible = self.connected(start_node)
    already_searched = {}
    for node in global_searched_nodes:
      if global_searched_nodes[node]:
        already_searched[node] = True  
    for node in possible:
      global_searched_nodes = self.DFS_tmp(node, global_searched_nodes)
    SCC = []
    for node in global_searched_nodes:
      if global_searched_nodes[node] and node not in already_searched:
        SCC += [node]
    return global_searched_nodes, SCC
  
  def SCC(self):
    '''
    Computes the strongly connected components of the graph
    '''
    searched_nodes = {}
    highest_node = 0
    global_searched_nodes = {}
    for i in self.graph.nodes:
      searched_nodes[i] = False
      highest_node += 1
      global_searched_nodes[i] = False
    top_val = highest_node
    map_node = {}
    int_map = {}
    for node in searched_nodes:
      if not searched_nodes[node]:
        searched_nodes, map_node, highest_node = self.DFS(node, searched_nodes, map_node, highest_node)
    # Should have a mapping for every node at this point, but they are not in sorted order
    for node in map_node:
      int_map[map_node[node]] = node
    SCC = []
    for i in range(1, top_val):
      node = int_map[i]
      if not global_searched_nodes[node]:
        global_searched_nodes, tmp_SCC = self.DFS_SCC(node, global_searched_nodes)
        SCC += [tmp_SCC]
    return SCC
solution = Solution(graph)
print(solution.SCC())