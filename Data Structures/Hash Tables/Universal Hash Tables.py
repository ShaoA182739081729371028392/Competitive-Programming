# Implements Dot Product Universal Hashing using Chaining
import pudb
import math
import random 
class Sieve():
  '''
  Computes all primes up to 101(max items is thus 10101) using the sieve method
  '''
  def __init__(self, max_nums):
    self.max_nums = max_nums
    self.is_prime = self.sieve()
  def sieve(self):
    '''
    Uses the Sieve method to quickly compute primes up to max nums.
    '''
    is_prime_mat = [None] * self.max_nums 
    is_prime_mat[0] = False
    is_prime_mat[1] = False
    for i in range(self.max_nums):
      if is_prime_mat[i] == None:
        is_prime_mat[i] = True
        for j in range(2, self.max_nums // i):
          is_prime_mat[j * i] = False
    return is_prime_mat
class LLNode():
  '''
  Linked List Node, Augmented with Original Key.
  '''
  def __init__(self):
    self.value = None
    self.key = None
    self.next = None
class LinkedList():
  '''
  Creates a linked list object, where items will be inserted using chaining if needed. 
  '''
  def __init__(self):
    self.head = None
  def __len__(self):
    '''
    Computes the length of the linked list.
    '''
    length = 0
    cur_node = self.head
    while cur_node:
      length += 1
      cur_node = cur_node.next
    return length
  def print_all(self):
    '''
    Runs through the linked list, printing all values
    '''
    cur_node = self.head 
    while cur_node:
      print(f'Key: {cur_node.key}, Value: {cur_node.value}')
      cur_node = cur_node.next
  def replace(self, key, value):
    '''
    Finds a Node with the same key, and replaces the value there.
    '''
    assert self.search(key), "Node must exist"
    cur_node = self.head
    while cur_node:
      if cur_node.key == key:
        cur_node.value = value
        return 
      cur_node = cur_node.next    
  def insert(self, key, value):
    '''
    Inserts a Key value pair into the linked list
    '''
    new_node = LLNode()
    new_node.key = key
    new_node.value = value
    if not self.head:
      self.head = new_node
      return 
    new_node.next = self.head
    self.head = new_node
  def delete(self, key):
    '''
    Deletes a node from the linked list

    Searches for the key, and then deletes the node
    '''
    assert self.search(key), "The node doesnt exist."
    cur_node = self.head
    if cur_node.key == key:
      self.head = cur_node.next
      return
    cur_node =self.head.next
    prev_node = self.head 
    while cur_node:
      if cur_node.key == key:
        # Delete the node
        prev_node.next = cur_node.next
        del prev_node
        return
      prev_node = cur_node
      cur_node = cur_node.next
  def retrieve(self, key):
    '''
    Retrieves the value of a linked list.
    '''
    assert self.search(key), "The Key must exist."
    cur_node = self.head
    while cur_node:
      if cur_node.key == key:
        return cur_node.value
      cur_node = cur_node.next
  def search(self, key):
    '''
    Searches for a key value pair by key.
    '''
    if not self.head:
      return False
    cur_node = self.head
    while cur_node:
      if cur_node.key == key:
        return True
      cur_node = cur_node.next
    return False 
  def in_order_traverse(self):
    '''
    Traverses through the Linked List.
    '''
    key_value_lists = []
    cur_node = self.head
    while cur_node:
      key_value_lists += [(cur_node.key, cur_node.value)]
      cur_node = cur_node.next
    return key_value_lists 
class HashMap():
  '''
  Simplified Hash Map with Universal Hashing.
  
  For simplicity, this hash map can only hash integers.

  We will find the prime needed using the sieve method, and then we just use m ^ 2 buckets.

  Parameters Needed: n, the universe size
  '''
  def __init__(self, max_items):
    self.max_items = max_items
    self.min_buckets = math.ceil(math.sqrt(self.max_items))
    self.sieve = Sieve(self.max_items + 1)
    # Find the minimum number of buckets needed 
    self.buckets = 0
    for i in range(self.min_buckets, self.max_items + 1):
      if self.sieve.is_prime[i]:
        self.buckets = i
        break
    # Create Initial Hash Map
    self.HashMap = [LinkedList() for i in range(self.buckets)]
    # Create Random Hash Functions:
    self.HashFNS = [random.randint(0, self.max_items - 1) for i in range(self.max_items)]

  def _base_m(self, i):
    '''
    Writes a integer in terms of base m(Vector of length 2 - since we set the buckets to be m^2 or lower)
    '''
    second_digit = i // self.buckets
    first_digit = i % self.buckets
    return [second_digit, first_digit]
  def dot_product(self, a, b):
    '''
    Computes the dot product between two vectors
    '''
    assert len(a) == len(b)
    sum = 0
    for i in range(len(a)):
      sum += a[i] * b[i]
    return sum
  def hash_function(self, i):
    '''
    Maps a Key to a hash table using universal hashing.

    i: must be an integer and 0<=i<self.max_items
    '''
    assert type(i) == type(0), "Must be an integer being hashed"
    assert i > -1 and i< self.max_items, "Not in range"
    # Break up the integer into vectors
    base_m_i = self._base_m(i)
    # Grab Predefined Random Hash function
    random_hash = self.HashFNS[i]
    base_m_random = self._base_m(random_hash)

    # Dot Product
    dot_prod = self.dot_product(base_m_i, base_m_random) % self.buckets
    # This dot product hashing is universal.
    return dot_prod 
  def insert(self, key, value):
    '''
    Inserts a value into the hash map, using a key.
    
    The key must be an integer, not the value.
    '''
    hashed_key = self.hash_function(key) # Grabs the key
    if self.search(key):
      # Replace the value in linked list
      self.HashMap[hashed_key].replace(key, value);
    else:
      self.HashMap[hashed_key].insert(key, value) # Insert the Key into the appropriate linked list
  def search(self, key):
    '''
    Searches if a key exists in the hash function.
    '''
    hashed_key = self.hash_function(key)
    return self.HashMap[hashed_key].search(key)
  def delete(self, key):
    '''
    Deletes a key from the hash table
    '''
    hashed_key = self.hash_function(key)
    assert self.HashMap[hashed_key].search(key), "The key doesnt exist"
    self.HashMap[hashed_key].delete(key)
  def lookup(self, key):
    '''
    Retrieves the hashed value of a key
    '''
    hashed_key = self.hash_function(key)
    return self.HashMap[hashed_key].retrieve(key)
  def print_lengths(self):
    '''
    Checks how balanced the hash table is, by checking the length of each one.
    '''
    for i in range(self.buckets):
      print(f"bucket: {i}, bucket_length: {len(self.HashMap[i])}")
  def print_buckets(self):
    ''' 
    Performs an in_order Traversal, printing the linked lists from each bucket.
    '''
    for i in range(self.buckets):
      print(f"Linked List {i}: {self.HashMap[i].in_order_traverse()}")
length_hash = 101
hashMap = HashMap(101)
for i in range(101):
  hashMap.insert(i, i + 1)