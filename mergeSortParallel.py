import random
import numpy
from mpi4py import MPI

def criarVetor(size):
    return [random.randint(0, 20000) for i in range(size)]

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

def merge_all(arrays):
    result = []
    for array in arrays:
        result = merge(result, array)
    return result

def main():
    #o melhor desempenho do algoritmo foi com 6 processos

    ARRAY_SIZE = 10000000
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    inicio = MPI.Wtime()

    if rank == 0:
        array = criarVetor(ARRAY_SIZE)
        sliceSize = ARRAY_SIZE // size
        data = [(sliceSize * i, sliceSize * (i+1)) for i in range(size)]
    else:
        data = None
        array = None

    array = comm.bcast(array, root=0)
    data = comm.scatter(data, root=0)

    slicedArray = array[data[0]:data[1]]

    slicedArray = mergeSort(slicedArray)

    sortedArrays = comm.gather(slicedArray, root=0)

    if rank == 0:
        sortedArray = merge_all(sortedArrays)
        fim = MPI.Wtime()
        print(f"Time taken to sort: {(fim - inicio):.4f} s")

if __name__ == "__main__":
    main()