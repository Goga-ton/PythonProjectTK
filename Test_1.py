import matplotlib.pyplot as plt
import pandas as pd


prices = pd.read_csv('/DZ/DZ-Тема_8-АналДан(-AZ-)/divan_prices.csv')['Цена']
#prices = df['Цена']


plt.hist(prices, bins=7, color='lightblue', edgecolor='black')

plt.title('Гистограмма цен на аренду')
plt.xlabel('Цена в рублях')
plt.ylabel('Количество')

plt.show()

