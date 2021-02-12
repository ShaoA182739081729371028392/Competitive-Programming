import copy
import math
import random
import pdb
class RSelect():
  def merge_sort(self, x):
    '''
    Merge Sort
    '''
    if len(x) == 1:
      return x
    else:
      left = self.merge_sort(x[0: int(len(x) / 2)])
      right = self.merge_sort(x[int(len(x)/2): ])
      vals = []
      i = 0
      j = 0
      while i < len(left) and j < len(right):
        if left[i] <= right[j]:
          vals += [left[i]]
          i += 1
        else:
          vals += [right[j]]
          j += 1
      if len(left) == i:
        vals += right[j: ]
      else:
        vals += left[i: ]
      return vals

  def __init__(self):
    pass
  def partition(self, arr, pivot, pivot_val):
    partition = 0
   
    for i in range(len(arr)):
      if arr[i] < pivot_val:
        cur_val = arr[i]
        arr[i] = arr[partition]
        arr[partition] = cur_val
        if pivot == i:
          pivot = partition
        elif pivot == partition:
          pivot = i
        partition += 1
      
    
    if pivot > partition:
      cur_val = arr[pivot]
      arr[pivot] = arr[partition]
      arr[partition] = cur_val
      
      return arr, partition
    elif pivot < partition:
      cur_val = arr[pivot]
      arr[pivot] = arr[partition-1]
      arr[partition-1] = cur_val
      
      return arr, partition - 1
    else:
      
      return arr, pivot
  def select_pivot(self, arr):
    '''
    Deterministically Calculates the "median of medians"
    '''
    length = len(arr)
    medians = []
    if len(arr) == 1:
      return arr
    for i in range(0, length, 5):
      if i + 5 > length:
        val = self.merge_sort(arr[i: ])
        if len(val) % 2 == 0:
          medians += [val[int(len(val) / 2)-1]]
        else:
          medians += [val[int(len(val) / 2)]]
      else:
        val = self.merge_sort(arr[i: i + 5])
        medians += [val[2]]
    return self.select_pivot(medians)
  def select(self, arr, index_to_find):
    '''
    This method selects the i smallest value in a randomized array
    '''
    if len(arr) == 1:
      return arr[0]
    else:
      #pivot = random.randint(0, len(arr) - 1)
      pivot = None
      pivot_val = self.select_pivot(arr)[0]
      for i in range(len(arr)): # This is still o(N)!
        if pivot_val == arr[i]:
          pivot = i
          break

      pivot_value = arr[pivot]
      arr, pivot = self.partition(arr, pivot, pivot_value)
    
      if index_to_find == pivot:
        return arr[pivot]
      if index_to_find > pivot:
        return self.select(arr[pivot + 1:], index_to_find - len(arr[:pivot + 1]))
      else:
        return self.select(arr[:pivot], index_to_find)
rselect = RSelect()
print(rselect.select([10, 2, 14, 291, 293, 12, 3, 4], 4))

'''
Practice Partition:
[3, 4, 2, 1, 6, p=5, 7, 8]
[3,4,2,1||6,5,7,8]
[3,4,2,1|6|,5,7,8] Pindex = 4, i = 5
[3,4,2,1|6,5|7,8] Pindex = 4, i = 6
[3,4,_,1,5|6,7,2], Pindex = 5, i = 6
[3,4,2,1,5|6,7|,2] Pindex = 5, i = 7
[3,4,2,1,5|6,7,2]
[3,4,2,1,5,2|7,6]
True Vals:
[3,4,2,1,5,6,7,8]
'''