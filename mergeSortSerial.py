import time
import random
from mpi4py import MPI

def merge(left, right):
    result = []
    i, j = 0, 0
    while (i < len(left) and j < len(right)):
        if (left[i] <= right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j+=1
    result += left[i:]
    result += right[j:]
    return result

def mergeSort(arr):
    if (len(arr) <= 1):
        return arr
    middle = len(arr) // 2
    left = mergeSort(arr[:middle])
    right = mergeSort(arr[middle:])
    return merge(left, right)

random_array = [random.randint(0, 1000) for i in range(10000000)]

start_time = MPI.Wtime()

random_array = mergeSort(random_array)

end_time = MPI.Wtime()

print(f"Time taken to sort: {(end_time - start_time):.4f} s")
