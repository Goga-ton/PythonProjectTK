# Создадим список для проверки
# в цикле переберем значения из списка и сравним их с их же версией прочитанной наоборот
# Если значение идентичны возвращаем True иначе False

test_strings = ["топот", "казак", "мадам", "привет"]

def is_palindrome_basic(stroka): #: str) -> bool:
    return stroka == stroka[::-1]

for i in test_strings:
    result = is_palindrome_basic(i)
    print(f'{i}: {result}')




