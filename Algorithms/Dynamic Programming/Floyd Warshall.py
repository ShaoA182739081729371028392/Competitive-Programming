class WeightedGraph:
  def __init__(self, unique_nodes):
    self.unique_nodes = sorted(list(set(unique_nodes)))
    self.edges = {}
    self.initialize_all_edges()
  def initialize_all_edges(self):
    '''
    Initializes each edge.
    '''
    for i in self.unique_nodes:
      for j in self.unique_nodes:
        if i == j:
          self.edges[i, j] = 0
        else:
          self.edges[i, j] = float('inf')
          self.edges[j, i] = float('inf')
  def find_outgoing_edges(self, node1):
    '''
    Finds Outgoing edges from node1
    '''
    edges = []
    for node2 in self.unique_nodes:
      if (node1, node2) in self.edges:
        edges += [node2]
    return edges
  def add_node(self, node1, node2, edge_weight):
    assert node1 in self.unique_nodes and node2 in self.unique_nodes
    self.edges[(node1, node2)] = edge_weight

  def finish(self):
    '''
    Sorts the nodes for consistency
    '''
    return sorted(list(set(self.unique_nodes))) # O(NlogN)

class NaiveDP():
  '''
  Naive Dynamic Recursive Program.
  '''
  def __init__(self, graph):
    self.graph = graph
    self.memoized = {} # 3 Stage Table(i, j, k)
    self.parent_pointers = {} # Parent pointers, how to get from A -> B
    self.initialize_path_weights()
  def initialize_path_weights(self):
    '''
    Initializes paths to themselves
    '''
    for node in self.graph.unique_nodes:
      for k in range(len(self.graph.unique_nodes)):
        self.memoized[(node, node, k)] = 0
        self.parent_pointers[(node, node, k)] = []
  def reset(self):
    self.memoized = {}
    self.initialize_path_weights()
  def dp(self, i, j, k):
    '''
    Naive Dynamic Program. O(n^4), since O(n^3) subproblems and O(n) per subproblem.
    '''
    if (i, j, k) in self.memoized:
      return self.memoized[i, j, k]
    else:
      if k == 0:
        result = self.graph.edges[(i, j)]
        path = [(i, j)]
      else:
        # Iterate over all k outgoing edges.
        outgoing_edges = self.graph.find_outgoing_edges(i)
        results = {} # Technically not needed, but makes more sense to read.
        min_weight = float('inf')
        best_node = None
        for outgoing in outgoing_edges:
          results[outgoing] = self.dp(outgoing, j, k - 1) + self.graph.edges[(i, outgoing)]
          if best_node == None:
            best_node = outgoing
            min_weight = float('inf')
          if results[outgoing] < min_weight:
            min_weight = results[outgoing]
            best_node = outgoing
        result = min_weight
        if i != best_node:
          path = [(i, best_node)] + [self.parent_pointers[(best_node, j, k - 1)]]
        else:
          path = []
      # Memoize
      self.memoized[(i, j, k)] = result
      self.parent_pointers[(i, j, k)] = path

      return result

  def solve(self):
    '''
    Uses DP to Solve ASPS
    '''
    paths = {}
    shortest_dist = {}
    for i in self.graph.unique_nodes:
      for j in self.graph.unique_nodes:
        best_path = []
        best_dist = float('inf')
        for k in range(len(self.graph.unique_nodes)):
          result = self.dp(i, j, k)
          path = self.parent_pointers[(i, j, k)]
          if result < best_dist:
            best_dist = result
            best_path = path
        paths[(i, j)] = (best_path)
        shortest_dist[(i, j)] = best_dist
    return paths, shortest_dist
class Optimized:
  '''
  O(N^3LogN) algorithm, Since Memoized State is O(N^2LogN) and each node needs O(N)
  '''
  def __init__(self, graph):
    self.graph = graph
    self.smallestM = 0
    self.smallestLogM = 0
    for i in range(len(self.graph.unique_nodes)):
      if 2**i > len(self.graph.unique_nodes) - 1:
        self.smallestM = 2 ** i
        self.smallestLogM = i
        break
    self.memoized = {}
    self.parent_pointers = {}
  def initialize_memoize(self):
    self.memoized = {}
    self.parent_pointers = {}
    for node in self.graph.unique_nodes:
      for i in range(self.smallestLogM):
        self.memoized[(node, node, 2 ** i)] = 0
  def dp(self, i, j, m):
    if (i, j, m) in self.memoized:
      return self.memoized[i, j, m]
    else:
      if i == j:
        result = self.graph.edges[i, j]
        path = []
      elif m == 1:
        result = self.graph.edges[i, j]
        path = [(i, j)]
      else:
        # Iterate over all k
        best_result = float('inf')
        best_path = None
        for k in self.graph.unique_nodes:
          result  = self.dp(i, k, m // 2) + self.dp(k, j, m // 2)
          path = self.parent_pointers[i, k, m // 2] + self.parent_pointers[k, j, m // 2]
          if best_path == None:
            best_path = path
            best_result = result
          if result < best_result:
            best_path = path
            best_result = result
        result = best_result
        path = best_path
    self.memoized[(i, j, m)] = result
    self.parent_pointers[(i, j, m)] = path
    return result
  def solve(self):
    for i in self.graph.unique_nodes:
      for j in self.graph.unique_nodes:
        self.dp(i, j, self.smallestM)
    # Loop Again to Find Fastest One(O(N^2LogN), so no contrib to asymptotic running time)
    best_distances ={}
    best_paths = {}
    for i in self.graph.unique_nodes:
      for j in self.graph.unique_nodes:
        best_path = None
        best_distance = float('inf')
        for k in range(self.smallestLogM):
          if best_path == None:
            best_path = self.parent_pointers[(i, j, 2 ** k)]
            best_distance = self.memoized[(i, j, 2 ** k)]
          if self.memoized[(i, j, 2 ** k)] < best_distance:
            best_distance = self.memoized[(i, j, 2 ** k)]
            best_path = self.parent_pointers[i, j, 2 ** k]
        best_distances[i, j] = best_distance
        best_paths[i, j] = best_path
    return best_distances, best_paths



class FloydWarshall:
  '''
  Optimized DP algorithm: O(N^3) instead of O(N^4) or O(N^3LogN)
  '''
  def __init__(self, graph):
    self.graph = graph
    self.node2idx = {}
    self.setupNodes()
    self.memoized = {}
    self.parent_pointers = {}
  def setupNodes(self):
    for node_idx in range(len(self.graph.unique_nodes)):
      self.node2idx[self.graph.unique_nodes[node_idx]] = node_idx
  def reset(self):
    self.memoized = {}
    self.parent_pointers = {}
  def initialize_path_weights(self):
    '''
    Initializes path weights(Nodes to themselves = 0)
    '''
    self.reset()
    for i in self.graph.unique_nodes:
      for k in range(len(self.graph.unique_nodes)):
        self.memoized[i, i, k] = 0
  def dp(self, i, j, k):
    if (i, j, k) in self.memoized:
      return self.memoized[i, j, k]
    else:
      # at this point, i cannot be j, since it is already memoized.
      if k == 0:
        result = self.graph.edges[i, j]
        path = [(i, j)]
      else:
        # O(1) time.
        short_result = self.dp(i, j, k - 1)
        short_path = self.parent_pointers[i, j, k - 1]
        inter_result = self.dp(i, self.graph.unique_nodes[k], k - 1) + self.dp(self.graph.unique_nodes[k], j, k -1)
        inter_path = self.parent_pointers[i, self.graph.unique_nodes[k], k - 1] + self.parent_pointers[self.graph.unique_nodes[k], j, k - 1]

        if short_result < inter_result:
          result = short_result
          path = short_path
        else:
          result = inter_result
          path = inter_path
      self.memoized[i, j, k] = result
      self.parent_pointers[i, j, k] = path
      return result
  def solve(self):
    best_paths = {}
    best_results = {}
    for i in self.graph.unique_nodes:
      for j in self.graph.unique_nodes:
        best_result = float('inf')
        best_path = None
        for k in range(len(self.graph.unique_nodes)):
          result = self.dp(i, j, k)
          if best_path == None:
            best_path = self.parent_pointers[i, j, k]
            best_result = result
          if result < best_result:
            best_result = result
            best_path = self.parent_pointers[i, j, k]
        best_paths[i, j] = best_path
        best_results[i, j] = best_result
    return best_results, best_paths
def sample_graph():
  graph = WeightedGraph(['A', 'B', 'C', 'D', 'E', 'F'])
  graph.add_node('A', 'B', 11)
  graph.add_node('B', 'F', 2)
  graph.add_node('A', 'D', 4)
  graph.add_node('A', 'C', 1)
  graph.add_node('C', 'D', 2)
  graph.add_node('C', 'E', 7)
  graph.add_node('E', 'D', 6)
  graph.add_node('D', 'F', 6)
  graph.add_node('E', 'F', 8)
  return graph
def main():
  graph = sample_graph()
  dp = FloydWarshall(graph)
  best_distances, best_paths = dp.solve()
  print(best_distances)
  print(best_paths)
if __name__ == '__main__':
  main()