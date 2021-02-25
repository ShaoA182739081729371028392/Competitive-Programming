# Balanced Binary Search Tree Types
# Create Helper Classes: Stack and Queues
class Stack():
  def __init__(self):
    self.stack = []
  def enstack(self, value):
    self.stack += [value]
  def destack(self):
    value = self.stack[-1]
    self.stack = self.stack[:-1]
    return value
# Queue:
class Queue():
  def __init__(self):
    self.queue = []
  def enqueue(self, value):
    self.queue += [value]
  def dequeue(self):
    val = self.queue[0]
    self.queue = self.queue[1:]
    return val 
  def empty(self):
    '''
    Checks if the Queue is empty or not
    '''
    return len(self.queue) == 0
class AVLNode():
  '''
  Node for the AVL Tree,
  Augmented DS with Height
  '''
  def __init__(self, value):
    self.value = value
    self.height = 0
    self.left = None
    self.right = None
    self.parent = None
class AVLTree():
  def __init__(self):
    '''
    Creates an AVL Tree
    '''
    self.root = None
  def _compute_height(self, node):
    '''
    Computes the height of a given node.
    Formula is max(node.left.height, node.right.height) + 1
    '''
    left_node_height = -1
    if node.left:
      left_node_height = node.left.height
    right_node_height = -1
    if node.right:
      right_node_height = node.right.height
    return max(right_node_height, left_node_height) + 1
  def search(self, value):
    '''
    Searches if the node exists in the tree
    '''
    if not self.root:
      return False
    cur_node = self.root
    while cur_node.left or cur_node.right:
      if cur_node.value == value:
        return True
      elif value < cur_node.value:
        if not cur_node.left:
          return False
        cur_node = cur_node.left
      else:
        if not cur_node.right:
          return False
        cur_node = cur_node.right
    if cur_node.value == value:
      return True
    return False
  def _rotate_right(self, cur_node):
    '''
    Performs a Right Rotation on the current_node

    Operations(Constant):
    - Same as self._rotate_left but backwards
    '''
    assert cur_node.left, "Left Node must exist"
    parent = cur_node.parent
    left_node = cur_node.left
    if parent:
      if parent.left == cur_node:
        parent.left = left_node
      else:
        parent.right = left_node
    else:
      self.root = left_node
    left_node.parent = parent
    # Route Left's Right node to the cur_node's left node
    tmp = left_node.right
    if tmp:
      tmp.parent = cur_node
    cur_node.left = tmp

    cur_node.parent = left_node
    left_node.right = cur_node

    cur_node.height = self._compute_height(cur_node)
    left_node.height = self._compute_height(left_node)
    # Update Heights for cur_node and left_node
    return # Right Rotation Completed. 
  def _rotate_left(self, cur_node):
    '''
    Performs a Left Rotation on the current_node

    Operations(Constant):
    - Set right_nodes left node(if exists) to cur_nodes right node
    - Set Right_nodes left_node to cur_node(adjust parent accordingly)
    - Set Right Nodes parent to cur_nodes parent
    - Set Cur_nodes parents right to cur_nodes right node
    '''
    assert cur_node.right, "Right node has to exist for a left rotation"
    parent = cur_node.parent # This can be None, in which the rotation still works
    right_node = cur_node.right
    if parent:
      if parent.right == cur_node:
        parent.right = right_node
      else:
        parent.left = right_node
    else:
      self.root = right_node
    right_node.parent = parent
    # Tmp Store right_nodes left node
    tmp = right_node.left # Can be None
    if tmp:
      tmp.parent = cur_node
    cur_node.right = tmp

    cur_node.parent = right_node
    right_node.left = cur_node

    # Update Height in cur-node and right_node, further discrepencies can only exist further up the TabError
    cur_node.height = self._compute_height(cur_node)
    right_node.height = self._compute_height(right_node)
    return # Left Rotation Complete.
    
  def _is_left_heavy(self, node):
    '''
    Given a discrepency, this method checks if the node is left heavy(True) or right_heavy(False)
    '''
    left_node_height = -1
    if node.left:
      left_node_height = node.left.height
    right_node_height = -1
    if node.right:
      right_node_height = node.right.height
    return left_node_height > right_node_height
  def _check_error(self, node):
    '''
    Check if there is a problem at this given node.
    Height should already be updated by now.
    '''
    if not node:
      return False
    left_node_height = -1
    if node.left:
      left_node_height = node.left.height
    right_node_height = -1
    if node.right:
      right_node_height = node.right.height
    return (node.height-1) - left_node_height > 1 or (node.height-1) - right_node_height > 1
  def _left_heavier(self, cur_node):
    '''
    Returns which node is heavier, the left or the right
    True: left is heavier
    False: Right is heavier
    '''
    left_node_height = -1
    if not cur_node:
      return
    if cur_node.left:
      left_node_height = cur_node.left.height
    right_node_height = -1
    if cur_node.right:
      right_node_height = cur_node.right.height
    return left_node_height > right_node_height
  def insert(self, value):
    '''
    Inserts a node into the AVL Tree and then fixes the AVL Property.
    '''
    assert not self.search(value), "Node already Exists in the Tree."

    new_node = self._insert_without_fix(value) # Node is inserted normally
    # Back Propagate back up the tree, fixing issues with the AVL property as you move up the tree.
    cur_node = new_node
    while cur_node:
      # Update height and check for problems
      cur_node.height = self._compute_height(cur_node)
      # Check if problem
      if self._check_error(cur_node):
        # Right Heavy or Left Heavy?
        left_heavy = self._is_left_heavy(cur_node)
        if left_heavy:
          # Left Heavy
          left_heavier = self._left_heavier(cur_node.left)
          if not left_heavier:
            self._rotate_left(cur_node.left)
          self._rotate_right(cur_node)
        else:
          # Right Heavy, Two cases: Right node is heavier on the right, right node is heavier on the left(2 Rotate) 
          left_heavier = self._left_heavier(cur_node.right)
          if left_heavier:
            self._rotate_right(cur_node.right)
          self._rotate_left(cur_node)
      cur_node = cur_node.parent
    
  def _insert_without_fix(self, value):
    '''
    Adds a node into the AVL Tree without fixing the AVL Property, returns where the node was inserted so parent function can fix it. 
    '''
    new_node = AVLNode(value)
    if not self.root:
      self.root = new_node
      return # Insert as root if AVL tree is empty.
    # Otherwise, you have a root
    cur_node = self.root
    while cur_node.left or cur_node.right:
      # Locate where the node should be inserted.
      if new_node.value < cur_node.value:
        if not cur_node.left:
          cur_node.left = new_node
          new_node.parent = cur_node
          return new_node
        cur_node = cur_node.left
      else:
        if not cur_node.right:
          cur_node.right = new_node
          new_node.parent = cur_node
          return new_node
        cur_node = cur_node.right
    # No other paths, so insert into the tree
    if new_node.value > cur_node.value:
      cur_node.right =new_node
    else:
      cur_node.left = new_node
    new_node.parent = cur_node
    return new_node

  def _balance(self, node):
    '''
    Propagates up the tree from a given node, using rotations to fix any problems in the tree, used in self.delete
    node: the parent of the node deleted.
    This method also updates the height accordingly
    '''     
    cur_node = node
    while cur_node:
      cur_node.height = self._compute_height(cur_node)
      # Check for errors
      discrepency = self._check_error(cur_node)
      if discrepency:
        # Check which side heavy
        left_heavy = self._is_left_heavy(cur_node)
        if left_heavy:
          # Case 1: Zig Zag(Left Heavy -> Right Heavy)
          if not self._left_heavier(cur_node.left):
            self._rotate_left(cur_node.left)
          self._rotate_right(cur_node)
        else:
          # Right heavy, Case 1: Zig Zag(Right Heavy -> Left Heavy)
          if self._left_heavier(cur_node.right):
            self._rotate_right(cur_node.right)
          self._rotate_left(cur_node)
      cur_node = cur_node.parent
  def _locate(self, value):
    '''
    Locates a Value inside of a tree, returns False if the Node doesnt exist.
    '''
    
    cur_node = self.root
    if not cur_node:
      return False
    while cur_node.left or cur_node.right:
      if cur_node.value == value:
        return cur_node
      if value < cur_node.value:
        if not cur_node.left:
          return False
        cur_node = cur_node.left
      else:
        if not cur_node.right:
          return False
        cur_node = cur_node.right
    if cur_node.value == value:
      return cur_node
    return False
  def delete(self, value):
    '''
    Deletes a Node from the tree, by first locating the node, deleting it, and then restoring the AVL property
    '''
    # Locate node 
    to_delete = self._locate(value)
    assert to_delete, "Node doesnt exist in tree"

    # Case 1: No Children
    parent_node = None
    if not to_delete.left and not to_delete.right:
      parent_node = to_delete.parent
      to_delete.parent = None
      if not parent_node:
        # This was the root
        self.root = None
        return 
      elif parent_node.left == to_delete:
        parent_node.left = None
      else:
        parent_node.right = None
    elif (to_delete.left and not to_delete.right) or (to_delete.right and not to_delete.left):
      # Case 2: One child
      parent_node = to_delete.parent
      if to_delete.left:
        to_delete.left.parent = parent_node
        if not parent_node:
          self.root = to_delete.left
        elif parent_node.right == to_delete:
          parent_node.right = to_delete.left
        else:
          parent_node.left = to_delete.left
      else:
        to_delete.right.parent = parent_node
        if not parent_node:
          self.root = to_delete.right
        if parent_node.right == to_delete:
          parent_node.right = to_delete.right
        else:
          parent_node.left = to_delete.right
    else:
      # Two Children, locate successor(Since we have 2 children, we know a successor exists)
      successor = self.successor(to_delete.value) # The Successor of this node
      to_delete.value = successor.value # Replace the deleted node with it's "successor"
      # Delete the successor, which has to be either case 1 or 0
      parent_node = successor.parent
      if not successor.left and not successor.right:
        if parent_node.left == successor:
          parent_node.left = None
        else:
          parent_node.right = None
      else:
        # Case 2
        if successor.left:
          if not parent_node:
            self.root = successor.left
          elif parent_node.left == successor:
            parent_node.left = successor.left
            successor.left.parent = parent_node
          else:
            parent_node.right = successor.left
            successor.left.parent = parent_node
        else:
          if not parent_node:
            self.root = successor.right
          elif parent_node.left == successor:
            parent_node.left = successor.right
            successor.right.parent = parent_node
          else:
            parent_node.right = successor.right
            successor.right.parent = parent_node
    self._balance(parent_node) # Solve from the parent node up  
  def in_order_print(self, cur_node):
    '''
    Performs a Recursive in order traversal, printing as it goes.
    '''
    if not cur_node:
      return
    else:
      if cur_node.left:
        self.in_order_print(cur_node.left)
      print(cur_node.value)
      if cur_node.right:
        self.in_order_print(cur_node.right)
  def AVLSort(self):
    '''
    Performs in order traversal, using a Queue
    '''
    cur_node = self.root
    queue = Queue()
    Val = []
    visited = []
    while True:
      first = False
      if cur_node.left and cur_node.left.value not in visited:
        visited += [cur_node.value]
        queue.enqueue(cur_node)
        cur_node = cur_node.left
        continue
      Val += [cur_node.value]
      # Check if there is a right child
      if cur_node.right:
        cur_node = cur_node.right
      else:
        if queue.empty():
          return Val
        cur_node = queue.dequeue()
    return Val
  def predecessor(self, value):
    '''
    Normal BST Operation. Locates the Predecessor of a Given Node, and returns False if it doesnt exist.
    '''
    node = self._locate(value)
    if not node:
      return False
    elif not node.left:
      return False
    cur_node = node.left
    while cur_node.left:
      cur_node = cur_node.left
    return cur_node
  def successor(self, value):
    '''
    Normal BST Operation. Locates the Successor of a given node, and returns False if it doesnt exist.
    '''
    # Locate the Node
    node = self._locate(value)
    if not node:
      return False
    elif not node.right:
      return False
    cur_node = node.right
    while cur_node.left:
      cur_node = cur_node.left
    return cur_node


# Sample AVL Tree Configuration
avlTree = AVLTree()
# Inserts
avlTree.insert(3)
avlTree.insert(2)
avlTree.insert(5)
avlTree.insert(6)
avlTree.insert(7) 
avlTree.insert(8)
avlTree.insert(1) 
# Deletions
avlTree.delete(8) # Causes a discrepency
avlTree.in_order_print(avlTree.root)
