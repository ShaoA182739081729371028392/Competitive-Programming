# This Python File performs easy augmentation of an AVL Tree, to support Rank and Select in Log(N) time
class AugmentedNode():
    def __init__(self):
        self.value = None
        self.parent = None
        self.left = None
        self.right = None
        self.height = None
        self.left_nodes = 0
        self.right_nodes = 0
        self.local_rank = 0
class Helper:
    @classmethod
    def num_nodes(cls, node):
        if node is None:
            return 0
        return node.left_nodes + node.right_nodes + 1
    @classmethod
    def is_left_child(cls, node, child):
        if node is None:
            return False
        return node.left == child
    @classmethod
    def num_children(cls, node):
        num = 0
        if node.left is not None:
            num += 1
        if node.right is not None:
            num += 1
        return num
    @classmethod
    def is_right_heavy(cls, node):
        left = None if node is None else node.left
        right = None if node is None else node.right

        left_height = -1 if left is None else left.height
        right_height = -1 if right is None else right.height
        return right_height >= left_height
    @classmethod
    def is_left_heavy(cls, node):
        left = None if node is None else node.left
        right = None if node is None else node.right

        left_height = -1 if left is None else left.height
        right_height = -1 if right is None else right.height
        return left_height >= right_height
    @classmethod
    def max_height(cls, node):
        # Computes the max height of the two nodes
        left_height = -1 if node.left is None else node.left.height
        right_height = -1 if node.right is None else node.right.height
        return max(left_height, right_height)
    @classmethod
    def rotate_right(cls, node):
        node_parent = node
        node_left = node.left
        # Shift Around Pointers
        node_parent.left = None if node_left is None else node_left.right
        node_left.right = node_parent
        node_left.parent = node_parent.parent
        node_parent.parent = node_left
        # update heights and rank of node_parent
        max_height = Helper.max_height(node_parent)
        node_parent.height = max_height + 1
        rank = 0 if node_parent.left is None else node_parent.left.local_rank + 1
        left_nodes = Helper.num_nodes(node_parent.left)
        right_nodes = Helper.num_nodes(node_parent.right)
        node_parent.local_rank = rank
        node_parent.left_nodes = left_nodes
        node_parent.right_nodes = right_nodes
    @classmethod
    def rotate_left(cls, node):
        node_parent = node
        node_right = node.right
        # Update Pointers
        node_parent.right = None if node_right is None else node_right.left
        node_right.left = node_parent
        node_right.parent = node_parent.parent
        node_parent.parent = node_right
        # Update height and rank of node_parent
        max_height = Helper.max_height(node_parent)
        node_parent.height = max_height + 1
        rank = 0 if node_parent.left is None else node_parent.left.local_rank + 1
        left_nodes = Helper.num_nodes(node_parent.left)
        right_nodes = Helper.num_nodes(node_parent.right)
        node_parent.local_rank = rank
        node_parent.left_nodes = left_nodes
        node_parent.right_nodes = right_nodes
class EasyAugmentedTree():
    # Easy Augmented - Augmentations and Changes can be kept local
    def __init__(self):
        self.root = None
    def locate(self, value):
        # Locates the node
        assert self.search(value)
        cur_node = self.root
        while cur_node is not None:
            if value == cur_node.value:
                return cur_node
            elif value < cur_node.value:
                cur_node = cur_node.left
                return cur_node
            else:
                cur_node = cur_node.right

    def search(self, value):
        # LogN Search of the Tree.
        cur_node = self.root
        while cur_node is not None:
            if cur_node.value == value:
                return True
            elif value < cur_node.value:
                cur_node = cur_node.left
            else:
                cur_node = cur_node.right
        return False

    def insert(self, value):
        # Unique Values only in the Tree
        assert not self.search(value) # O(logN) anyways.
        node = AugmentedNode()
        node.value = value
        node.height = 0
        node.local_rank = 0
        node.left_nodes = 0
        node.right_nodes = 0
        if self.root is None:
            self.root = node
            return
        cur_node = self.root
        # tree Traversal
        while cur_node:
            if value < cur_node.value:
                if cur_node.left is None:
                    # Insert (maybe erroneuously) into the left, then correct mistakeds
                    cur_node.left = node
                    node.parent = cur_node
                    self.fix_error(cur_node)
                    return
                cur_node = cur_node.left
            else:
                 # Must be right side of tree
                 if cur_node.right is None:
                     cur_node.right = node
                     node.parent = cur_node
                     self.fix_error(cur_node)
                     return
                 cur_node = cur_node.right

    def fix_error(self, node):
        # Recursively solves all errors in the AVLTree, moving up the tree to fix all parent nodes
        # Update height and rank of node
        node.height = Helper.max_height(node) + 1
        if node.left is not None:
            node.local_rank = node.left.local_rank + 1
            node.left_nodes = node.left.left_nodes + node.left.right_nodes + 1
        if node.right is not None:
            node.right_nodes = node.right.left_nodes + node.right.right_nodes + 1
        # Check for errors in the Tree
        left_tree_height = -1 if node.left is None else node.left.height
        right_tree_height = -1 if node.right is None else node.right.height
        abs_error = abs(left_tree_height - right_tree_height)
        if abs_error > 1:
            # Error in the Tree, fix the trees.
            # Case 1: left - right = 2(Larger errors would have been caught by then)
            if left_tree_height - right_tree_height > 1:
                # Case 1: Doubly Left Heavy
                left_heavy = Helper.is_left_heavy(node.left)
                if left_heavy:
                    # Right Rotate
                    node_left = node.left
                    Helper.rotate_right(node)
                    if self.root == node:
                        self.root = node_left
                else:
                    # Case 2: Double Rotation
                    node_left = node.left
                    Helper.rotate_left(node.left)
                    Helper.rotate_right(node)
                    if node == self.root:
                        self.root = node_left
            else:
                right_heavy = Helper.is_right_heavy(node.right)
                # Case 3:  Double Right Heavy
                if right_heavy:
                    node_right = node.right
                    Helper.rotate_left(node)
                    if node == self.root:
                        self.root = node_right
                else:
                    node_right = node.right
                    # Case 4: Double Rotation
                    Helper.rotate_right(node.right)
                    Helper.rotate_left(node)
                    if node == self.root:
                        self.root = node_right
        if node.parent is not None:
            self.fix_error(node.parent)
    def delete(self, value):
        # Standard BST Delete and then update and fix tree.
        node = self.locate(value)
        # Case 1: Is a leaf
        num_children = Helper.num_children(node)
        if num_children == 0:
            # Pick off the node
            parent = node.parent
            is_left_child = Helper.is_left_child(parent, node)
            if is_left_child:
                parent.left = None
            else:
                parent.right = None
            self.fix_error(parent)
        elif num_children == 1:
            to_fix = None
            if node.left is not None:
                parent = node.parent
                is_left_child = Helper.is_left_child(parent, node)
                if is_left_child:
                    parent.left = node.left
                    to_fix = parent.left
                else:
                    parent.right = node.left
                    to_fix = parent.right
            else:
                parent = node.parent
                is_left_child = Helper.is_left_child(parent, node)
                if is_left_child:
                    parent.left = node.right
                    to_fix = parent.left
                else:
                    parent.right = node.right
                    to_fix = parent.right
            self.fix_error(to_fix)
        else:
            # Case: 2 Children
            predecessor = self.predecessor(node)
            node.value = predecessor.value
            self.delete(predecessor)
    def rank(self, value):
        # Computes the global rank of a node
        cur_node = self.root
        rank = 0
        while cur_node:
            if cur_node.value == value:
                return rank + cur_node.local_rank + 1
            elif value < cur_node.value:
                cur_node = cur_node.left
            else:
                rank = rank + Helper.num_nodes(cur_node.left) + 1
                cur_node = cur_node.right

    def select(self, rank):
        cur_node = self.root
        while cur_node:
            num_nodes = Helper.num_nodes(cur_node.left) + 1
            if num_nodes == rank:
                return cur_node
            elif rank < num_nodes:
                cur_node = cur_node.left
            else:
                rank = rank - num_nodes
                cur_node = cur_node.right
        return None
    def predecessor(self, value):
        # Predecessor = Select(Search(x).rank - 1) = 2Log(N)
        rank = self.rank(value)
        rank_to_search = rank - 1
        return self.select(rank_to_search)
    def successor(self, value):
        rank = self.rank(value)
        rank_to_search = rank + 1
        return self.select(rank_to_search)

def main():
    tree = EasyAugmentedTree()
    tree.insert(1)
    tree.insert(2)
    tree.insert(3)
    tree.insert(4)
    tree.delete(1)
if __name__ == '__main__':
    main()