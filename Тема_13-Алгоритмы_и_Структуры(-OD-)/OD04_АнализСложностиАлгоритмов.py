# O(1) - константа (врменная) сложности алгоритма
def get_elements(arr, index):
    return arr[index]

arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print('O(1) - константа сложности алгоритма:')
print(get_elements(arr, 4))

# O(n) - линейная сложности алгоритма
def line_search(arr, terget):
    for i in range(len(arr)):
        if arr[i] == terget:
            return i
    return 'Число не найдено'
print('\nO(n) - константа сложности алгоритма:')
print(line_search(arr, 9))
print(line_search(arr, 15))

# O(log n) - логаарифмическая (бинарная) сложности алгоритма
# в данном способе мы работаем с отсортированным массивом
print('\nO(log n) - логаарифмическая сложности алгоритма:')

def binary_search(arr, terget):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == terget:
            return mid
        elif arr[mid] < terget:
            low = mid + 1
        else:
            high = mid - 1
    return f'Указанное значение {terget} в диапозоне не найдено'
print(f'Индекс указанно числа = {binary_search(arr, 7)}')
print(binary_search(arr, 25))