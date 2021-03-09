# Import Libraries
import math
import random
class Sieve():
  '''
  With the Sieve method, computes all necessary primes
  '''
  def __init__(self, max_nums):
    self.max_nums = max_nums
    self.is_prime = self.sieve()
  def sieve(self):
    is_prime = [None] * self.max_nums
    is_prime[0] = False
    is_prime[1] = False
    for i in range(2, self.max_nums):
      if is_prime[i] == None:
        is_prime[i] = True
        for j in range(2, self.max_nums // i):
          is_prime[i * j] = False
    return is_prime

class KVNode():
  '''
  Stores a Key-Value Node
  '''
  def __init__(self, key, value):
    self.key = key
    self.value = value
class FirstPartPerfectHash():
  def __init__(self, key_value_pairs, num_keys, universe_size):
    self.key_value_pairs = key_value_pairs
    self.universe_size = universe_size
    self.num_keys = num_keys
    self.num_buckets = self.num_keys ** 2

    while True:
      self.HashKeys = self.generate_random()
      bucket_keys = [None for i in range(self.num_buckets)]
      bucket_num = [0] * self.num_buckets

      # Hash All Key Value Pairs into Buckets
      for node_idx in range(len(self.key_value_pairs)):
        KVpair = self.key_value_pairs[node_idx]
        h_key = self.hash_function(KVpair.key)
        bucket_keys[h_key] = KVNode(KVpair.key, KVpair.value)
        bucket_num[h_key] += 1
      if not self.valid_bucketize(bucket_num):
        continue
      self.buckets = bucket_keys
      break
  def print_buckets(self):
    print("-----------------------------")
    for bucket_idx in range(len(self.buckets)):
      print(self.buckets)
      if self.buckets[bucket_idx] != None:
        print(f"bucket: {bucket_idx} Key: {self.buckets[bucket_idx].key}, value: {self.buckets[bucket_idx].value}")
      else:
        print(f"bucket {bucket_idx} empty")
  def retrieve(self, key):
    assert self.search(key)
    h_key = self.hash_function(key)
    return self.buckets[h_key]
  def search(self, key):
    '''
    Searches if a key exists
    '''
    h_key = self.hash_function(key)
    if self.buckets[h_key] != None:
      return True
    return False
  def valid_bucketize(self, bucket_num):
    for num in bucket_num:
      if num > 1:
        return False
    return True
  def _base_m(self, i):
    second_digit = i // self.num_buckets
    first_digit = i % self.num_buckets
    return [second_digit, first_digit]
  def hash_function(self, key):
    '''
    Universally Hashes a key
    '''
    base_m_key = self._base_m(key)
    base_m_a = self._base_m(self.HashKeys[key])
    hash_key = self.dot_product(base_m_key, base_m_a) % self.num_buckets
    return hash_key

  def dot_product(self, a, b):
    '''
    Dot Product between a and b
    '''
    assert len(a) == len(b)
    sum = 0
    for idx in range(len(a)):
      sum += a[idx] * b[idx]
    return sum
  def generate_random(self):
    '''
    Generates Random Keys
    '''
    keys = [random.randint(0, self.num_buckets - 1) for i in range(self.universe_size)]
    return keys


class PerfectHashMap():
  '''
  This class implements a perfect hash map, which is static, but guarentees (1/M) probability hashing for search.

  This is a guarenteed O(1) lookup and O(n) space.

  Strategy to generate a perfect HashMap:
  Hash Map needs to be modified to contain not a linked list, but just an array now(Perfect Hashing)
  - Two Table Hash Map with M buckets(M^2 > N)

  '''
  def __init__(self, key_value_pairs):
    '''
    Constructs a Perfect Hash Map

    key_value_pairs: [KVnode, ...]
    How the key_value_pairs are structured.
    '''
    self.max_items = len(key_value_pairs)
    self.constant = 10 # Probabilistically, by setting this constant to 2, the perfect hash creation is a coin flip if it works(and it's linear space)
    self.key_value_pairs = key_value_pairs
    # Linear S
    self.sieve = Sieve(self.max_items)
    self.min_buckets = math.ceil(math.sqrt(self.max_items))
    self.num_buckets = 0
    for i in range(self.min_buckets, self.max_items):
      # Check if prime.
      if self.sieve.is_prime[i]:
        self.num_buckets = i
        break
    del self.min_buckets # We have no need for this variable anymore.
    # Hash the values first.
    while True:
      # Note for Debugging: Cannot break out of this loop
      self.hash_keys = self.generate_random()
      hashed_nodes = [[] for i in range(self.num_buckets)]
      hashed_keys = [0] * self.num_buckets

      for node_idx in range(len(key_value_pairs)):
        node = key_value_pairs[node_idx]
        h_key = self.hash_function(node.key)
        hashed_nodes[h_key] += [KVNode(node.key, node.value)]
        hashed_keys[h_key] += 1
      if self.valid_stage_1(hashed_keys):
        break
    # Create Stage 1 Hash Table
    self.Stage1HashTable = [FirstPartPerfectHash(hashed_nodes[i], hashed_keys[i], self.max_items) if hashed_keys[i] > 0 else None for i in range(self.num_buckets)]


  def print_buckets(self):
    '''
    Performs an in order traversal of the buckets, printing them each.
    '''
    for bucket in self.Stage1HashTable:
      bucket.print_buckets();

  def valid_stage_1(self, hashed_keys):
    '''
    hashed_keys: Represents how many nodes are hashed to this bucket
    '''
    sum = 0
    for hashed_key in hashed_keys:
      sum += hashed_key ** 2
    return sum < self.constant * self.max_items
  def dot_product(self, a, b):
    '''
    Computes dot product between two vectors A and B
    '''
    assert len(a) == len(b)
    sum = 0
    for idx in range(len(a)):
      sum += a[idx] * b[idx]
    return sum
  def _base_m(self, i):
    '''
    Break integer into base m
    Super easy since M^2 > N
    '''
    second_digit = i // self.num_buckets
    first_digit = i % self.num_buckets
    return [second_digit, first_digit]
  def generate_random(self):
    '''
    Generates Random Keys
    '''
    keys = [random.randint(0, self.max_items-1) for i in range(self.max_items)]
    return keys
  def hash_function(self, key):
    '''
    Uses a Universal Hash Function to hash initial keys into buckets.

    input: Integer(Key), output: Hashed Key
    '''
    # Split the Key into Vector
    base_m_key = self._base_m(key)
    base_m_random = self._base_m(self.hash_keys[key])

    # Take the Dot Product
    dot_prod = self.dot_product(base_m_key, base_m_random) % self.num_buckets
    # return Hash Functions
    return dot_prod

  def search(self, key):
    '''
    Searches for a key in the perfect hash map.
    '''
    # First Find the first bucket
    h_key = self.hash_function(key)
    if self.Stage1HashTable[h_key]:
      return self.Stage1HashTable[h_key].search(key)
    return False
  def retrieve(self, key):
    '''
    Retrieves the value in the perfect hash map.
    '''
    assert self.search(key)
    h_key = self.hash_function(key)
    if self.Stage1HashTable[h_key]:
      return self.Stage1HashTable[h_key].retrieve(key)
KVPairs = [KVNode(i, i + 1) for i in range(101)]

hashMap = PerfectHashMap(KVPairs)
hashMap.print_buckets()
print(f"key: {hashMap.retrieve(0).key},value: {hashMap.retrieve(0).value}")