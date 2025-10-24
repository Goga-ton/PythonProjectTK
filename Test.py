from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


class WikipediaSearcher:
    def __init__(self):
        """Инициализация браузера и настройка опций"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")

        try:
            service = Service(ChromeDriverManager().install())
            self.browser = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.browser, 10)
            self.current_url = None
            print("Браузер успешно инициализирован!")
        except Exception as e:
            print(f"Ошибка инициализации браузера: {e}")
            raise

    def search_wikipedia(self, query):
        """Поиск статьи на Википедии по запросу"""
        try:
            # Переходим на главную страницу Википедии
            self.browser.get("https://ru.wikipedia.org")

            # Находим поле поиска
            search_box = self.wait.until(
                EC.presence_of_element_located((By.ID, "searchInput"))
            )

            # Вводим запрос
            search_box.clear()
            search_box.send_keys(query)
            search_box.submit()

            # Ждем загрузки результатов
            time.sleep(2)

            # Проверяем, есть ли результаты поиска
            try:
                # Если есть результаты поиска, кликаем на первый
                first_result = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".mw-search-results .mw-search-result-heading a"))
                )
                first_result.click()
            except:
                # Если нет результатов поиска, возможно мы уже на странице статьи
                pass

            self.current_url = self.browser.current_url
            print(f"Перешли на страницу: {self.browser.title}")
            return True

        except Exception as e:
            print(f"Ошибка при поиске: {e}")
            return False

    def get_paragraphs(self):
        """Получение всех параграфов текущей статьи"""
        try:
            # Находим основной контент статьи
            content = self.browser.find_element(By.ID, "mw-content-text")

            # Ищем все параграфы
            paragraphs = content.find_elements(By.TAG_NAME, "p")

            # Фильтруем пустые параграфы
            valid_paragraphs = []
            for p in paragraphs:
                text = p.text.strip()
                if text and len(text) > 50:  # Только параграфы с достаточным количеством текста
                    valid_paragraphs.append(text)

            return valid_paragraphs

        except Exception as e:
            print(f"Ошибка при получении параграфов: {e}")
            return []

    def display_paragraphs(self):
        """Отображение параграфов статьи с возможностью листания"""
        paragraphs = self.get_paragraphs()

        if not paragraphs:
            print("Параграфы не найдены.")
            return

        current_index = 0

        while True:
            print(f"\n--- Параграф {current_index + 1} из {len(paragraphs)} ---")
            print(paragraphs[current_index])
            print("\n" + "=" * 80)

            print("\nДоступные действия:")
            print("1. Следующий параграф")
            print("2. Предыдущий параграф")
            print("3. Вернуться в главное меню")

            choice = input("Выберите действие (1-3): ").strip()

            if choice == "1":
                if current_index < len(paragraphs) - 1:
                    current_index += 1
                else:
                    print("Это последний параграф.")
            elif choice == "2":
                if current_index > 0:
                    current_index -= 1
                else:
                    print("Это первый параграф.")
            elif choice == "3":
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    def get_related_links(self):
        """Получение связанных ссылок из статьи"""
        try:
            # Находим основной контент
            content = self.browser.find_element(By.ID, "mw-content-text")

            # Ищем все ссылки в основном тексте
            links = content.find_elements(By.CSS_SELECTOR, "p a[href^='/wiki/']")

            # Фильтруем ссылки (исключаем служебные)
            valid_links = []
            for link in links:
                href = link.get_attribute("href")
                text = link.text.strip()

                # Исключаем служебные ссылки
                if (text and
                        not href.endswith(("redlink=1", "edit", "cite")) and
                        not text.startswith("[") and
                        len(text) > 2):
                    valid_links.append({
                        "text": text,
                        "href": href
                    })

            return valid_links[:10]  # Ограничиваем количество ссылок

        except Exception as e:
            print(f"Ошибка при получении связанных ссылок: {e}")
            return []

    def display_related_links(self):
        """Отображение связанных ссылок с возможностью перехода"""
        links = self.get_related_links()

        if not links:
            print("Связанные ссылки не найдены.")
            return

        print("\nДоступные связанные статьи:")
        for i, link in enumerate(links, 1):
            print(f"{i}. {link['text']}")

        print(f"{len(links) + 1}. Вернуться в главное меню")

        while True:
            try:
                choice = int(input(f"\nВыберите статью (1-{len(links) + 1}): "))

                if choice == len(links) + 1:
                    break
                elif 1 <= choice <= len(links):
                    selected_link = links[choice - 1]
                    print(f"Переходим к статье: {selected_link['text']}")

                    # Переходим по ссылке
                    self.browser.get(selected_link['href'])
                    self.current_url = self.browser.current_url
                    time.sleep(2)

                    print(f"Текущая статья: {self.browser.title}")

                    # Предлагаем действия для новой статьи
                    self.article_menu()
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")

            except ValueError:
                print("Пожалуйста, введите число.")

    def article_menu(self):
        """Меню действий для текущей статьи"""
        while True:
            print(f"\n--- {self.browser.title} ---")
            print("\nВыберите действие:")
            print("1. Листать параграфы текущей статьи")
            print("2. Перейти на одну из связанных страниц")
            print("3. Вернуться в главное меню")

            choice = input("Выберите действие (1-3): ").strip()

            if choice == "1":
                self.display_paragraphs()
            elif choice == "2":
                self.display_related_links()
            elif choice == "3":
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    def main_menu(self):
        """Главное меню программы"""
        print("=" * 60)
        print("           ПОИСКОВИК ВИКИПЕДИИ")
        print("=" * 60)

        while True:
            if not self.current_url:
                # Первоначальный запрос
                query = input("\nВведите ваш поисковый запрос: ").strip()
                if not query:
                    print("Запрос не может быть пустым.")
                    continue

                print(f"Ищем информацию о: {query}")
                if self.search_wikipedia(query):
                    self.article_menu()
                else:
                    print("Не удалось найти информацию. Попробуйте другой запрос.")
            else:
                # Если уже есть открытая статья
                print(f"\nТекущая статья: {self.browser.title}")
                print("\nВыберите действие:")
                print("1. Листать параграфы текущей статьи")
                print("2. Перейти на одну из связанных страниц")
                print("3. Новый поиск")
                print("4. Выйти из программы")

                choice = input("Выберите действие (1-4): ").strip()

                if choice == "1":
                    self.display_paragraphs()
                elif choice == "2":
                    self.display_related_links()
                elif choice == "3":
                    self.current_url = None
                elif choice == "4":
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")

    def close(self):
        """Закрытие браузера"""
        try:
            self.browser.quit()
            print("Браузер закрыт успешно!")
        except Exception as e:
            print(f"Ошибка при закрытии браузера: {e}")


def main():
    """Главная функция программы"""
    searcher = None

    try:
        searcher = WikipediaSearcher()
        searcher.main_menu()

    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        if searcher:
            searcher.close()


if __name__ == "__main__":
    main()