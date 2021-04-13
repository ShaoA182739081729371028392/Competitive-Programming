'''
This code covers slightly more advanced techniques for Dynamic Programming.
'''
class LongestPalindromicSequence():
    '''
    Computes the longest palindromic Sequence(Not including spaces), warmup problem.

    The sequence doesnt have to be direct, or else there would be no point for DP, just compute the min over all subsequences.

    '''
    def clean_text(self, x):
        string = ''
        for char in x:
            if char != ' ':
                string += char
        return string
    def __init__(self, string1):
        self.string1 = str.lower(self.clean_text(string1))
        self.len = len(self.string1)
        self.memoized = {}
        self.parent_pointers = {}
    def reset(self):
        self.memoized = {}
        self.parent_pointers = {}
    def dp(self, i, j):
        '''
        Recursively Computes the Longest Palidromic SubSequence
        Stored as (i, j), where palidrome is str[i: j]
        '''
        if (i, j) in self.memoized:
            return self.memoized[i, j]
        else:
            if i == j:
                # Even Length Palidrome, Center is between two letters
                result = 0
                path = None
            elif j - i == 1:
                result = 1
                path = None
            else:
                # Recursive Case
                inner = self.dp(i + 1, j - 1)
                if self.string1[i] == self.string1[j - 1]:
                    inner += 2
                outer = self.dp(i + 1, j)
                if inner > outer:
                    result = inner
                    path = (i + 1, j - 1)
                else:
                    result = outer
                    path = (i + 1, j)

        self.memoized[i, j] = result
        self.parent_pointers[i, j] = path
        return result
    def solve(self):
        longest = self.dp(0, self.len)
        # Decode Predictions
        cur_node = (0, self.len)
        string = [None for i in range(longest)]
        cur_length = self.memoized[cur_node]
        i = 0
        while True:
            next_node = self.parent_pointers[cur_node]
            if next_node == None:
                if cur_node[0] != cur_node[1]:
                    # One Letter in the center
                    string[i] = self.string1[cur_node[0]]
                break
            next_length = self.memoized[next_node]
            if next_length != cur_length:
                string[i] = self.string1[cur_node[0]]
                string[-(i + 1)] = self.string1[cur_node[-1] - 1]
                i += 1
            cur_node = next_node
            cur_length = next_length
        # Create Substring from List
        str_string = ''
        for char in string:
            str_string += char
        return longest, str_string
class VisualizeBST:
    '''
    Just a Data structure to visualize the results after. No Real BST operations here.
    '''
    def __init__(self, arr):
        '''
        Array of nodes
        '''
        self.arr = arr

    def __str__(self):
        '''
        Print the structure of the BST.

        Pretty Print it, layer by layer.
        '''
        remaining_arr = self.arr
        # Flatten the List, one layer at a time
        while True:
            # extract nodes
            flat_list = []
            remaining_array = []
            for i in range(len(remaining_arr)):
                if not isinstance(remaining_arr[i], list):
                    flat_list += [remaining_arr[i]]
                    remaining_array += remaining_arr[i - 1]
                    remaining_array += remaining_arr[i + 1]
            if len(flat_list) == 0:
                break
            print(flat_list)
            remaining_arr = remaining_array
        return ""


class WeightedOptimalBST:
    def __init__(self, nodes):
        '''
        Nodes: dict(node_name -> weight)
        O(N^3 LogN), N^2logN memoized, N / 2 Per Recursion
        '''
        for key in nodes:
            assert isinstance(key, (int, float))
        self.nodes = nodes
        self.num_nodes = len(self.nodes)
        # Sort Nodes
        self.node_names = sorted(self.nodes)

        self.memoized = {} # Stores the total cost of storing the node there.
        self.parent_pointers = {}
    def reset(self):
        self.memoized = {}
        self.parent_pointers = {}
    def dp(self, remaining_nodes, depth):
        hashable_remaining = tuple(remaining_nodes)
        if (hashable_remaining, depth) in self.memoized:
            return self.memoized[hashable_remaining, depth]
        else:
            if len(remaining_nodes) == 0:
                return 0
            else:
                # Try all remaining nodes as a head
                best_val = float('inf')
                best_head = None
                for node_idx in range(len(remaining_nodes)):
                    left_nodes = remaining_nodes[:node_idx] # Kept in sorted order.
                    right_nodes = remaining_nodes[node_idx + 1:]
                    center_node = remaining_nodes[node_idx]
                    weights = self.dp(left_nodes, depth + 1) + self.dp(right_nodes, depth + 1) + self.nodes[center_node] * depth
                    if best_head == None:
                        best_head = center_node
                        best_val  = weights
                    if weights < best_val:
                        best_val = weights
                        best_head = center_node
        self.memoized[(hashable_remaining, depth)] = best_val
        self.parent_pointers[(hashable_remaining, depth)] = best_head
        return best_val

    def recur_reconstruct(self, remaining_nodes, depth):
        '''
        Recursively Computes the optimal BST
        '''
        if len(remaining_nodes) == 0:
            return []
        hashable_remaining_nodes = tuple(remaining_nodes)
        center_node = self.parent_pointers[hashable_remaining_nodes, depth]
        # locate the center node
        left_nodes = None
        right_nodes = None
        for idx in range(len(remaining_nodes)):
            if remaining_nodes[idx] == center_node:
                left_nodes = remaining_nodes[:idx]
                right_nodes = remaining_nodes[idx + 1:]
        BST = [self.recur_reconstruct(left_nodes, depth + 1), center_node, self.recur_reconstruct(right_nodes, depth + 1)]
        return BST

    def solve(self):
        best_val = self.dp(self.node_names, 1)
        # Reconstruct the Tree from the optimal root.
        BST = self.recur_reconstruct(self.node_names, 1)
        bst = VisualizeBST(BST)
        return best_val, bst
class CoinProblem:
    '''
    Given an even number of weighted coins, you want to maximize the weight
    of coins taken given the fact that you can only take the first or last coin

    Your opponent can only do the same as well.

    Solved using DP and Min-Max.
    '''
    def __init__(self, coins):
        assert isinstance(coins, list)
        self.coins = coins
        self.num_coins = len(self.coins)
        assert self.num_coins % 2 == 0
        self.memoized = {}
        self.parent_pointers = {}
    def reset(self):
        self.memoized = {}
        self.parent_pointers = {}
    def dp_opponent(self, i, j):
        '''
        Opponents turn, returns the minimum
        '''
        if (i, j) in self.memoized:
            return self.memoized[i, j]
        else:
            if i == j:
                result = self.coins[i]
                action = None # end of Game
            else:
                # Min Optimization - Minimizing self.dp
                dp_i = self.dp(i + 1, j)

                dp_j = self.dp(i, j - 1)

                one = dp_i
                two = dp_j

                if one < two:
                    result = one
                    action = (i + 1, j)
                else:
                    result = two
                    action = (i, j - 1)
        self.memoized[(i, j)] = result
        self.parent_pointers[(i, j)] = action
        return result
    def dp(self, i, j):
        '''
        MY Turn, returns the maximum.
        '''
        if (i, j) in self.memoized:
            return self.memoized[i, j]
        else:
            if j - i == 1:
                # Base Case: two coins left
                if self.coins[i] < self.coins[j]:
                    result = self.coins[j]
                    action = (i, j - 1) # (i, i)
                else:
                    result = self.coins[i]
                    action = (i + 1, j) # (j, j)
            else:
                # Min-Max, Skip DP calls for odd numbers and directly compute min.
                # Path 1: Take i, opponent takes i + 1 or j
                one =  self.coins[i] + self.dp_opponent(i + 1, j)
                # Path 2: Take j, opponent takes i or j - 1
                two = self.coins[j] + self.dp_opponent(i, j - 1)
                if one > two:
                    result = one
                    action = (i + 1, j)
                else:
                    result = two
                    action = (i, j - 1)
        self.memoized[i, j] = result
        self.parent_pointers[i,j] = action
        return result
    def solve(self):
        max_val = self.dp(0, self.num_coins - 1)
        print(f"Best Score: {max_val}")
        # Reconstruct the game
        cur_idx = (0, self.num_coins - 1)
        while True:
            idx_taken = self.parent_pointers[cur_idx]
            if (cur_idx[1] - cur_idx[0]) % 2 == 0:
                print(f"You:from pos: {cur_idx}, took: {idx_taken}")
            else:
                print(f"Me:from pos: {cur_idx}, took: {idx_taken}")
            cur_idx = idx_taken
            if idx_taken[0] == idx_taken[1]:
                break
        return max_val
def main():
    sample_problem = {1: 3,
        2:1,
        3:5,
        4:8,
        5:3,
        6:2
    }
    solver = WeightedOptimalBST(sample_problem)
    best_val, bst = solver.solve()
    print(best_val)
    print(bst)
if __name__ == '__main__':
    main()