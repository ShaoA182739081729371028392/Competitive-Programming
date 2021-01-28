# This is a set of Binary Tree Operations
# Helper Classes for construction of BST
import pudb
class Node():
  def __init__(self):
    self.value = None
    self.left = None
    self.right = None
    self.parent = None
    self.keys_below = None # Augmented Data
    self.y = None # Augmented Data, needed for visualization of the binary Tree
    self.x = None # Same as X
class Queue():
  def __init__(self):
    self.queue = []
  def enqueue(self, value):
    self.queue = self.queue + [value]
  def dequeue(self):
    value = self.queue[0]
    self.queue = self.queue[1:]
    return value
  def empty(self):
    return len(self.queue) == 0
class Stack():
  def __init__(self):
    self.stack = []
  def enstack(self, val):
    self.stack.append(val)
  def unstack(self):
    val = self.stack[-1]
    self.stack = self.stack[:-1]
    return val
  def empty(self):
    return len(self.stack) == 0

# Main BST Module, Aug stands for Augmented as there is augmented data in each node
class AugBST():
  def __init__(self):
    self.root = None
  def __str__(self):
    '''
    Prints a representation of the binary search tree, using the x and y values
    '''
    y_values = {} # Maps the heights to their respective nodes
    y_to_max = {} # Maps the y values to the maximum x_value of the nodes, to pad the string when it comes to printing
    max_y_val = 0
    queue = Queue()
    if not self.root:
      return "Binary Tree is Empty"
    queue.enqueue(self.root)
    while not queue.empty():
      cur_node = queue.dequeue()
      cur_node_y = cur_node.y
      max_y_val = max(max_y_val, cur_node_y)
      if cur_node_y not in y_values:
        y_values[cur_node_y] = [cur_node]
        y_to_max[cur_node_y] = cur_node.x
      else:
        y_values[cur_node_y] += [cur_node]
        y_to_max[cur_node_y] = max(y_to_max[cur_node_y], cur_node.x)
      if cur_node.left:
        queue.enqueue(cur_node.left)
      if cur_node.right:
        queue.enqueue(cur_node.right)
    # Should have collected all nodes by now, so now simply print out the tree as needed
    for y in range(max_y_val + 1):
      # Create Padded String
      print_row = " " * y_to_max[y]
      for node in y_values[y]:
        print_row = print_row[:node.x] + str(node.value) + print_row[node.x + 1:]
      print(print_row) 
    return f"Binary Tree Printed, Height: {max_y_val}"

  def insert(self, value):
    '''
    Inserts into the tree and updates the keys_below, asserts that the Tree only has unique values
    '''
    # Create New Node to be inserted into the BST
    new_node = Node()
    new_node.value = value
    new_node.keys_below = 1 # Just itself, since it will be added as a leaf
    new_node.y = 0
    new_node.x = 0
    if self.root == None:
      self.root = new_node
      return
    # Now that we know that the tree isn't empty, we search to ensure that this value isn't already in the tree first
    assert not self.search(value), "Node already Exists, we assume that the BST has only unique values"
    cur_node = self.root
    while cur_node.left or cur_node.right:
      cur_node.keys_below += 1
      new_node.y += 1
      if value <= cur_node.value: # There should be no ties
        if cur_node.left:
          cur_node = cur_node.left
        else:
          cur_node.left = new_node
          new_node.parent = cur_node
          self.__update_x_values(new_node, self.root)
          return
      else:
        new_node.x = cur_node.x + 1
        if cur_node.right:
          cur_node = cur_node.right
        else:
          cur_node.right = new_node
          new_node.parent = cur_node
          self.__update_x_values(new_node, self.root)
          return
    cur_node.keys_below += 1
    new_node.y += 1
    if value <= cur_node.value:
      cur_node.left = new_node
      new_node.parent = cur_node
    else:
      new_node.x += 1
      cur_node.right = new_node
      new_node.parent = cur_node
    self.__update_x_values(new_node, self.root)
  def __update_x_values(self, node, root_node):
    '''
    Given Some inserted node, this method updates all x_values of all nodes to the right of it.
    '''
    # Performs traversal of all nodes recursively
    if not root_node.left and not root_node.right:
      return
    else:
      if root_node.left:
        self.__update_x_values(node, root_node.left)
      if root_node.right:
        self.__update_x_values(node, root_node.right)
      # update the x value if is the same or greater(means this node is to the left)
      if root_node.x >= node.x and node != root_node:
        root_node.x += 1
  def __deletion_no_sub(self, node):
    '''
    Performs deletion in the tree when there is no children
    '''
    assert not node.left and not node.right # Leaf or only one node
    if not node.parent:
      self.root = None # Tree is empty now
      return 
    else:
      value = node.value
      # Move to the parent and cut off connection
      parent = node.parent
      if parent.left:
        if parent.left.value == value:
          parent.left = None
      elif parent.right:
        if parent.right.value == value:
          parent.right = None
      # Node is now deleted
  def __delete_node_one_subtree(self, node):
    '''
    Performs short circuit deletion if there is only one node underneath the selected node 
    '''
    assert (node.left or node.right) and not (node.left and node.right) # Asserts that there is at least one subtree and that there is only one subtree
    # Search for child node
    child_node = None
    if node.left:
      child_node = node.left
    else:
      child_node = node.right # We know there exists at least one tree
    if not node.parent:
      self.root = child_node
      return
    else:
      value = node.value
      parent_node = node.parent
      if parent_node.left.value == value:
        parent_node.left = child_node
      else:
        parent_node.right = child_node
  def __delete_node_both_subtrees(self, node):
    '''
    Deletes the node if both subtrees exist
    '''
    assert node.left and node.right
    # Locate the Predecessor Node
    predecessor = self.__find_predecessor(node)
    # Copy Value over the predecessor into the main Node
    node.value = predecessor.value
    # Try to delete the predecesssor
    self.__delete_node(predecessor)
  def __delete_node(self, node):
    '''
    Runs the conditions to figure out while deletion is needed for this node
    '''
    # Easiest Case, no children
    if not node.left and not node.right:
      self.__deletion_no_sub(node)
    elif (node.left or node.right) and not (node.left and node.right):
      # One subtree
      self.__delete_node_one_subtree(node)
    else:
      # Two Subtrees
      self.__delete_node_both_subtrees(node)

  def delete(self, value):
    '''
    Deletes a Certain value(We assume unique values) and updates keys_below
    '''
    # Locate the Node
    node = self.search_node(value)
    self.__delete_node(node)
  def __find_maximum_node(self, node):
    '''
    Given some node, this locates the maximum valued node
    Helper method to self.__find_predecessor
    '''
    # Simply move to the right as much as possible
    while node.right:
      node = node.right
    return node
  def __find_predecessor(self, node):
    '''
    Locates a Predecessor Node to the node given, helper method to self.__delete_node_both_subtrees
    Return: Node
    '''
    # Check for easy Case, when the node has a left tree
    if node.left:
      return self.__find_maximum_node(node.left)
    else:
      cur_node = node
      value = node.value
      while cur_node.parent:
        if cur_node.value < value:
          return cur_node
        cur_node = cur_node.parent
      raise Exception("There is no Predecessor")

  def maximum(self, root):
    '''
    Returns the maximum value in the tree from some root, this may be useful to pick out the maximum in a subroot
    Performs this recursively, to keep the code clean
    '''
    assert root, "This Root Doesnt Exist"
    if not root.right:
      return root.value
    else:
      return self.maximum(root.right)
  def minimum(self, root):
    '''
    Returns the minimum value in the tree
    '''
    assert root, "This Root Doesnt Exist"
    if not root.left:
      return root.value
    else:
      return self.minimum(root.left)
  def search(self, value):
    '''
    Returns if a certain value exists in the tree
    '''
    assert self.root, "Please Construct a Tree before searching it"
    cur_node = self.root
    while cur_node.left or cur_node.right:
      if value == cur_node.value:
        return True
      if value < cur_node.value:
        if not cur_node.left:
          return False
        else:
          cur_node = cur_node.left
      else:
        if not cur_node.right:
          return False
        else:
          cur_node = cur_node.right
    if cur_node.value == value:
      return True
    return False
  def locate_node_value(self, value):
    '''
    Returns the node location of the given value, assumes that the BST has only unique values and that this node actually exists 
    '''
    assert self.search(value), "Node doesnt exist in the tree"
    cur_node = self.root
    while cur_node.left or cur_node.right:
      if cur_node.value == value:
        return cur_node
      elif value < cur_node.value:
        cur_node = cur_node.left # No need to check as the search already determines that the node is present in the tree
      else:
        cur_node = cur_node.right
    if cur_node.value == value:
      return cur_node

  def predecessor(self, value):
    '''
    First asserts the value exists in the tree and then computes the predecessor node
    '''
    assert self.search(value), "Node doesn't exist in tree"
    node_located = self.locate_node_value(value)

    # Case 1: The Node has a left tree
    if node_located.left:
      return self.maximum(node_located.left)
    else:
      # Case 2: No Left Tree, follow parent nodes
      cur_node = node_located
      while cur_node.parent:
        if value > cur_node.value:
          return cur_node.value
        cur_node = cur_node.parent
      if cur_node.value < value:
        return cur_node.value
      else:
        raise Exception("No predecessor")
  def successor(self, value):
    '''
    Opposite of self.predecessor
    '''
    assert self.search(value), "Node doesn't exist"
    node_located = self.locate_node_value(value)
    # case 1, right tree exists
    if node_located.right:
      return self.minimum(node_located.right)
    else:
      # Follow parents upward
      cur_node = node_located
      while cur_node.parent:
        if cur_node.value > value:
          return cur_node.value
        else:
          cur_node = cur_node.parent
      if cur_node.value > value:
        return cur_node.value
      else:
        raise Exception("No Successor")
  def rank(self, value):
    '''
    returns the rank of a key(AKA how many nodes this one is higher than)
    '''
    # Locate Node in the tree
    located_node =  self.search_node(value)
    if not located_node.left:
      return 0
    else:
      return located_node.left.keys_below
  def __search_node_private(self, head_node, value):
    '''
    Recursively Locates the node
    '''
    if head_node.value == value:
      return head_node
    elif head_node.value < value:
      if not head_node.left:
        raise Exception("Node doesnt exist in tree")
      return self.__search_node_private(self, head_node.left, value)
    else:
      if not head_node.right:
        raise Exception("Node Doesnt exist in tree")
      return self.__search_node_private(self, head_node.right, value)
  def search_node(self, value):
    '''
    Locates a Node in the graph and returns the node, useful for self.rank
    
    Assumes the Tree is unique
    '''
    assert self.root
    cur_node = self.root
    return self.__search_node_private(cur_node, value)
    
  def select(self, i):
    '''
    Recursively determines the ith highest value.
    i represents the ith highest value
    Returns the value
    '''
    assert self.root, "Root Doesn't Exist"
    cur_node = self.root
    ith = i
    while True:
      # Collect Left Tree value
      left_tree_val = 0 # Non-existant left nodes are denoted as 0
      if cur_node.left:
        left_tree_val = cur_node.left.keys_below
      if ith == left_tree_val:
        return cur_node.value
      elif ith < left_tree_val:
        if not cur_node.left:
          raise Exception("This selection doesnt exist")
        cur_node = cur_node.left
      else:
        if not cur_node.right:
          raise Exception("This Selection doesnt exist")
        cur_node = cur_node.right
        ith-= (left_tree_val + 1)
     

  def list_insert(self, values):
    '''
    Quality of Life Method, inserts nodes in order of the array
    '''
    for i in values:
      self.insert(i)
  def store_inOrderTraversal(self):
    '''
    Uses a stack to traverse down the BST In order
    '''
    assert self.root, "There is no tree to traverse"
    stack = Stack()
    cur_node = self.root
    stack.enstack(cur_node)
    ordered = []
    while not stack.empty() or cur_node:
      if cur_node:
        if cur_node.left:
          cur_node = cur_node.left
          stack.enstack(cur_node)
          continue
      if stack.empty():
        break
      cur_node = stack.unstack()
      ordered += [cur_node.value]
      cur_node = cur_node.right
      if cur_node:
        stack.enstack(cur_node)
    return ordered
# BST Sort: outside of BST class
def BST_sort(arr):
  '''
  Generates a New BST and performs BST sort on it
  O(nLogN)
  '''
  new_BST = AugBST()
  new_BST.list_insert(arr)
  return new_BST.store_inOrderTraversal()
