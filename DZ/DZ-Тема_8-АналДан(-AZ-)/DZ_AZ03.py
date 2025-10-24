from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

driver = webdriver.Chrome()

try:
     # Открываем страницу
     driver.get("https://www.divan.ru/category/divany")

     # Ждем загрузки страницы
     time.sleep(5)

     # Ищем все карточки с объявлениями
     cards = driver.find_elements(By.CSS_SELECTOR, 'div.lsooF')

     print(f"Найдено объявлений: {len(cards)}")
     print("-" * 50)

     with open('/DZ/divan_prices.csv', 'w', newline='', encoding='utf-8') as file:
          writer = csv.writer(file)

          # Записываем заголовки столбцов
          writer.writerow(['Номер', 'Название', 'Цена'])

          data = []
          # Проходим по каждой карточке и извлекаем данные
          for i, card in enumerate(cards, 1):
               try:
                    # Извлекаем цену
                    price_element = card.find_element(By.CSS_SELECTOR, 'span.ui-LD-ZU').text
                    price = int(price_element.replace(' ',''))
                    data.append(price)
                    # Извлекаем заголовок
                    title_element = card.find_element(By.CSS_SELECTOR, 'span[itemprop="name"]')
                    title = title_element.text

                    # Записываем данные в CSV
                    writer.writerow([i, title, price])

                    # Выводим информацию в консоль
                    print(f"{i}. {title}")
                    print(f"   Цена: {price}")
                    # print(f"   Адрес: {address}")
                    print()

               except Exception as e:
                    print(f"{i}. Не удалось получить данные для карточки")
                    # Записываем хотя бы номер, если данные не получены
                    writer.writerow([i, 'Ошибка', 'Нет данных', 'Нет данных', 'Нет данных'])

     print("Данные успешно сохранены в файл 'cian_prices.csv'")

except Exception as e:
     print(f"Произошла ошибка: {e}")

finally:
      driver.quit()
data_gr = np.array(data)
print(f'Среднеарифметичекое цены = {data_gr.mean()}')

plt.hist(data, bins=10, color='lightblue', edgecolor='black')
plt.title('Гистограмма стоимости диванов')
plt.xlabel('Цена в рублях')
plt.ylabel('Количество')
plt.show()