import matplotlib.pyplot as plt

# Линейная диограма

x = [2,6,8,14,18]
y = [6,4,10,12,9]
plt.plot(x,y)

plt.title('Пример простого линейного гарфика')
plt.xlabel('ось - х')
plt.ylabel('ось - у')
plt.show()

# Гистограмма

data = [5,6,7,4,6,5,7,8,5,8,9,10,11,8,9,10,7,6,5,7,8,9,10,7,6,5]
plt.hist(data, bins=3)

plt.title('Продолжительность сна')
plt.xlabel('часы сна')
plt.ylabel('кол-во людей')
plt.show()

# Диограмма рассеивания

x = [2,6,8,14,18]
y = [6,4,10,12,9]
plt.scatter(x,y)

plt.title('Пример простой диаграммы рассеивания')
plt.xlabel('ось - х')
plt.ylabel('ось - у')
plt.show()

# Работа с массивами

import numpy as np
import matplotlib.pyplot as plt

a = np.array([1,2,3,4])
print(a)

b = np.ones((3,3))
print(b)

c = np.random.randint(1,21,(4,5))
print(c)

d = np.arange(1, 10, 2)
print(d)

e = np.linspace(1, 30, 10).astype(int)
print(e)

x = np.linspace(-10, 10, 100).astype(int)
y = x**2

plt.plot(x, y)
plt.title('График функции у = х**2')
plt.xlabel('ось Х')
plt.ylabel('ось У')
plt.grid(True)
plt.show()

