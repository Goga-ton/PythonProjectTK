# Пример 1
import pandas as pd
data = {
    'набор А':[85, 90, 95, 100, 105],
    'набор Б':[70, 80, 95, 110, 120],
}

df = pd.DataFrame(data)
stdA = df['набор А'].std()
stdB = df['набор Б'].std()

print(f'stdA: {stdA}\nstdB: {stdB}')


# Пример 2
print()
data1 = {
    'Возраст':[20, 23, 25, 27, 29, 35, 25, 22, 36, 28],
    'Зарплата':[54000, 56000, 58000, 54850, 51000, 60000, 58000, 52000, 57000, 62000],
}

df1 = pd.DataFrame(data1)
print(f'Средний возраст - {df1["Возраст"].mean()}')
print(f'Медианный возраст - {df1["Возраст"].median()}')
print(f'Стандартное отклонение возраста - {df1["Возраст"].std()}')
print(f'Средняя зарплата - {df1["Зарплата"].mean()}')
print(f'Медианная зарплата - {df1["Зарплата"].median()}')
print(f'Стандартоное отклонение зарплаты - {df1["Зарплата"].std()}')


# Пример 3 (Временные ряды)
import pandas as pd
import numpy as np

dates = pd.date_range(start='2022-07-26', periods=10, freq='D')

values = np.random.randint(-10, 11, 10) # "-10" и "11" это давпозон от "-10" до "10", "11" не входит и затем "10" это количество случайных чисел в данном диапозоне

df = pd.DataFrame({'date': dates, 'value': values})
df.set_index('date', inplace=True) # индексируем что бы програма поняла что это даты и смогла выполнить группировку по месяцам для поиска среднего, строка ниже

month = df.resample('ME').mean() # ищим среднею внутри каждого месяца по датам которые в него входят с 26.07.2022

print(month)
print(df)

# Пример 4 (Выбросы)

import pandas as pd
import matplotlib.pyplot as plt

data = {'value': [1, 2, 3, 3, 4, 6, 7, 4 ,4, 3,6,7,3,4,7,8,3,55]}

df = pd.DataFrame(data)

# df.boxplot(column='value')
# plt.show()

#Определяем квантили
Q1 = df['value'].quantile(0.25)
Q3 = df['value'].quantile(0.75)
IQR = Q3 - Q1

#Создаем переменные для усов
downside = Q1 - 1.5*IQR
upside = Q3 + 1.5*IQR

# формируем новый дата фрейм с условия чтобы в него вошли только цифры из диапозона
df_new = df[(df['value'] >= downside) & (df['value'] <= upside)]

df_new.boxplot(column='value')
plt.show()
# print(df.describe())
print(f'Q1 = {Q1}\nQ3 = {Q3}\nIQR = {IQR}')


# Пример 5 (Категориальные данные)

import pandas as pd

data = {
     'name': ['Alica', 'Bob', "Roma", 'Anna', 'David'],
     'gender': ['female', 'male', 'male', 'female', 'male'],
     'department': [ 'HR', "Engineering", 'Marketing', "Engineering", 'HR']}

df = pd.DataFrame(data)

df['gender'] = df['gender'].astype('category') # Создаем категорийную переменную
df['department'] = df['department'].astype('category') # Создаем категорийную переменную

print(df['department'].cat.categories)

df['department'] = df['department'].cat.add_categories(['Finansist']) # Добававляем категорию

# print(df['gender'].cat.codes)
print(df['department'].cat.categories)

df['department'] = df['department'].cat.remove_categories(['HR']) # Удаляем категорию
print(df['department'].cat.categories)

print(df)


