class WeightedGraph():
  def __init__(self):
    self.nodes = []
    self.weights = {}
    self.unique_nodes = []
    self.source = None
    self.sink = None
  def add_node(self, node1, node2, weight, isSource = False, isSink = False):
    # Check that No Nodes heading towards Source, and no nodes heading out of sink(Proper WeightedGraph)
    if self.source:
      assert node2 != self.source, "No Nodes can head into the source"
    if self.sink:
      assert node1 != self.sink, "No Nodes can leave the sink"
    if node1 not in self.unique_nodes:
      self.unique_nodes += [node1]
    if node2 not in self.unique_nodes:
      self.unique_nodes += [node2]
    if isSink:
      self.sink = node2
    if isSource:
      self.source = node1
    self.nodes += [(node1, node2)]
    self.weights[(node1, node2)] = weight
    # (node1, node2) represents node1 -> node 2
class BellmanFord():
  def __init__(self, graph):
    self.graph = graph
    self.shortest_path = {} # Nodes are stored in the format: {"Node Name": {"Shortest Path": [Path], "Shortest Dist": int}}
    # Not Reachable Nodes will have an Empty Path and inf as the shortest dist 
    for node in self.graph.unique_nodes:
      self.shortest_path[node] = {"Shortest Path": [], "Shortest Dist": float('inf')}
    assert self.graph.source, "No Source in Graph"
    assert self.graph.sink, "No Sink in Graph"
    # Initialize Source
    self.shortest_path[self.graph.source]['Shortest Dist'] = 0
  def relax_edge(self, node1, node2):
    '''
    Relaxes an Edge if the node1.weight + W(node1, node2) < node2.weight

    Updates Shortest Path As needed
    '''
    node1_weight= self.shortest_path[node1]['Shortest Dist']
    node2_weight = self.shortest_path[node2]['Shortest Dist']
    node1_node2 = self.graph.weights[(node1, node2)]
    if node1_weight + node1_node2 < node2_weight:
      self.shortest_path[node2]['Shortest Path'] = self.shortest_path[node1]['Shortest Path'] + [(node1, node2)] 
      self.shortest_path[node2]['Shortest Dist'] = self.shortest_path[node1]['Shortest Dist'] + node1_node2
  def bellmanFord(self):
    '''
    Runs Bellman-Ford on the graph, raises Exception if no path from source to sink.

    Also raises Exception if negative cycle exists.
    '''
    num_iter = len(self.graph.unique_nodes) - 1
    for i in range(num_iter):
      '''
      Relax Every Edge that Exists.
      '''
      for node1, node2 in self.graph.weights:
        self.relax_edge(node1, node2)
    # Check if Sink has been reached
    source, sink = (self.graph.source, self.graph.sink)
    assert self.shortest_path[sink]['Shortest Dist'] != float('inf'), "Sink is Unreachable"
    # Check all nodes for negative cycles
    for node1, node2 in self.graph.weights:
      node2_dist = self.shortest_path[node2]['Shortest Dist']
      node1_dist = self.shortest_path[node1]['Shortest Dist']
      node1_node2 = self.graph.weights[(node1, node2)]
      assert node1_dist + node1_node2 >= node2_dist, "Negative Cycle Detected."
    print("Bellman Ford Completed.") 
def main():
  '''
  Tests BellMan-Ford Algo.
  '''
  # Create Sample Graph
  graph = WeightedGraph()
  graph.add_node('s', 'a', 1, isSource = True)
  graph.add_node('s', 'd', 5, isSource = True)
  graph.add_node('a', 'b', 2)
  graph.add_node('b', 'c', 3)
  graph.add_node('c', 'b', -5) # Negative Cycle
  graph.add_node('c', 't', 4, isSink = True)
  graph.add_node('d', 'e', 1)
  graph.add_node('e', 't', 1, isSink = True)
  # Create BellMan Ford Object
  bellmanFord = BellmanFord(graph)
  bellmanFord.bellmanFord()
  print(bellmanFord.shortest_path)
  
if __name__ == '__main__':
  main()