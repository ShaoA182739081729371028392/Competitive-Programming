class KnapSack:
  def valid_items(self, items):
    for i in items:
        assert i > 0
  def __init__(self, items, max_weight):
    self.items = items # Stored as a tuple (weight, value)
    self.valid_items(self.items)
    self.num_items = len(self.items)
    self.max_weight = max_weight
    self.memoized = {}
    self.states = {}
  def reset(self):
    self.memoized = {}
    self.states = {}
  def dp(self, i, j):
    '''
    I: Item Number(>= i)
    j: Weight remaining(<= j)
    '''
    if j < 0:
      # Overflowed weight
      return float('-inf')

    if (i, j) in self.memoized:
      return self.memoized[i, j]
    if i >= self.num_items:
      return 0 # End of list
    take = self.items[i][1] + self.dp(i + 1, j - self.items[i][0])
    no_take = self.dp(i + 1, j)
    self.memoized[i, j] = max(take, no_take)
    if take > no_take:
      self.states[i] = 1
      return take
    self.states[i] = 0
    return no_take
  def maximize_value(self):
    return self.dp(0, self.max_weight)

class SubsetSumKnapsack():
    '''
    Solves the problem of a Subset sum.
    '''
    def valid_items(self, items):
        for i in items:
            assert i > 0
    def __init__(self, items, exact_weight):
        self.items = items # Format simply a list of weights.
        self.valid_items(self.items)
        self.num_items = len(self.items)
        self.exact_weight = exact_weight
        self.memoized = {}
    def reset(self):
        self.memoized = {}
    def _and(self, a, b):
        return a * b
    def _not(self, a):
        return 1 - a
    def _or(self, a, b):
        return max(a, b)
    def dp(self, i, j):
        '''
        i: item number
        j: Exact Weight to match
        '''
        if j < 0:
            self.memoized[i, j] = 0
            return 0
        if (i, j) in self.memoized:
            return self.memoized[i, j]
        result = None
        ans = None
        if i == self.num_items - 1:
            if self.items[i] == j:
                result = 1
                ans = 1
            else:
                result = 0
                ans = 0
        else:
            if self.items[i] == j:
                # Can Early Exit
                ans = 1
                result = 1
            else:
                take_result = self.dp(i + 1, j - self.items[i])
                no_take = self.dp(i + 1, j)
                ans = self._or(take_result, no_take)
                result = take_result
        self.memoized[(i, j)] = result
        return ans

    def solve(self):
        '''
        returns 1 if there exists a combination of items that sum exactly to weight, else 0.
        '''
        return self.dp(0, self.exact_weight)
class KSum():
    '''
    Solves the KSum Knapsack problem
    Can you select exactly K items that will give exactly n weight
    '''
    def valid_items(self, items):
        for i in items:
            assert i > 0
    def __init__(self, items, k, exact_weight):
        self.items = items
        self.valid_items(self.items)
        self.num_items = len(self.items)
        self.k = k
        self.exact_weight = exact_weight

        self.memoized = {}
    def reset(self):
        self.memoized = {}
    # basic Boolean logic functions
    def _and(self, a, b):
        return a * b
    def _or(self, a, b):
        return max(a, b)
    def _not(self, a):
        return 1 - a
    def dp(self, i, j, k):
        '''
        i: Item Idx
        j: remaining weight
        k: num items still left to take.
        '''
        if (i, j, k) in self.memoized:
          return self.memoized[i, j, k]
        if j < 0 or k < 0:
            result = 0
        elif j== 0 and k == 0:
            result = 1
        elif i == self.num_items - 1:
            if j == self.items[i] and k == 1:
                result = 1
            else:
                result = 0
        else:
            take_result = self.dp(i + 1, j - self.items[i], k - 1)
            no_take = self.dp(i + 1, j, k)
            result = self._or(take_result, no_take)
        self.memoized[i, j, k] = result
        return result
    def solve(self):
        return self.dp(0, self.exact_weight, self.k)
class MultiSetKSum():
    '''
    Instead of 1 bar per slot, there are infinite copies of each bar.
    '''
    def valid_items(self, items):
        for i in items:
            assert i > 0
    def __init__(self, items, k, exact_weight):
        self.items = items
        self.valid_items(self.items)
        self.num_items = len(self.items)
        self.k = k
        self.exact_weight = exact_weight
        self.memoized = {}
    def reset(self):
        self.memoized = {}
    # Boolean Logic
    def _and(self, a, b):
        return a * b
    def _or(self, a, b):
        return max(a, b)
    def _not(self, a):
        return 1 - a
    def dp(self, i, j, k):
        '''
        i: item idx
        j: remaining_weight
        k: bars left to take.
        '''
        if (i, j, k) in self.memoized:
          return self.memoized[i, j, k]
        if j == 0 and k == 0:
            # Solved in prev recursive call
            result = 1
        elif j < 0 or k < 0:
            # Too much already
            result = 0
        elif i == self.num_items - 1:
            if j % self.items[i] == 0 and j // self.items[i] == k:
                result = 1
            else:
                result = 0
        else:
            # Try all take combinations
            result = 0
            for num_take in range(j // self.items[i] + 1):
                result = self._or(result, self.dp(i + 1, j - num_take * self.items[i], k - num_take))
        self.memoized[i, j, k] = result
        return result

    def solve(self):
        return self.dp(0, self.exact_weight, self.k)
def main():
    ksum = MultiSetKSum((2, 3, 5), 3, 6)
    print(ksum.solve())
if __name__ == '__main__':
    main()
