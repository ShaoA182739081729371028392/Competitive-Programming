class SimpleRollingHash:
  def __init__(self, num_buckets, base = 26):
    self.base = 26
    self.num_buckets = num_buckets
    self.curSum =0
    self.cur_len = 0
  def reset(self):
    self.curSum = 0
    self.cur_len = 0
  def hash(self):
    '''
    Super Simple Hashing function, mod p
    '''
    return self.curSum % self.num_buckets
  def append(self, new):
    '''
    Appends a number into the sum, slow if base and numbers are large.
    '''
    self.curSum *= self.base
    self.curSum += new
    self.cur_len += 1
  def skip(self, old):
    '''
    Skips a number from the sum.
    '''
    self.curSum -= old * self.base ** (self.cur_len - 1)
    self.cur_len -= 1


class RollingHash:
  '''
  Implements a more efficient RollingHash with internal states, so numbers are smaller and operations are faster.
  '''
  def __init__(self, num_buckets, base = 26):
    self.num_buckets = num_buckets
    self.base = base
    # Precompute the Inverse of Base
    self.ibase = self.modular_inverse(self.base)[-1]
    self.curModSum = 0 # Internal State to keep the numbers small
    self.magic = 1 # base^(k), Internal State
  def reset(self):
    '''
    Resets this instances internal states
    '''
    self.curModSum = 0
    self.magic = 1
  def euclidean_algorithm(self, a, b):
    '''
    Recursively computes the GCD between two numbers
    '''
    # Compute Larger of two numbers
    larger = max(a, b)
    smaller = min(a, b)
    if a * b == 0 and (a != 0 or b != 0):
      if a:
        return a
      return b
    else:
      return self.euclidean_algorithm(smaller, larger % smaller)
  def extended_euclidean_algorithm(self, a, b):
    '''
    A > B
    Recursively Computes the extended euclidean algorithm
    returns tuple(gcd, a_prime, b_prim)
    '''
    assert a > b
    if b == 0:
      return (1, 1, 0) # (gca has to be 1, thus a = 1, b = 0)
    gca, a_prime, b_prime = self.extended_euclidean_algorithm(b, a % b)
    new_a = b_prime
    new_b = a_prime - (a // b) * new_a
    return (gca, new_a, new_b)

  def modular_inverse(self, a):
    m = self.num_buckets
    smaller = min(a, m)
    larger = max(a, m)

    (gca, x, y) = self.extended_euclidean_algorithm(larger, smaller)

    if smaller == a:
      return (gca, y + m)
    return (gca, x + m)
  def hash(self):
    '''
    Returns the Current Hashed Values
    '''
    return self.curModSum % self.num_buckets # Simple, since all hard work is done in append and skip.
  def append(self, new):
    self.curModSum = ((self.curModSum * self.base) + new) % self.num_buckets
    # Update magic to have one extra length
    self.magic = (self.magic * self.base) % self.num_buckets
  def skip(self, old):
    self.magic = (self.magic * self.ibase) % self.num_buckets
    self.curModSum = (self.curModSum - old * self.magic)
    
class KarpRabin:
  '''
  Implements Karp Rabin Rolling Hash
  '''
  def __init__(self, key, corpus):
    self.key = key
    self.corpus = corpus
    self.window_size = len(self.key)
    self.FastRollingHash = RollingHash(23)
  def collision_check(self, key, substring):
    return key == substring
  def reset(self):
    '''
    Designated Reset Function
    '''
    self.FastRollingHash.reset();
  def append(self, val):
    '''
    Designated Append Function
    '''
    self.FastRollingHash.append(val)
  def skip(self, val):
    '''
    Designed Skip Function
    '''
    self.FastRollingHash.skip(val)
  def hash(self):
    '''
    Designated Hashing Function.
    '''
    hash_complex = self.FastRollingHash.hash()
    return hash_complex
  def karp_rabin(self):
    '''
    Computes where identical substrings exist in O(n + m) time.
    '''
    identical_substring_positions = []
    # Hash Initial Key
    key_hash = self.hash_initial(self.key)
    cur_key = self.hash_initial(self.corpus[:self.window_size])
    if cur_key == key_hash:
      if self.collision_check(self.key, self.corpus[:self.window_size]):
        identical_substring_positions += [(0, self.window_size)]

    for i in range(0, len(self.corpus) - self.window_size):
      old = self.corpus[i]
      new = self.corpus[i + self.window_size]
      self.skip(ord(old))
      self.append(ord(new))
      hashed = self.hash()
      if hashed == key_hash:
        if self.collision_check(self.key, self.corpus[i + 1: self.window_size + 1 + i]):
          identical_substring_positions += [(i + 1, self.window_size + 1 + i)]
    return identical_substring_positions
  def decode_hashed(self, indices):
      '''
      Decodes the hashed values
      indices: list of (start, end) pairs
      '''
      values_decoded = []
      for start, end in indices:
          values_decoded += [self.corpus[start: end]]
      return values_decoded
  def hash_initial(self, key):
    self.reset();
    for i in key:
      self.append(ord(i))
    return self.hash()
karpRabin = KarpRabin("AAT", "AATAGATSGAATAAT")
print(karpRabin.karp_rabin())