import random
import pdb

class Quicksort():
    def __init__(self):
        pass

    def quicksort(self, arr):
        '''
    This method sorts an array using the Quicksort Method
    '''
        if len(arr) <= 1:
            return arr
        else:
            pivot = self.select_pivot(arr)
            pivot_val = arr[pivot]
            
            arr, pivot = self.partition(arr, pivot, pivot_val)
            arr[0: pivot] = self.quicksort(arr[0:pivot])
            arr[pivot + 1: ] = self.quicksort(arr[pivot + 1:])
            return arr

    def partition(self, arr, pivot, pivot_value):
        '''
    Pivot is an Int and it represents the index of the pivot 
    Arr is the array to be partitioned around the pivot
    '''
        partition = 0
        boosted = False
        for i in range(len(arr)):
          if arr[i] < pivot_value:
            cur_val = arr[i]
            arr[i] = arr[partition]
            if i == pivot:
              pivot = partition
            elif pivot == partition:
              pivot = i
            arr[partition] = cur_val
            partition += 1
            if partition == len(arr): 
              break
            try:
              while arr[partition] == pivot_value:
                  partition += 1
                  boosted = True
                  if partition >= len(arr):
                      raise NotImplementedError
            
            except NotImplementedError:
              break
              
          
        next_pivot = 0
        # Insert Pivot
        
        if pivot > partition:
            cur_val = arr[pivot]
            arr[pivot] = arr[partition]
            arr[partition] = cur_val
            next_pivot = partition
        if pivot < partition:
            cur_val = arr[pivot]
            arr[pivot] = arr[partition - 1]
            arr[partition - 1] = cur_val
            next_pivot = partition - 1

        return arr, next_pivot
    def select_pivot(self, arr):
        return random.randint(0, len(arr) - 1)


'''
Sample Problem:
[||0, 4, 2, 5, P=1, 8]
[0||4, 2, 5, 1, 8]
[0|4|2,5,1,8]
[0|4,2|5,1,8]
[0|2,4,5|1,8]
[0|2,4,5,1|,8]
[0,|2,4,5,1,8]
[0,1|,4,5,2,8]

'''
quicksort = Quicksort()
val = [4, 2, 5, 1, 8, 7, 3, 6]
quicksort.quicksort(val)
#quicksort.partition(val, 5, 7)
print(val)
