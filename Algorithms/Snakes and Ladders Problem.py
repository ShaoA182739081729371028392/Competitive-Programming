'''
Uses Breadth First Search to Solve the Snakes and Ladders Problem
'''
class Graph():
  def __init__(self):
    self.directed_nodes = {}
    self.unique_nodes = []
  def add_connection(self, a, b):
    self.directed_nodes[(a, b)] = True
    self.unique_nodes += [a]
    self.unique_nodes += [b]
    self.unique_nodes = list(set(self.unique_nodes))
  
  def generate_grid(self, length):
    for i in range(1, length):
      self.add_connection(i, i + 1) 
class Queue():
  def __init__(self):
    self.queue = []
  def enqueue(self, val):
    self.queue = [val] + self.queue
  def dequeue(self):
    val = self.queue[0]
    self.queue = self.queue[1: ]
    return val
  def empty(self):
    return len(self.queue) == 0
class Solution():
  def __init__(self, graph):
    self.graph = graph
  def connected(self, start_node):
    '''
    Searches all of the nodes connected to this node
    '''
    vals = []
    for A, B in self.graph.directed_nodes:
      if A == start_node:
        vals += [B]
    return vals
  def shortest_path(self, end_node):
    '''
    Solves the Shortest Path in the snakes algorithm
    '''
    values = {1: None}
    queue = Queue()
    queue.enqueue(1)
    path = []
    while not queue.empty():
      cur_node = queue.dequeue()
      possible = self.connected(cur_node)
      for node in possible:
        if node not in values:
          values[node] = cur_node
          queue.enqueue(node)
        if node == end_node:
          cur_node = end_node
          while cur_node != None:
            path += [(cur_node, values[cur_node])]
            cur_node = values[cur_node]
          path.reverse()
          return path
    raise Exception("Node is not in the graph")
# Create a Grid
graph = Graph()
graph.generate_grid(36)
# Add Snakes and Ladders
graph.add_connection(20, 29)
graph.add_connection(27, 1)
graph.add_connection(21, 9)
graph.add_connection(19, 7)
graph.add_connection(17, 4)
graph.add_connection(11, 26)
graph.add_connection(5, 8)
graph.add_connection(3, 22)

solution = Solution(graph)
print(solution.shortest_path(30))