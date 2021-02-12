# Implement an Index Binary Heap, for Eager Dijkstra's with Early Stopping
import math
class BidirectionalHashMap():
  '''
  This class just stores the bidirection dictionaries needed for the index binary heap
  '''
  def __init__(self):
    self.dict = {}
    self.inverse = {}
    self.values = {}
class BinaryHeap():
  '''
  This im
  '''
  def __init__(self, min = True):
    self.nodes = []
    self.min = min # Chooses if the Heap will be min or max
    # Represent the Heap as an array
    self.HashMap = BidirectionalHashMap()
  def __in__(self, key):
    return key in self.HashMap.values
  def get_val(self, key):
    return self.HashMap.values[key]
  def get_true_pos(self, index):
    '''
    Converts the 0 based indices to 1 based, as used in heap formulas
    '''
    return index + 1
  def get_node(self, index):
    return self.nodes[index - 1]
  def get_children(self, parent_idx):
    left_child_idx = 2 * self.get_true_pos(parent_idx)
    right_child_idx = 2 * self.get_true_pos(parent_idx) + 1
    left_child = None
    right_child = None
    if left_child_idx <= len(self.nodes):
      left_child = self.get_node(left_child_idx)
    if right_child_idx <= len(self.nodes):
      right_child = self.get_node(right_child_idx)
    return left_child, right_child, left_child_idx if left_child else None, right_child_idx if right_child else None
  def swap_two_nodes(self, a, b):
    # a and b both in 1 based indexing
    Key_A = self.HashMap.inverse[a]
    Key_B = self.HashMap.inverse[b]

    self.HashMap.dict[Key_A] = b
    self.HashMap.inverse[b] = Key_A
    self.HashMap.dict[Key_B] = a
    self.HashMap.inverse[a] = Key_B


    val_b = self.get_node(b)
    self.nodes[b - 1] = self.get_node(a)
    self.nodes[a - 1] = val_b
  def max_heapify(self, index):
    '''
    Max Heapifies at the current index, given the fact that we know the lower values are fully prepared min/max heaps
    '''
    parent_node = self.get_node(index + 1)
    left_child, right_child, left_child_idx, right_child_idx = self.get_children(index)
    if left_child == None:
        return
    minimum_val = left_child
    if right_child != None:
      if self.min:
        minimum_val = min(left_child, right_child)
      else:
        minimum_val = max(left_child, right_child)
    minimum_index = left_child_idx if minimum_val == left_child else right_child_idx
    if self.min:
      if parent_node > minimum_val:
        self.swap_two_nodes(index + 1, minimum_index)
        self.max_heapify(minimum_index - 1)
    else:
      if parent_node < minimum_val:
        self.swap_two_nodes(index + 1, minimum_index)
        self.max_heapify(minimum_index - 1)
  def Heapify(self, arr):
    '''
    Creates a new heap in O(N) time
    '''
    # Reset the heap to be changed in place
    values = []
    count = 1
    for i in arr:
      for key in i:
        values += [i[key]]
        self.HashMap.dict[key] = count
        self.HashMap.inverse[count] = key
        self.HashMap.values[key] = i[key]
        count += 1
    self.nodes = values
    starting_node = math.floor(len(self.nodes) / 2) - 1 # 0 based coord
    for i in range(starting_node, -1, -1):
      self.max_heapify(i)
  def bubble_up(self, index):
    '''
    Bubbles Up the index(1 Based)
    '''
    parent_idx = math.floor(index / 2)
    if parent_idx <= 0:
        return
    child_node = self.get_node(index)
    parent_node = self.get_node(parent_idx)
    if self.min:
      if child_node < parent_node:
        self.swap_two_nodes(index, parent_idx)
        self.bubble_up(parent_idx)
    else:
      if child_node > parent_node:
        self.swap_two_nodes(index, parent_idx)
        self.bubble_up(parent_idx)
  def insert(self, value):
    # Append it to the end of the nodes
    for key in value:
      value = value[key]
    self.nodes += [value]

    self.HashMap.dict[key] = len(self.nodes)
    self.HashMap.inverse[len(self.nodes)] = key
    self.HashMap.values[key] = value

    # Bubble Up
    index = len(self.nodes) # 1 Based
    self.bubble_up(index)
  def bubble_down(self, index):
    '''
    bubbles the value down
    '''
    left_child_idx = 2 * index
    right_child_idx = 2 * index + 1

    left_child = None
    right_child = None
    
    if not left_child_idx > len(self.nodes):
      left_child = self.get_node(left_child_idx)
    if not right_child_idx > len(self.nodes):
      right_child = self.get_node(right_child_idx)
    if left_child == None:
      return
    minimum_val = left_child
    if right_child != None:
      if self.min:
        minimum_val = min(left_child, right_child)
      else:
        minimum_val = max(left_child, right_child)
    minimum_index = left_child_idx if minimum_val == left_child else right_child_idx
    parent_node = self.get_node(index)

    if self.min:
      if parent_node > minimum_val:
        self.swap_two_nodes(index, minimum_index)
        self.bubble_down(minimum_index)
    else:
      if parent_node < minimum_val:
        self.swap_two_nodes(index, minimum_index)
        self.bubble_down(minimum_index)
  def extract_min(self, get_node = False):
    '''
    This will extract the minimum or maximum value and completely remove it from the heap, returning this value
    '''
    minimum_val = self.get_node(1) # This is the min/max value, by nature of the heap, now to remove the value
    node = self.HashMap.inverse[1]
    
    self.swap_two_nodes(1, len(self.nodes))

    key = self.HashMap.inverse[len(self.nodes)]
    del self.HashMap.inverse[len(self.nodes)]
    del self.HashMap.dict[key]
    del self.HashMap.values[key]
    self.nodes = self.nodes[0: -1] # the node is removed, fix the ordering to make it a heap again

    self.bubble_down(1)
    if get_node:
      return node
    return minimum_val
  def update(self, key, value):
    '''
    This method will update the value of the key and fix the structure of the heap
    '''
    # First, update the value in the heap
    assert key in self.HashMap.dict 
    index = self.HashMap.dict[key]
    self.HashMap.values[key] = value
    self.nodes[index - 1] = value
    # Decide between Bubbling Up or Down
    left_child, left_child_idx, right_child, right_child_idx = self.get_children(index - 1)

    minimum_val = left_child
    if right_child != None:
      if self.min:
        minimum_val = min(left_child, right_child)
      else:
        minimum_val = max(left_child, right_child)
    if minimum_val != None:
      minimum_index = left_child_idx if minimum_val == left_child else right_child_idx
      if self.min:
        if value > minimum_val:
          self.swap_two_nodes(index, minimum_index)
          self.bubble_down(minimum_index)
          return
      else:
        if value < minimum_val:
          self.swap_two_nodes(index, minimum_index)
          self.bubble_down(minimum_index)
          return # If it bubbles down, there is no need to bubble up
    parent_node_idx = math.floor(index / 2)
    if parent_node_idx <= 0:
      return
    parent_node = self.get_node(parent_node_idx)
    if self.min:
      if parent_node > value:
        self.bubble_up(index)
    else:
      if parent_node < value:
        self.bubble_up(index)
  def delete(self, key):
    '''
    Deletes a Key completely from the heap
    '''
    index = self.HashMap.dict[key]
    self.swap_two_nodes(index, len(self.nodes)) # Swaps this index with the last value
    # Delete this from the heap
    del self.HashMap.dict[key]
    del self.HashMap.values[key]
    del self.HashMap.inverse[len(self.nodes)]
    self.nodes = self.nodes[:-1]
    # now, fix the original node
    left_child, left_child_idx, right_child, right_child_idx = self.get_children(index - 1)
    minimum_val = left_child
    if right_child != None:
      if self.min:
        minimum_val = min(left_child, right_child)
      else:
        minimum_val = max(left_child, right_child)
    parent_node = self.get_node(index)
    if minimum_val != None:
      minimum_index = left_child_idx if minimum_val == left_child else right_child_idx
      if self.min:
        if parent_node > minimum_val:
          self.swap_two_nodes(index, minimum_index)
          self.bubble_down(minimum_index)
          return
      else:
        if parent_node < minimum_val:
          self.swap_two_nodes(index, minimum_index)
          self.bubble_down(minimum_index)
          return
    Parent_idx = math.floor(index / 2)
    if Parent_idx <= 0:
      return
    Parent_node = self.get_node(parent_idx)
    if self.min:
      if Parent_node > parent_node:
        self.swap_two_nodes(Parent_idx, index)
        self.bubble_up(Parent_idx)
    else:
      if Parent_node < parent_node:
        self.swap_two_nodes(Parent_idx, index)
        self.bubble_up(Parent_idx)
  def empty(self):
    return len(self.nodes) == 0  
class HeapSort():
  def __init__(self):
    pass
  def sort(self, arr):
    count = 1
    values = []
    for i in arr:
      values += [{count: i}]
      count += 1
    heap = BinaryHeap()
    heap.Heapify(values)
    sorted_arr = []
    while not heap.empty():
      sorted_arr += [heap.extract_min()]
    return sorted_arr
# Eager Dijkstra's with Early Stopping
# First, Construct the Graph
class WeightedGraph():
  def __init__(self):
    self.edges = {}
    self.unique_nodes =[]
  def add_edge(self, a, b, weight):
    assert weight >= 0
    assert (a, b) not in self.edges # Unique Assignment
    self.edges[(a, b)] = weight
    self.unique_nodes += [a]
    self.unique_nodes += [b]
    self.unique_nodes = list(set(self.unique_nodes))
  def update_graph(self, a, b, weight):
    assert weight >=0
    assert (a, b) in self.edges
    self.edges[a, b] = weight
  def connected(self, source):
    found = []
    for A, B in self.edges:
      if A == source:
        found += [B]
    return found
# Sample Graph 
graph = WeightedGraph()
# Path One
graph.add_edge('s', 'a', 2)
graph.add_edge('a', 'd', 6)
graph.add_edge('d', 'g', 4)
graph.add_edge('g', 't', 4)
# Path Two(GT!)
graph.add_edge('s', 'b', 2)
graph.add_edge('b', 'e', 3)
graph.add_edge('e', 'd', 2)
# Path Three
graph.add_edge('s', 'c', 7)
graph.add_edge('c', 'f', 8)
graph.add_edge('f', 't', 5)
class Dijkstra():
  def __init__(self, graph):
    self.graph = graph
    self.heap = BinaryHeap()
  def shortest_path(self, source, sink):
    '''
    Solves for the Shortest Path, using Early Stopping, Assuming a Complete path from source to sink
    '''
    found = [source]
    path = {source: {'length': 0, 'path': []}}
    cur_node = source
    path_to_node = {}
    prev_path_length = 0
    while len(found) != len(self.graph.unique_nodes):
      possible = self.graph.connected(cur_node)
      for node in possible:
        weight = self.graph.edges[(cur_node, node)] + prev_path_length
        if self.heap.__in__(node):
          value = self.heap.get_val(node)
          if weight < value:
            path_to_node[node] = (cur_node, node)
          self.heap.update(node, weight)
        else:
          self.heap.insert({node: weight})
          path_to_node[node] = (cur_node, node)
      # Extract Minimum Value of Dijkstra Greedy Score
      min_node = self.heap.extract_min(get_node = True)
      A, B = path_to_node[min_node]
      tmp = path[A]
      tmp_value = tmp['length']
      tmp_path = tmp['path']
      weight = self.graph.edges[(A, B)] + tmp_value
      path_min = tmp_path + [(A, B)]
      path[B] = {'length': weight, 'path': path_min}
      prev_path_length = weight
      cur_node = B
      found += [B]
      found = list(set(found))
      if B == sink:
        return path[B]
    return path
Solution = Dijkstra(graph)
print(Solution.shortest_path('s', 't'))