'''
Practicing a variety of DP Problems, increasing in difficulty.
'''
import collections
import copy
class LongestIncreasingSubsequence:
    '''
    Given a list of numbers, compute the longest increasing subsequence
    O(N^2) Solution: Iterate over all numbers, and compute longest increasing on suffix.
    '''
    def __init__(self, sequence):
        self.sequence = sequence
        self.num_items = len(self.sequence)
        self.memoized = {}
    def reset(self):
        self.memoized = {}
    def dp(self, i, cur_list):
        '''
        i: Index of the suffix
        highest_int: Highest int used so far.
        cur_len
        '''
        if (i, tuple(cur_list)) in self.memoized:
            return self.memoized[i, tuple(cur_list)]
        elif i == self.num_items - 1:
            return cur_list # Nothing left to check
        else:
            if cur_list == []:
                highest_int = float('-inf')
            else:
                highest_int = cur_list[-1] # Extract Highest Value from array
            # Iterate through rest of integers.
            longest_list = None
            longest_length = 0
            for integer in self.sequence[i:]:
                if integer > highest_int:
                    new_list = copy.deepcopy(cur_list + [integer])
                    tmp_list = self.dp(i + 1, new_list)
                    tmp_length = len(tmp_list)
                    if longest_list == None:
                        longest_list = tmp_list
                        longest_length = tmp_length
                    elif tmp_length > longest_length:
                        longest_length = tmp_length
                        longest_list = tmp_list
            result = longest_list
            if result == None:
                # Nothing Found
                result = cur_list
        self.memoized[(i, tuple(cur_list))] = result
        return result
    def solve(self):
        return self.dp(0, [])
class ChangeProblem:
    '''
    Given Change needed, minimize coins returned using dynamic programming.
    I know you can in theory use modulos, but Im experimenting with DP, so its O(nC), where n is change(Pseudo Polynomial - Not great.)
    coins are abitrary in value, input as list of values.
    '''
    def __init__(self, change, coins):
        self.coins = coins
        self.change = change
        self.memoized = {}
        self.parent_pointers = {}
    def reset(self):
        self.memoized = {}
        self.parent_pointers = {}
    def dp(self, num_coins, remaining_change):
        '''
        num_coins: coins used so far(State variable)
        remaining_change: How much change still needed(State variable)
        '''
        if (num_coins, remaining_change) in self.memoized:
            return self.memoized[num_coins, remaining_change]
        elif remaining_change == 0:
            self.memoized[(num_coins, remaining_change)] = num_coins
            self.parent_pointers[(num_coins, remaining_change)] = []
            return num_coins
        else:
            smallest_coins = float('inf')
            coin_paths = []
            coin_chg = 0
            for coin in self.coins:
                chg =  round(remaining_change - coin, 2)
                if chg < 0:
                    # Gave Back too much Change.
                    continue
                coins_used = self.dp(num_coins + 1, chg) # Prev Coin + this one.
                coin_path = self.parent_pointers[num_coins + 1, chg] + [coin]
                if coin_paths == None:
                    coin_paths = coin_path
                    smallest_coins = coins_used
                    coin_chg = chg
                elif coins_used < smallest_coins:
                    smallest_coins = coins_used
                    coin_paths = coin_path
                    coin_chg = chg
        self.memoized[(num_coins, remaining_change)] = smallest_coins
        self.parent_pointers[(num_coins, remaining_change)] = coin_paths
        return smallest_coins
    def solve(self):
        smallest_coins = self.dp(0, self.change)
        return smallest_coins, collections.Counter(self.parent_pointers[0, self.change])
class EditDistance:
    '''
    Find the minimum operations to convert STR1 -> STR2
    Distance is classified into three moves:
    - Insert a Character in STR1
    - Delete a Character in STR1
    - Replace a Character in STR1
    Cost is all the same(Unless specified in cost_matrix).
    Check takes O(n)
    DP takes O(3N^2)
    '''
    def __init__(self, string1, string2, cost_matrix):
        # Cost matrix: list of 3 vals in the order of (Insert, Delete, Replace)
        assert isinstance(cost_matrix, list) and len(cost_matrix) == 3
        self.cost_matrix = cost_matrix
        for i in self.cost_matrix:
            assert isinstance(i, (int, float))
        self.costs = {"INSERT": self.cost_matrix[0], "DELETE": self.cost_matrix[1], "REPLACE": self.cost_matrix[2]}
        self.string1 = string1
        self.string2 = string2

        self.string1_len = len(self.string1) # compute this only once(O(N))
        self.string2_len = len(self.string2)

        self.memoized = {}
        self.parent_pointers = {} # Stores the Action taken.
    def reset(self):
        self.memoized = {}
        self.parent_pointers = {}
    def convert_to_arr(self, string):
        string_arr =[]
        for char in string:
            string_arr += [ord(char)]
        return string_arr
    def dp(self, i, j):
        '''
        i: index of string 1, the number of characters traversed.
        j: index of string 2, basically the number of characters matched.

        When str1[i] != str2[j], 3 solutions to resolve problem:
        - Delete Str1[i]
        - Insert str2[j] at i
        - Replace str1[i] with str2[j]
        '''
        if (i, j) in self.memoized:
            return self.memoized[i, j]
        else:
            if i == self.string1_len and j == self.string2_len:
                return 0
            # Corner Case: j already finished, so we can only delete
            elif j == self.string2_len:
                result = self.dp(i + 1, j) + self.costs['DELETE']
                action = f'DELETE {self.string1[i]}'
            # Corner case: i already finished, so we can only insert
            elif i == self.string1_len:
                result = self.dp(i, j + 1) + self.costs["INSERT"]
                action = f'INSERT {self.string2[j]}'
            # Corner Case: str1[i] == str2[j]
            elif self.string1[i] == self.string2[j]:
                result = self.dp(i + 1, j + 1)
                action = f"SKIP: {self.string2[j]}"
            else:
                # Try all three options, minimize the results
                result_replace = self.dp(i + 1, j + 1) + self.costs['REPLACE']
                result_insert = self.dp(i, j + 1) + self.costs['INSERT']
                result_delete = self.dp(i + 1, j) + self.costs["DELETE"]

                if result_replace <= result_insert and result_replace <= result_delete:
                    result = result_replace
                    action = f"REPLACE {self.string1[i]} with {self.string2[j]}"
                elif result_insert <= result_replace and result_insert <= result_delete:
                    result = result_insert
                    action = f"INSERT {self.string2[j]}"
                else:
                    result= result_delete
                    action= f"DELETE {self.string1[i]}"
        self.memoized[i, j] = result
        self.parent_pointers[i, j] = action
        return result
    def solve(self):
        min_dist = self.dp(0, 0)
        # Decode Changes made
        actions = []
        cur_i = 0
        cur_j = 0
        while True:
            if (cur_i, cur_j) not in self.parent_pointers:
                break
            action = self.parent_pointers[cur_i, cur_j]
            actions += [action]
            if action[0] == 'D':
                # Deleted
                cur_i += 1
            elif action[0] == 'I':
                # Inserted
                cur_j += 1
            elif action[0] == 'S':
                cur_i += 1
                cur_j += 1
            else:
                # Replaced
                cur_i += 1
                cur_j += 1
        return min_dist, actions
class ComputationalBiology:
    '''
    Variation on Edit Distance, minimum cost needed to align two DNA strings
    - Since this is pretty similar to edit distance, I will be practicing the bottom-up form of DP.

    Actions that can be performed:
    - Add a space in str1
    - Add a space in str2
    Cost: Number of mismatches, where char(or space) matched to the wrong char.

    Uses the Needleman-Wunsch Algorithm, for O(mn) time.
    '''
    def __init__(self, string1, string2, cost_matrix):
        self.string1 = string1
        self.string2 = string2
        self.cost_matrix = cost_matrix
        # Cost matrix should be in the form of [Space Penalty, Mismatch Penalty]
        assert isinstance(self.cost_matrix, list) and len(self.cost_matrix) == 2
        self.costs = {"SPACE": self.cost_matrix[0], 'MISMATCH': self.cost_matrix[1]}

        self.valid_chars = ['c', 'g', 'a', 't']
        for char in self.string1:
            assert char in self.valid_chars

        self.string1_len = len(self.string1)
        self.string2_len = len(self.string2)
    def bottom_up_dp(self):
        '''
        Computes the alignment using a bottom up manner.
        '''
        # Initialize Distance Matrix
        memoized = [[float('inf') for i in range(self.string1_len + 1)] for j in range(self.string2_len + 1)]
        memoized[0][0] = 0

        parent_pointers = [['NULL' for i in range(self.string1_len + 1)] for j in range(self.string2_len + 1)]
        for i in range(self.string2_len + 1): # Columns
            for j in range(self.string1_len + 1): # Rows
                if memoized[i][j] != float('inf'):
                    continue # Value already solved.
                # Corner Case: I == 0(Gap only to the down)
                elif i == 0:
                    memoized[i][j] = memoized[i][j - 1] + self.costs['SPACE']
                    parent_pointers[i][j] = (i, j - 1)
                #Corner Case: J == 0(Gap only to the right)
                elif j == 0:
                    memoized[i][j] = memoized[i - 1][j] + self.costs['SPACE']
                    parent_pointers[i][j] = (i - 1, j)
                # Else, Try All Options
                else:
                    result_up_gap = memoized[i][j-1] + self.costs['SPACE']
                    result_right_gap = memoized[i - 1][j] + self.costs['SPACE']
                    # Check if match
                    match_penalty = 0 if self.string1[j - 1] == self.string2[i - 1] else self.costs['MISMATCH']
                    result_diag = memoized[i - 1][j - 1] + match_penalty

                    # Minimize
                    if result_up_gap <= result_right_gap and result_up_gap <= result_diag:
                        memoized[i][j] = result_up_gap
                        parent_pointers[i][j] = (i, j - 1)
                    elif result_right_gap <= result_up_gap and result_right_gap <= result_diag:
                        memoized[i][j] = result_right_gap
                        parent_pointers[i][j] = (i - 1, j)
                    else:
                        memoized[i][j] = result_diag
                        parent_pointers[i][j] = (i - 1, j - 1)
        return memoized, parent_pointers


    def solve(self):
        memoized, parent_pointers = self.bottom_up_dp()
        smallest_dist = memoized[-1][-1]
        # Store the path and reverse
        path = []
        cur_i = self.string2_len
        cur_j = self.string1_len
        while True:
            path += [(cur_i, cur_j)]
            nextVal = parent_pointers[cur_i][cur_j]
            if nextVal == "NULL":
                break
            cur_i, cur_j = nextVal
        path = path[::-1]

        string1 = ""
        string2 = ''
        cur_i, cur_j = path[0]
        for idx in range(1, len(path)):
            next_i, next_j = path[idx]
            print(next_i, next_j)
            if cur_i == next_i:
                string2 += "_"
            else:
                string2 += self.string2[next_i - 1]
            if cur_j == next_j:
                string1 += '_'
            else:
                string1 += self.string1[next_j - 1]
            cur_i, cur_j = (next_i, next_j)
        return smallest_dist, string1, string2

class InterleavingStrings:
    '''
    Given Strings X, Y, and Z, see if Z can be written as an interleaved string of X and Y(characters must be kept in order)
    '''
    def __init__(self, s1: str, s2: str, s3: str) -> None:
        self.memoized = {}
        self.len_s1 = len(s1)
        self.len_s2 = len(s2)
        self.len_s3 = len(s3)
        self.s3 = s3
        self.s1 = s1
        self.s2 = s2
        if self.len_s1 + self.len_s2 != self.len_s3:
            return False

    def dp(self, i, j):
        if (i, j) in self.memoized:
            return self.memoized[i, j]
        else:
            if i == self.len_s1 and j == self.len_s2:
                return True
            elif i == self.len_s1:
                if self.s2[j] != self.s3[i + j]:
                    return False
                else:
                    result = self.dp(i, j + 1)
            elif j == self.len_s2:
                if self.s1[i] != self.s3[i + j]:
                    return False
                else:
                    result = self.dp(i + 1, j)
            else:
                one_result = None
                two_result = None
                if self.s1[i] == self.s3[i + j]:
                    one_result = self.dp(i + 1, j)
                if self.s2[j] == self.s3[i + j]:
                    two_result = self.dp(i, j + 1)
                if one_result or two_result:
                    result = True
                else:
                    result = False
        self.memoized[i, j] = result
        return result
    def solve(self):
        return self.dp(0, 0)

class TravellingSalesmanProblem:
    '''
    The Classic Travelling Salesman Problem, NP Hard Problem
    Given N cities, with weight N[i, j] representing cost from i to j
    Minimize Cost from i -> i, visiting all cities.

    O(N^2 * 2^N) DP implementation.
    '''
    def unique_nodes(self, weights):
        unique = []
        new_weights = {}
        for a, b in weights:
            unique += [a]
            unique += [b]
            new_weights[(a, b)] = weights[(a, b)]
            new_weights[(b, a)] = weights[(a, b)]
        return set(unique), new_weights
    def __init__(self, weights):
        self.weights = weights # dictionary of len n^2
        self.nodes_unique, self.weights = self.unique_nodes(self.weights)
        self.num_nodes = len(self.nodes_unique)
        self.memoized = {}
        self.parent_pointers = {}
    def reset(self):
        self.memoized ={}
        self.parent_pointers = {}
    def dp(self, orig_node,  cur_node, nodes_visited):
        sorted_nodes = tuple(sorted(list(nodes_visited))) # O(N^2LogN), still less than O(2^N),so it's fine.
        nodes_visited.add(cur_node)
        if len(nodes_visited) == self.num_nodes:
            return 0
        if (cur_node, sorted_nodes) in self.memoized:
            return self.memoized[(cur_node, sorted_nodes)]

        else:
            other_nodes = self.nodes_unique.symmetric_difference(nodes_visited)
            action = None
            result = float('inf')
            for node in other_nodes:
                tmp_nodes = copy.deepcopy(nodes_visited)
                weight = self.dp(orig_node, node, tmp_nodes)
                weight += self.weights[(cur_node, node)]
                if action == None:
                    action = node
                    result = weight
                if weight < result:
                    result = weight
                    action = node

        self.memoized[(cur_node, sorted_nodes)] = result
        self.parent_pointers[(cur_node, sorted_nodes)] = action
        return result
    def solve(self):
        # Iterate over all nodes
        best_path = None
        best_weight = float('inf')
        node_order = ['a', 'd', 'b', 'c']
        for node in node_order:
            result = self.dp(node, node, set())
            # Decode Predictions
            cur_node = node
            weight = self.memoized[(cur_node, ())]
            cur_set = []
            path = [cur_node]
            while True:
               if len(cur_set) == self.num_nodes - 1:
                   break
               cur_set = sorted(cur_set)

               next_node = self.parent_pointers[(cur_node, tuple(cur_set))]
               cur_set += [cur_node]
               path += [next_node]
               cur_node = next_node
            final_weight = self.weights[(cur_node, node)] + weight
            path += [node]
            if best_path == None:
                best_path = path
                best_weight = final_weight
            if final_weight < best_weight:
                best_weight = final_weight
                best_path = path
        return best_path, best_weight
def main():
    weights = {
        ('a', 'b'): 10,
        ('a', 'c'): 35,
        ('a', 'd'): 25,
        ('b', 'd'): 20,
        ('d', 'c'): 30,
        ('b', 'c'): 15,
    }
    solver = TravellingSalesmanProblem(weights)
    start, weight = solver.solve()
    print(weight)
    print(start)
if __name__ == '__main__':
    main()