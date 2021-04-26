# This Python Script details a Van Embe Boas Tree, which supports O(LogLogU) insertions, Deletions, and Predecessor/Successor
import math
class Summary():
    # Summary Node
    def __init__(self):
        self.exists = False # Denotes if a given node exists or not in general
class Cluster():
    def __init__(self, universe_size, successor = False):
        self.clusters = {} # Either more clusters or a binary number(1 or None)
        self.successor = successor # Tree Construction changes based on what the goal is.
        self.universe_size = universe_size
        # For convienience, assert that the sqrt is integer.
        # precompute the square root of the universe size.
        self.sqrt = math.ceil(math.sqrt(self.universe_size))
        self.more_trees = int(self.sqrt) > 2 # After 2, splitting doesn't do anything
        if not self.more_trees:
            self.sqrt = self.universe_size
        # Create the summary nodes.
        self.summary = {}
        # Create Min Nodes
        self.min_nodes = None
        # Create Max nodes
        self.max_nodes = None
        # Summary Max and Min
        self.summary_min = None # Min never used in predeccessor
        self.summary_max = None # Max never used in successor
        # Initialize Nodes
        for idx in range(self.sqrt):
            self.summary[idx] = Summary() # Summary Node, used mostly in deletion.
            if self.more_trees:
                self.clusters[idx] = Cluster(self.sqrt, successor = self.successor)
            else:
                self.clusters[idx] = None
    def high(self, x):
        # Computes the Tree Value
        tree = x // self.sqrt
        return tree
    def low(self, x):
        tree = x % self.sqrt
        return tree

    #--------------------Check Methods-----------------
    def check_successor(self):
        assert self.successor # Simple Check
    def check_predecessor(self):
        assert not self.successor # Simple Check
    # -------------------Successor Methods------------------------------
    def search_successor(self, key):
        # Search in O(LogLogU) time
        high = self.high(key)
        low = self.low(key)
        if self.min_nodes == key:
            return True
        if not self.summary[high].exists: # Search the Summary Vector
            return False
        return self.clusters[high].search_successor(low)
    def find_successor(self, orig_key):
        # check min nodes first
        if self.min_nodes is not None:
            if orig_key < self.min_nodes:
                return self.min_nodes
            if self.summary_min is not None:
                if orig_key < self.summary_min:
                    return self.summary_min
        # Recursively searches the tree for the first value present
        high = self.high(orig_key)
        low = self.low(orig_key)
        # Check if it can exist in the current cluster
        if self.clusters[high] is not None:
            if self.clusters[high].max_nodes is not None:
                if self.clusters[high].max_nodes > orig_key:
                    # Search Current Cluster
                    value = self.clusters[high].find_successor(low)
                    idx = high * self.sqrt + value
                    return idx

        # Search Summary Vector
        for idx in range(high + 1, self.sqrt):
            if self.summary[idx].exists:
                item = self.clusters[idx] # Non-zero value
                if isinstance(item, Cluster):
                    # Recurse
                    val = item.find_successor(low)
                    if val is None:
                        continue
                    return_val = self.sqrt * idx + val
                    if return_val== orig_key:
                        continue
                    return return_val
                else:
                    # Value found, base case
                    return idx
        return None
    def insert_summary_successor(self, key):
        self.check_successor()
        high = self.high(key)
        low = self.low(key)

        if self.more_trees:
            # Continue recursively
            self.clusters[high].insert_summary_successor(low)
            self.summary[high].exists = True
        else:
            self.summary[low].exists = True
    def insert_successor(self, key):
        self.check_successor()
        high = self.high(key) # Index of the Next Tree Level
        low = self.low(key) # Index Position in the next Tree

        # Update Summary Trees, Eagerly.
        if not self.summary[high].exists:
            # nothing exists in summary so update.
            if self.more_trees:
                self.clusters[high].insert_summary_successor(low)
                self.summary[high].exists = True
            else:
                self.summary[low].exists = True # node exists now.

        # Case 1: min node doesn't even exist
        if self.min_nodes is None:
            self.min_nodes = key
            return # Lazy Propagation

        # Case 2: if key < min
        if key < self.min_nodes:
            # Swap, min is never inserted, only into summary vector
            tmp = self.min_nodes
            self.min_nodes = key
            key = tmp
            self.summary_min = key

        if self.min_nodes is not None and self.summary_min is None:
            # Set Summary Min to trailblaze.
            self.summary_min = key
        high = self.high(key)
        low = self.low(key)

        # Update High and Low
        if not self.more_trees:
            # Last tree height, insert into position
            self.summary[high].exists = True
        else:
            # Continue down.
            self.clusters[high].insert_successor(low)
    def delete_successor(self, key):
        self.check_successor()
        # Start deletion
        high = self.high(key)
        low = self.low(key)
        if key == self.min_nodes:
            # Delete this node, move min nodes to the successor(OLgLgN), this makes delete slower than insert. Used primarily when you don't delete much but msotly insert..
            i = self.summary_min
            if i is None:
                self.min_nodes = None
                return # O(1)
            self.summary_min = self.find_successor(i)
            self.min_nodes = i
        if self.clusters[high] is None:
            return
        self.clusters[high].delete_summary_successor(low)
        self.clusters[high].delete_successor(low)
        self.summary_min = self.find_successor(key)

    def delete_summary_successor(self, key):
        self.check_successor()
        high = self.high(key)
        low = self.low(key)
        if self.clusters[high] is None:
            self.summary[low].exists = False
        else:
            self.clusters[high].delete_summary_successor(low)

    # -------------------Predecessor Methods----------------------
    def search_predecessor(self, key):
        # Search in a predecessor tree in O(lgLgN)
        high = self.high(key)
        low = self.low(key)
        if self.max_nodes == key:
            return True
        if self.clusters[high] is None:
            return self.summary[low].exists
        if self.summary[high].exists:
            return self.clusters[high].search_predecessor(low)
        return False
    def find_predecessor(self, key):
        self.check_predecessor()
        # computes the predecessor item in LgLgN time.
        high = self.high(key)
        low = self.low(key)
        # Check first, if the predecessor exists in the current cluster
        if self.max_nodes is not None:
            if self.max_nodes < key:
                return self.max_nodes
            if self.summary_max is not None:
                if self.summary_max < key:
                    return self.summary_max
        # Check summary vector for first branch
        for i in range(high, -1, -1):
            if self.summary[i].exists:
                if self.clusters[i] is not None:
                    idx = self.clusters[i].find_predecessor(low)
                    if idx is None:
                        return None
                    val = idx + high * self.sqrt
                    if val == key:
                        continue
                    return val
                else:
                    return i
        return None
    def insert_summary_predecessor(self, key):
        self.check_predecessor()
        high = self.high(key)
        low = self.low(key)
        if self.clusters[high] is not None:
            self.clusters[high].insert_summary_predecessor(low)
            self.summary[high].exists = True
        else:
            self.summary[low].exists = True
    def insert_predecessor(self, key):
        self.check_predecessor()
        high = self.high(key)
        low = self.low(key)

        if self.max_nodes is None:
            self.max_nodes = key
            return # O(1)
        if key > self.max_nodes:
            # Swap
            tmp = self.max_nodes
            self.max_nodes = key
            key = tmp
            self.summary_max = key

        if self.max_nodes is not None and self.summary_max is None:
            self.summary_max = key
        high = self.high(key)
        low = self.low(key)
        if self.clusters[high] is None:
            # Base Case
            self.summary[low].exists = True
            return
        if not self.summary[high].exists:
            # Insert exist in summary structure
            self.clusters[high].insert_summary_predecessor(low)
            self.summary[high].exists = True
        self.clusters[high].insert_predecessor(low)
    def delete_summary_predecessor(self, key):
        self.check_predecessor()
        high = self.high(key)
        low = self.low(key)
        if self.clusters[high] is not None:
            self.clusters[high].delete_summary_predecessor(low)
            self.summary[high].exists = False
        else:
            self.summary[low].exists = False
    def delete_predecessor(self, key):
        self.check_predecessor()
        high = self.high(key)
        low = self.low(key)
        if key == self.max_nodes:
            i = self.summary_max
            if i is None:
                self.max_nodes = None
                return # O(1)
            prev = self.find_predecessor(i)
            self.summary_max = pred
            self.max_nodes = i
        if self.clusters[high] is None:
            # Base Case
            if self.summary_max == key:
                self.summary_max = self.find_predecessor(key) # Only one of these calls are ever made.
            return
        self.clusters[high].delete_summary_predecessor(low)
        self.clusters[high].delete_predecessor(low)
        if self.summary_max == key:
            self.summary_max = self.find_predecessor(key)

def main():
    # Construct Sample Tree, with universe size 8(1 - 8 is available keys)
    universe_size = 8
    successor = False # predecessor search
    tree = Cluster(universe_size, successor = successor)
    tree.insert_predecessor(2)
    tree.insert_predecessor(5)
    tree.insert_predecessor(1)
    print(tree.search_predecessor(1))
    tree.delete_predecessor(1)
    print(tree.find_predecessor(8))
if __name__ == '__main__':
    main()
