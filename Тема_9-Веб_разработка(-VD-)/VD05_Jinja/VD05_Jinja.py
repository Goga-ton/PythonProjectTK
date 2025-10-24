from flask import Flask, render_template

app = Flask(__name__)


# @Dostyp.route('/')
# def films():
#     context={
#         "caption":"Это ПЕРВАЯ штурка",
#         "user":"Вася",
#         "number": 8,
#         "list": ["Толя", "Сергей", "Никита", "Оля", "Света", "Тома"],
#         "poem": ["Я помню, ранило березу",
#                 "Осколком бомбы на заре.",
#                 "Студеный сок бежал, как слезы,",
#                 "По изувеченной коре.",
#                 "За лесом пушки грохотали,",
#                 "Клубился дым пороховой.",
#                 "Но мы столицу отстояли,",
#                 "Спасли березу под Москвой."]
#
#     }
#     return render_template('VD05_conditions.html', **context)



@app.route('/')
def main():
    return render_template('VD05_main.html')

@app.route('/heroes/')
def index():
    context = {
        "caption": " index (Герои)",
        "link": "Ну так для тестинго=а"
    }
    return render_template('VD05_index.html', **context)


if __name__ == '__main__':
    app.run()