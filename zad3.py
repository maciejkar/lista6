

class Binary_Heap():
    """Binary_Heap with limits of elements """
    def __init__(self, limit = 10):
        self.heap = [None]
        self.current_size = 0
        self.size_limit = limit

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
            if self.size_limit <= self.current_size:
                if item > self.heap[1]:
                    self.heap[1] = item
                    self.item_down(1)
            else:
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

if __name__ == "__main__":
    heap = Binary_Heap()
    heap.append([1,2,3,4,5,6,7,8,9,10,11])
    print(heap)
    heap.append(1)
    print(heap)
    heap.append(65)
    print(heap)