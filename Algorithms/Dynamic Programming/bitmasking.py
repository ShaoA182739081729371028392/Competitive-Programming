'''
This file will explore the BitMasking Technique in Dynamic Programming to reduce memory consumption and increase the speed of
Dynamic Programs.
'''
# Starting Off Simple
def count_set_bits(integer):
    count = 0
    cur_int = integer
    while True:
        cur_int = cur_int & (cur_int - 1)
        count += 1
        if cur_int == 0:
            return count
class StringSolver():
    def __init__(self, strings):
        '''
        Returns the maximum length of a pair of strings given that the string has 0 overlapping characters.

        Cant get rid of O(N^2), since each pair of strings needs to be compared, but we can reduce the constants needed using bitwise operations
        '''
        self.orig_strings = strings
        self.string_lengths = [] # Stores lengths to avoid recomputing.
        self.num_strings = 0
        self.strings = [self.generate_bit_mask(str.lower(string)) for string in strings]

    def solve(self):
        '''
        Uses Bitwise AND to assert no overlapping strings
        '''
        max_length = 0
        best_strings = ()
        for i in range(self.num_strings):
            for j in range(i + 1, self.num_strings):
                if self.strings[i] & self.strings[j] != 0:
                    continue
                # Valid string pair
                prod = self.string_lengths[i] * self.string_lengths[j]
                if prod > max_length:
                    max_length = prod
                    best_strings = (self.orig_strings[i], self.orig_strings[j])
        return max_length, best_strings
    def generate_bit_mask(self, string):
        # Forms a BitMask given a string, creating a bitmask using right shifts
        initial_mask = 0
        count = 0
        ascii_shift = 97 # All lowercased
        for char in string:
            assert char.isalpha()
            shifted_bit = 1 << (ord(char) - ascii_shift)
            initial_mask |= shifted_bit # Mask bit in this position, duplicates are fine, since
            count += 1
        self.string_lengths += [count]
        self.num_strings += 1
        return initial_mask

class HamiltonianPath:
    '''
    Solves the Hamiltonian Path Problem using Bitmasking.

    Cities should be characters, starting from A. This makes bitmasking easier.

    Ex.

    A
    B
    C
    D.

    '''
    def __init__(self, connections):
        self.connections = connections # dict of tuple (i, j), value doesn't matter.
        self.unique_nodes = []
        for i, j in self.connections:
            self.unique_nodes += [i]
            self.unique_nodes += [j]
        self.unique_nodes = sorted(list(set(self.unique_nodes)))
        self.num_cities = len(self.unique_nodes)

        self.memoized = {}
        self.parent_pointers = {}
    def reset(self):
        self.memoized = {}
        self.parent_pointers = {}
    def generate_bitmasks(self):
        '''
        Initializes a Bitmasks of not visited
        '''
        bitmask = 0
        for idx in range(self.num_cities):
            bitmask |= (1 << idx)
        return bitmask
    def mask(self, bitmask, city):
        ascii_shift = 97
        idx = ord(city) - ascii_shift
        # Masks/Unmasks a part of the bitmask
        bitmask ^= (1 << idx)
        return bitmask
    def is_masked(self, bitmask, city):
        ascii_shift = 97
        idx = ord(city) - ascii_shift
        masked = bitmask ^ (1 << idx)
        return masked > bitmask
    def dp(self, orig_city, cur_node, bitmask):

        # Mask the current city
        new_bitmask = self.mask(bitmask, cur_node)
        if new_bitmask == 0:
            return True if (cur_node, orig_city) in self.connections else False # Check if connection back to orig city exists.

        elif (cur_node, bitmask) in self.memoized:
            return self.memoized[(cur_node, bitmask)]
        else:
            is_possible = False
            city_needed = None
            for city in self.unique_nodes:
                if not self.is_masked(new_bitmask, city) and (cur_node, city) in self.connections:
                    outcome = self.dp(orig_city, city, new_bitmask)
                    if outcome:
                        is_possible = outcome
                        city_needed = city
        # memoize Results
        self.memoized[(cur_node, new_bitmask)] = is_possible
        self.parent_pointers[(cur_node, new_bitmask)] = city_needed
        return is_possible
    def solve(self):
        is_possible = False
        orig_city = None
        for city in self.unique_nodes:
            bitmask = self.generate_bitmasks()
            possible = self.dp(city, city, bitmask)
            if possible:
                is_possible = possible
                orig_city = city
        if not is_possible:
            return is_possible, None
        # Reconstruct Path
        bitmask = self.generate_bitmasks()
        bitmask = self.mask(bitmask, orig_city)
        cur_city = orig_city
        path = [cur_city]
        while True:
            next_city = self.parent_pointers[cur_city, bitmask]
            print(bin(bitmask))
            bitmask = self.mask(bitmask, next_city)
            path += [next_city]
            if bitmask == 0:
                path += [orig_city]
                return is_possible, path
            cur_city = next_city

class TSP:
    '''
    Solves the Travelling Salesman Problem using Bitmasking, reducing space and time needed(constants)
    '''
    def __init__(self, weights):
        self.weights = weights
        self.edges = {}
        self.unique_nodes = []
        for i, j in self.weights:
            self.unique_nodes += [i]
            self.unique_nodes += [j]
            self.edges[i, j] = self.weights[i, j]
            self.edges[j, i] = self.weights[i, j]
        self.unique_nodes = sorted(list(set(self.unique_nodes)))
        self.num_nodes = len(self.unique_nodes)


        for i in self.unique_nodes:
            for j in self.unique_nodes:
                if i == j:
                    continue
                if (i, j) not in self.edges:
                    self.edges[i, j] = float('inf')
                    self.edges[j, i] = float('inf')
        self.memoized = {}
        self.parent_pointers = {}
        self.final_nodes = {} # O(n) space, stores the index of the final node given some orig node.
    def reset(self):
        self.memoized = {}
        self.parent_pointers = {}
    def generate_bitmask(self):
        bitmask = 0
        for i in range(self.num_nodes):
            bitmask ^= (1 << i)
        return bitmask
    def mask(self, bitmask, city):
        ascii_shift = 97
        idx = ord(city) - ascii_shift

        bitmask ^= (1 << idx)
        return bitmask
    def is_masked(self, city, bitmask):
        ascii_shift = 97
        idx = ord(city) - ascii_shift
        masked = bitmask ^ (1 << idx)
        return masked < bitmask
    def dp(self, orig_city, cur_city, bitmask):
        if (cur_city, bitmask) in self.memoized:
            return self.memoized[(cur_city, bitmask)]
        else:
            bitmask = self.mask(bitmask, cur_city)
            if bitmask == 0:
                # All Cities visited
                return 0
            else:
                shortest = float('inf')
                city_to_visit = None
                # Try all remaining cities
                for city in self.unique_nodes:
                    if self.is_masked(city, bitmask):
                        # Visit this city
                        distance = self.dp(orig_city, city, bitmask) + self.edges[cur_city, city]
                        if city_to_visit is None:
                            city_to_visit = city
                            shortest = distance
                        elif distance < shortest:
                            shortest = distance
                            city_to_visit = city
        # Memoize
        self.memoized[(cur_city, bitmask)] = shortest
        self.parent_pointers[(cur_city, bitmask)] = city_to_visit
        return shortest
    def solve(self):
        shortest = float('inf')
        path = None
        # Try all Possible starting cities
        for city in self.unique_nodes:
            bitmask = self.generate_bitmask()
            distance = self.dp(city, city, bitmask)
            # reconstruct path to get final node
            cur_path = [city]
            bitmask = self.generate_bitmask()
            bitmask = self.mask(bitmask, city)

            cur_city = city
            while True:
                next_city = self.parent_pointers[(cur_city, bitmask)]
                bitmask = self.mask(bitmask, next_city)
                cur_path += [next_city]
                cur_city = next_city
                if bitmask == 0:
                    break
            cur_path += [city]
            distance += self.edges[cur_city, city]
            if path is None:
                path = cur_path
                shortest = distance
            elif shortest < distance:
                 distance = shortest
                 path = cur_path
        return shortest, path

import copy

class CapAssignmentProblem:
    '''
    Given n hat ids, how can we uniquely assign the hats to each person
    '''
    def __init__(self, hats, n_hats):
        self.hats = hats
        self.num_people = len(self.hats)
        self.n_hats = n_hats

        self.memoized = {}
        self.parent_pointers = {} # Store Tuple of Bitmasks
    def reset(self):
        self.memoized = {}
        self.parent_pointers = {}
    def turn_on(self, bitmask, idx):
        bitmask |= (1 << idx)
        return bitmask
    def turn_off(self, bitmask, idx):
        bitmask = self.turn_on(bitmask, idx)
        bitmask ^= (1 << idx)
        return bitmask
    def mask(self, bitmask, idx):
        bitmask ^= (1 << idx)
        return bitmask
    def is_masked(self, bitmask, idx):
        masked = bitmask ^ (1 << idx)
        return masked < bitmask
    def generate_bits_from_hats(self, hats):
        '''
        Creates a Bitmask from hats.
        '''
        bitmask = 0
        for idx in hats:
            bitmask = self.mask(bitmask, idx)
        return bitmask
    def num_hats(self, bitmask):
        count = 0
        for idx in range(self.n_hats):
            if self.is_masked(bitmask, idx):
                count += 1
        return count
    def dp(self, remaining_hats, cur_idx):
        # remaining_hats, list of bitmasks.
        tuple_remaining_hats = tuple(remaining_hats)
        if tuple_remaining_hats in self.memoized:
            return self.memoized[tuple_remaining_hats]
        else:
            if len(remaining_hats) == 1: # 1 Person Remaining
                combos = []
                hats = remaining_hats[0]
                for idx in range(self.n_hats):
                    if self.is_masked(hats, idx):
                        combos.append({cur_idx: idx})

                self.parent_pointers[tuple_remaining_hats] = combos
                self.memoized[tuple_remaining_hats] = self.num_hats(hats)
                return self.memoized[tuple_remaining_hats]
            else:
                # Try all Possible Assignments of remaining person
                person = remaining_hats[0] # bit mask of the first remaining person
                num_combinations = 0
                total_combinations = []
                for idx in range(self.n_hats):
                    if self.is_masked(person, idx):

                        # Assign this hat to person 1 and turn off the bitmask for every person
                        remaining_people = [self.turn_off(mask, idx) for mask in copy.deepcopy(remaining_hats[1:])]
                        num = self.dp(remaining_people, cur_idx + 1)

                        combos = copy.deepcopy(self.parent_pointers[tuple(remaining_people)])
                        for combo in combos:
                            combo[cur_idx] = idx

                        num_combinations += num
                        total_combinations += combos
                self.parent_pointers[tuple_remaining_hats] = total_combinations
                self.memoized[tuple_remaining_hats] = num_combinations
                return self.memoized[tuple_remaining_hats]

    def solve(self):
        list_of_bitmask = []
        for hat in self.hats:
            list_of_bitmask += [self.generate_bits_from_hats(hat)]

        num_of_combos = self.dp(list_of_bitmask, 0)
        tuple_bitmask = tuple(list_of_bitmask)
        all_combos = self.parent_pointers[tuple_bitmask]
        return num_of_combos, all_combos
def main():
    solver = CapAssignmentProblem([
        [5, 100, 1],
        [2],
        [5, 100]

    ], 101)
    num_combos, all_combos = solver.solve()
    print(num_combos)
    print(all_combos)
if __name__ == '__main__':
    main()