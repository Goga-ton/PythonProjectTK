from flask import Flask, render_template

app = Flask(__name__)

# Выводит приветсвие и потом если чер слэш а адресной строке браузера написать имя то выводимое сообщение на странице измениться
# @Dostyp.route('/')
# @Dostyp.route('/<pr>')
# def hello_world(pr="Незнакомец"):
#     return f'Hello World, {pr}!'

# Задаем несколько разных ссылок на одну и туже страницу - множественное декорирование
# @Dostyp.route('/new/')
# @Dostyp.route('/new1/')
# def new():
#     return 'New page'

# Можно задать условия вывода той или иной страницы
# @Dostyp.route('/')
# @Dostyp.route('/<pr>')
# def hello_world(pr=None):
#     if pr=="1234":
#         return f'Password is Right!'
#     else:
#         return f'The password is incorrect!'

# Пример работы с html кодом
# @Dostyp.route('/')
# def hello_world():
#     html = """
#     <h1>Тестовый запуск локального Сервера</h1>
#     <p>А это просто ТЕКС</p>
#     """
#     return html

@app.route('/')
def films():
    return render_template('DZ_VD04_time.html')

@app.route('/heroes/')
def heroes():
    return render_template('DZ_VD05_templates.html')


if __name__ == '__main__':
    app.run()