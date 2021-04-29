# Implements Randomized Skip Lists, which support O(LogN) lookup with high probability
import random
class SkipNode():
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None # Doubly Linked List + Skip List
        self.down = None
class Layer():
    # Skip List Layer of Nodes
    def __init__(self, neg_inf = None, pos_inf = None):
        # Initializes a Skip List with -inf and inf nodes to start each node
        self.start = SkipNode(float('-inf'))
        self.start.down = neg_inf
        end = SkipNode(float('inf'))
        end.prev = self.start
        end.down = pos_inf
        self.end = end
        self.start.next = self.end
        self.length = 2
    def __str__(self):
        cur_node = self.start
        string = ''
        while cur_node is not None:
            string += f'{cur_node.value} '
            cur_node = cur_node.next
        return string
    def find_node(self, value):
        cur_node = self.start
        infinity = float('inf')
        while cur_node.value != infinity:
            if cur_node.value == value:
                return cur_node
            cur_node = cur_node.next
        return None
    def insert_node(self, value, down_node = None):
        # Inserts the node and returns a pointer to it(In case of promotion)
        new_node = SkipNode(value)

        cur_node = self.start # Always initialized, so no need for check
        while cur_node.next is not None:
            if cur_node.value <= value and cur_node.next.value >= value:
                new_node.prev = cur_node
                new_node.next = cur_node.next
                new_node.down = down_node
                cur_node.next.prev = new_node
                cur_node.next = new_node
                self.length += 1
                return new_node
            cur_node = cur_node.next

        raise Exception("This should never be reached")
    def find_down(self, node, value):
        # Given a Node, continues through the skip list layer to find where the node exists
        cur_node = node
        while cur_node is not None:
            if cur_node.value == value:
                return cur_node, True # early exit.
            if cur_node.value <= value and cur_node.next.value > value:
                # Should drop down here(If no drop, then node doesn't exist)
                return cur_node.down, False
            cur_node = cur_node.next
        return None, False

class SkipList():
    def __init__(self):
        self.layers = [Layer()]
        self.num_layers = 1
    def __str__(self):
        for i in range(self.num_layers - 1, -1, -1):
            print(self.layers[i].__str__())
        return ''
    def find_first(self, value):
        # Finds the First Instance of a value in the skip list, used in deletion
        cur_layer = self.num_layers - 1
        cur_down = self.layers[cur_layer].start
        cur_down, found = self.layers[cur_layer].find_down(cur_down, value)

        while not found:
            cur_down, found = self.layers[cur_layer].find_down(cur_down, value)
            cur_layer -= 1
            if cur_layer < 0:
                return None, None
        return cur_down, cur_layer

    def search(self, value):
        cur_layer = self.num_layers - 1
        cur_node = self.layers[cur_layer].start
        cur_node, found = self.layers[cur_layer].find_down(cur_node, value)
        while not found:
            cur_node, found = self.layers[cur_layer].find_down(cur_node, value)
            if cur_node is None:
                return False
        return True
    def delete_node(self, node, cur_layer):
        # Deletes a Node from the layer.
        prev = node.prev
        next_node = node.next
        prev.next = next_node
        next_node.prev = prev
        self.layers[cur_layer].length -= 1
    def delete(self, value):
        # Start from the top node, and use down dependencies to delete all nodes
        cur_node, cur_layer = self.find_first(value)

        while cur_node is not None:
            self.delete_node(cur_node, cur_layer)
            cur_layer -=1
            cur_node = cur_node.down

    def insert(self, value):
        # Randomly Inserts and Promotes nodes
        # Insert at lowest level guarenteed
        inserted  = self.layers[0].insert_node(value)
        # Randomly keep inserting
        cur_idx = 1
        while random.random() < 0.5: # Fair Coin
            if cur_idx >= self.num_layers:
                # Add a New Layer, with only this node
                neg_inf = self.layers[cur_idx - 1].start
                pos_inf = self.layers[cur_idx - 1].end
                self.layers.append(Layer(neg_inf = neg_inf, pos_inf = pos_inf))
                self.num_layers += 1
            inserted = self.layers[cur_idx].insert_node(value, down_node = inserted)
            cur_idx += 1
def main():
    skipList = SkipList()
    skipList.insert(0)
    skipList.insert(1)
    skipList.insert(5)
    skipList.delete(1)
    print(skipList)
    print(skipList.search(1))
if __name__ == '__main__':
    main()