# Stack (Стек)
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

stack = Stack()
print(f'Пустой список Stack: {stack.is_empty()}')
stack.push(1)
stack.push(2)
stack.push(3)
print(f'Пустой список Stack: {stack.is_empty()}')
print(f'Верхний элемент списка Stack: {stack.peek()}')

# Queue (Очередь)
class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

queue = Queue()
print(f'Пустая очередь - {queue.is_empty()}')
queue.enqueue('действие 1')
queue.enqueue('действие 2')
queue.enqueue('действие 3')
queue.enqueue('действие 4')
print(f'Пустая очередь - {queue.is_empty()}')
print(f'Количество элементов в очереди - {queue.size()}')
print(f'Удаление первого элемента очереди - {queue.dequeue()}')
print(f'Количество элементов в очереди - {queue.size()}')
from sqlalchemy.dialects.mysql import insert


# Tree (Дерево)
class Node():
    def __init__(self, koren):
        self.left = None
        self.right = None
        self.value = koren

def insert(root, key):
    if root is None:
        return Node(key)
    else:
        if root.value < key:
            root.right = insert(root.right, key)
        else:
            root.left = insert(root.left, key)

    return root

root = Node(70)
root = insert(root, 30)
root = insert(root, 56)
root = insert(root, 89)
root = insert(root, 45)
root = insert(root, 60)
root = insert(root, 73)
root = insert(root, 98)
root = insert(root, 84)

# Графы
class Graf:
    def __init__(self):
        self.graf = {}

    def add_edge(self, u, v):
        if u not in self.graf:
            self.graf[u] = []
        self.graf[u].append(v)


    def print_graf(self):
        for node in self.graf:
            print(node, "->", " -> ".join(map(str, self.graf[node])))

g = Graf()
g.add_edge(0, 1)
g.add_edge(0, 4)
g.add_edge(1, 2)
g.add_edge(1, 3)
g.add_edge(1, 4)
g.add_edge(2, 3)
g.add_edge(3, 4)


g.print_graf()














































