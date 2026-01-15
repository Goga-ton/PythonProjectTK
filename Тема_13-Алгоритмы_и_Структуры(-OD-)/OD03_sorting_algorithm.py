# Пузырьковая сортировка
mas = [5, 7, 4, 3, 8, 8, 2]
n = 7

for run in range(n-1):
    for i in range(n-1-run): # "run" тут используется что бы сократить количество проходов
        if mas[i] > mas[i+1]:
            mas[i], mas[i+1] = mas[i+1], mas[i]

print(f'Результат пузырьковой сортировки: \n {mas}')

# Быстрая сортировка

def quick_sort(s):
    if len(s) <= 1:
        return s

    element = s[0]
    left = list(filter(lambda i: i < element, s))
    center = [i for i in s if i==element]
    right = list(filter(lambda i: i > element, s))
    return quick_sort(left) + center + quick_sort(right)

print(f'\nРезультат быстрой сортировки: \n {quick_sort(mas)}')


# Сортировка выбором
print('\nСортировка выбором' )
a = [-3, 7, 0, 3, -2, 10, 2, 0,-5]

def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

selection_sort(a)
print(a)

# Сортировка выбором
print('\nСортировка вставками' )
def insert_sort(ar):
    for i in range(1, len(ar)):
        key = ar[i]
        j = i-1
        while j >= 0 and key < ar[j]:
            ar[j+1] = ar[j]
            j -= 1
        ar[j+1] = key

insert_sort(a)
print(a)