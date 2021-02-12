'''
Tasks for Maze Solving:
BFS:
- Connectvity
- Shortest Path
'''
class Graph():
  def __init__(self):
    self.nodes = {}
    self.direct_nodes = {}
    self.unique_nodes = []
  def add_connection(self, a, b):
    self.nodes[(a, b)] = True
    self.nodes[(b, a)] = True
    self.direct_nodes[(a, b)] = True
    self.unique_nodes += [a]
    self.unique_nodes += [b]
    self.unique_nodes = list(set(self.unique_nodes))

# Create Sample Graph
graph = Graph()
graph.add_connection(('a', ), ('b', ))
graph.add_connection(('a', ), ('c', ))
graph.add_connection(('c', ), ('d', ))
graph.add_connection(('b', ), ('e', ))
graph.add_connection(('e', ), ('f', ))
graph.add_connection(('d', ), ('f', ))

graph.add_connection(('f', ), ('a', )) # Creates a Cycle in the Graph
graph.add_connection(('g', ), ('h', ))
graph.add_connection(("i", ), ('j', ))
class Queue():
  def __init__(self):
    self.queue = []
  def enqueue(self, val):
    self.queue += [val]
  def dequeue(self):
    val = self.queue[0]
    self.queue = self.queue[1: ]
    return val
  def empty(self):
    if len(self.queue) == 0:
      return True
    return False
  def in_queue(self, x):
    return x in self.queue
  def clear(self):
    self.queue = []
class BFS():
  def __init__(self, graph):
    self.graph = graph
    self.queue = Queue()
  def bfs_connectivity(self, start_node, searched_nodes):
    self.queue.enqueue(start_node)
    vals = []
    while not self.queue.empty():
      cur_node = self.queue.dequeue()
      searched_nodes[cur_node] = True
      possible = self.connected(cur_node, searched_nodes)
      for found in possible:
        self.queue.enqueue(found)
      vals += [cur_node]
    return list(set(vals)), searched_nodes

  def connected(self, start_node, searched_nodes):
    vals = []
    for i in self.graph.nodes:
      A, B = i
      if A == start_node and not searched_nodes[B] and not self.queue.in_queue(B):
        vals += [B]
      elif B == start_node and not searched_nodes[A] and not self.queue.in_queue(A):
       vals += [A]
    return vals
  def direct_connected(self, start_node, searched_nodes):
    vals = []
    for i in self.graph.direct_nodes:
      A, B = i
      if A == start_node and not self.queue.in_queue(B):
        vals += [B]
    return vals
  def connectivity(self):
    groups = []
    nodes_explored = {}
    for i in self.graph.unique_nodes:
      nodes_explored[i] = False
    for i in nodes_explored:
      if not nodes_explored[i]:
        group, nodes_explored = self.bfs_connectivity(i, nodes_explored)
        if group != []:
          groups += [group]
    return groups
  def pathable(self, start_node, end_node):
    self.queue.clear()
    self.queue.enqueue(start_node)
    searched_nodes = {}
    for i in self.graph.unique_nodes:
      searched_nodes[i] = False
    while not self.queue.empty():
      cur_node = self.queue.dequeue()
      searched_nodes[cur_node] = True
      possible = self.connected(cur_node, searched_nodes)
      for B in possible:
        self.queue.enqueue(B)
      if cur_node == end_node:
        return True 
    return False
  def shortest_path(self, start_node, end_node):
    '''
    Returns the path of the shortest path
    '''
    self.queue.clear()
    # Check that this is possible
    assert self.pathable(start_node, end_node), 'This Path is Impossible'
    self.queue.clear()
    searched_node = {}
    for i in self.graph.unique_nodes:
      searched_node[i] = False
    edges = {start_node: None}
    self.queue.enqueue(start_node)
    while not self.queue.empty():
      cur_node = self.queue.dequeue()
      searched_node[cur_node] = True 
      possible = self.connected(cur_node, searched_node)
      for B in possible:
        self.queue.enqueue(B)
        edges[B] = cur_node
        if B == end_node:
          path = [B]
          cur_node = B
          while cur_node != None:
            cur_node = edges[cur_node]
            path += [cur_node]
          # Reverse list
          pathh = []
          for i in range(len(path) -1, -1, -1):
            pathh += [path[i]]
          return pathh[1: ]
      prev_node = cur_node
    raise NotImplementedError
  def loop(self, cycle):
    for i in cycle:
      self.queue.clear()
      self.queue.enqueue(i)
      found = {}
      for j in cycle:
        found[j] = False
      while not self.queue.empty():
        cur_node = self.queue.dequeue()
        if found[cur_node]:
          return True
        found[cur_node] = True
        possible = self.direct_connected(cur_node, found)
        for B in possible:
          self.queue.enqueue(B)
    return False
  def find_single_cycle(self, cycle):
    searched_nodes = {}
    Searched_nodes = {}
    cur_node = None
    for i in cycle:
      cur_node = i
      searched_nodes[i] = False
      Searched_nodes[i] = False
    self.queue.clear()
    self.queue.enqueue(cur_node)
    vals = []
    while not self.queue.empty():
      cur_node = self.queue.dequeue()
      Searched_nodes[cur_node] = True
      possible = self.direct_connected(cur_node, searched_nodes)
      for B in possible:
        vals += [(cur_node, B)]
        if self.loop(vals, (cur_node, B)):
          return True
      possible = self.direct_connected(cur_node, Searched_nodes)
      for B in possible:
        self.queue.enqueue(B)
    return False
  def find_cycle(self):
    '''
    Detects if there is a loop in the graph
    '''
    groups = self.connectivity()
    for group in groups:
      if self.loop(group):
        return True
    return False

bfs = BFS(graph)
print(bfs.find_cycle())