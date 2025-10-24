# Этот код по заданию урока писался на ИИ

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import matplotlib.pyplot as plt
import pandas as pd

driver = webdriver.Chrome()

try:
     # Открываем страницу
     driver.get("https://www.cian.ru/snyat-kvartiru-1-komn-ili-2-komn/")

     # Ждем загрузки страницы
     time.sleep(5)

     # Ищем все карточки с объявлениями
     cards = driver.find_elements(By.CSS_SELECTOR, '[data-name="CardComponent"]')

     print(f"Найдено объявлений: {len(cards)}")
     print("-" * 50)

     with open('cian_prices.csv', 'w', newline='', encoding='utf-8') as file:
          writer = csv.writer(file)

          # Записываем заголовки столбцов
          writer.writerow(['Номер', 'Название', 'Цена'])

          # Проходим по каждой карточке и извлекаем данные
          for i, card in enumerate(cards, 1):
               try:
                    # Извлекаем цену
                    price_element = card.find_element(By.CSS_SELECTOR, '[data-mark="MainPrice"]')
                    price = price_element.text

                    # Извлекаем заголовок
                    title_element = card.find_element(By.CSS_SELECTOR, '[data-mark="OfferTitle"]')
                    title = title_element.text

                    # Извлекаем адрес
                    # address_element = card.find_element(By.CSS_SELECTOR, '[data-name="GeoLabel"]')
                    # address = address_element.text

                    # Извлекаем параметры
                    # params_elements = card.find_elements(By.CSS_SELECTOR, '[data-name="Description"] > div')
                    # params = ", ".join([p.text for p in params_elements])

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
     # Закрываем браузер
     driver.quit()


def create_prices_only_csv(): # Создаем файл с ценами в виде чисел
     """
     Создает отдельный файл только с числовыми ценами
     """
     try:
          prices_numbers = []

          # Читаем основной файл
          with open('cian_prices.csv', 'r', encoding='utf-8') as file:
               reader = csv.reader(file)
               next(reader)  # Пропускаем заголовок

               for row in reader:
                    if len(row) >= 3:
                         price_text = row[2]  # Столбец с ценой

                         # Преобразуем "225 000 ₽/мес." → 225000
                         clean_price = ''.join(char for char in price_text if char.isdigit())
                         if clean_price:
                              numeric_price = int(clean_price)
                              prices_numbers.append(numeric_price)

          # Сохраняем в новый файл
          with open('prices_only.csv', 'w', newline='', encoding='utf-8') as file:
               writer = csv.writer(file)
               writer.writerow(['Цена'])  # Только один заголовок

               for price in prices_numbers:
                    writer.writerow([price])

          print(f"✅ Файл 'prices_only.csv' создан с {len(prices_numbers)} ценами")
          print(f"💰 Диапазон цен: от {min(prices_numbers)} до {max(prices_numbers)}")

     except Exception as e:
          print(f"❌ Ошибка при создании файла с ценами: {e}")


def simple_histogram(): # строим гистограму
     """
     Простая гистограмма для новичка
     """
     try:
          # Читаем данные
          df = pd.read_csv('prices_only.csv')
          prices = df['Цена']

          # Создаем график
          # plt.figure(figsize=(10, 5))
          plt.hist(prices, bins=7, color='lightblue', edgecolor='black')

          # Подписи
          plt.title('Гистограмма цен на аренду')
          plt.xlabel('Цена в рублях')
          plt.ylabel('Количество')

          # Показываем
          plt.show()

          print(f"Построена гистограмма для {len(prices)} цен")

     except:
          print("Сначала запустите парсер для создания файла prices_only.csv")


create_prices_only_csv()

simple_histogram()