import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time
class Binary_Heap():
    def __init__(self):
        self.heap = [None]
        self.current_size = 0

    def item_up(self, n):
        """Method move element up"""
        while n // 2 > 0 :
            if self.heap[n] < self.heap[n //2]:
                self.heap[n // 2 ], self.heap[n] = self.heap[n] , self.heap[n // 2]
            n //= 2

    def append(self, items):
        """Method add new items to the heap """
        if type(items) == int or type(items) == float or type(items) == str:
            items = [items]
        for item in items:
            self.heap.append(item)
            self.current_size += 1
            self.item_up(self.current_size)

    def find_min(self):
        """Method return min from heap """
        return self.heap[1]

    def item_down(self, k):
        """Method move element down"""
        while ( k * 2) <= self.current_size:
            min_element = self.min_child(k)
            if self.heap[k] > self.heap[min_element]:
                self.heap[k], self.heap[min_element] =self.heap[min_element], self.heap[k] 
            k = min_element

    def min_child(self, k):
        """Method return min child of the heap"""
        if k *2 + 1 > self.current_size:
            return k * 2 
        else:
            if self.heap[k*2] < self.heap[k*2 +1]:
                return k * 2
            else:
                return k * 2 + 1

    def dealate_min(self):
        """Method delate min"""
        element = self.heap[1]
        self.heap[1] = self.heap[self.current_size]
        self.current_size -= 1
        self.heap.pop()
        self.item_down(1)
        return element

    def __str__(self):
        return str(self.heap[1:])

if __name__ == '__main__':
    heap = Binary_Heap()
    heap.append([3,2,1,6,3,5,7,10 , 11])
    print(heap)
    print(heap.dealate_min())
    print(heap)

    def time_of_sort(number_of_items, reps = 50):
        sorted_items = []
        times = []
        
        for _ in range(reps):
            heap = Binary_Heap()
            items = np.random.randint(0,10000, size=number_of_items)
            start = time.time()
            heap.append(items)
            for _ in range(number_of_items ):
                sorted_items.append(heap.dealate_min())
            end = time.time()
            times.append(end-start)
        return np.mean(times)

    def function(n , a,b ):
        return a*n*np.log2(b*n) 

    
    count_of_variables = np.linspace(3,503,500,dtype=np.int32)
    times_of_solves = np.array([time_of_sort(x) for x in count_of_variables ])
    popt, _ = curve_fit(function,count_of_variables, times_of_solves )
    plt.plot(count_of_variables, times_of_solves)
    plt.plot(count_of_variables, popt[0] * count_of_variables * np.log2(popt[1] * count_of_variables) )
    plt.show()
    print(popt)